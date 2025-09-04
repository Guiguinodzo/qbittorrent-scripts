import sys
import time

import qbittorrentapi

from lib.config import read_config
from lib.export import TorrentExport, parse_torrent_export_from_csv_line, TORRENT_EXPORT_HEADER
from lib.cleaning_rules import TRACKER_CLEANING_RULES, CleaningRules
from lib.torrent_efficiency import TorrentEfficiency
from lib.misc import human_readable_size

MINIMUM_INTERVAL_BETWEEN_STATS = 3600 * 24


def parse_file(filename: str, check_header: bool = True) -> dict[str, TorrentExport]:
    stats_by_hash = {}
    with open(filename, "r") as f:
        header = f.readline().strip()
        if check_header and header != TORRENT_EXPORT_HEADER:
            raise Exception(f"Invalid file format.\nExpected header: {TORRENT_EXPORT_HEADER}\nFound header   : {header}")
        for line in f:
            torrent_export = parse_torrent_export_from_csv_line(line)
            stats_by_hash[torrent_export.hash] = torrent_export

    return stats_by_hash


def is_torrent_potentially_removable(torrent: TorrentEfficiency) -> bool:
    if torrent.private_tracker is None or torrent.private_tracker not in TRACKER_CLEANING_RULES.keys():
        return False

    rules : CleaningRules = TRACKER_CLEANING_RULES[torrent.private_tracker]

    # A torrent should either have been seeding for a sufficient amount of time or have minimum ratio before being
    # considered for removal.
    # TODO : age != seeding time, export should include completedOn timestamp
    return ((torrent.seeding_time > rules.minimumAge or torrent.ratio > rules.minimumRatio)
            and torrent.category not in rules.exclude_categories )


config = {}
try:
    import json

    with open("config.json", "r") as f:
        config = json.load(f)
except Exception as e:
    print(f"Failed to load config.json: {e}")
    exit(1)

config = read_config("config.json")

conn_info = dict(
    host=config.qbittorrent.host,
    port=config.qbittorrent.port,
    username=config.qbittorrent.username,
    password=config.qbittorrent.password
)

qbt_client = qbittorrentapi.Client(**conn_info)

try:
    qbt_client.auth_log_in()
    print("Successfully authenticated")
except qbittorrentapi.LoginFailed as e:
    print(f"Failed to authenticate: {e}")

old_stats_filename = sys.argv[1]
new_stats_filename = sys.argv[2]

new_timestamp = int(new_stats_filename.split('/')[-1].split('.')[0])
old_timestamp = int(old_stats_filename.split('/')[-1].split('.')[0])
delta = new_timestamp - old_timestamp
if delta < MINIMUM_INTERVAL_BETWEEN_STATS:
    print(f"Stats are too close to each others ({delta}s), skipping")
    exit(0)

old_stats = parse_file(old_stats_filename)
new_stats = parse_file(new_stats_filename)

torrents_efficiency: dict[str, TorrentEfficiency] = {}

for hash in new_stats.keys():
    new_statsN = new_stats[hash]
    if hash not in old_stats:
        print(f"New torrent ({hash}), skipping")
        continue
    elif not new_statsN.complete:
        print(f"Incomplete torrent ({hash}), skipping")
        continue

    now = int(time.time())
    age = now - new_statsN.added_on
    seeding_time = now - new_statsN.completed_on

    old_statsN = old_stats[hash]

    uploaded_since = new_statsN.uploaded - old_statsN.uploaded
    upload_speed = uploaded_since / delta

    torrents_efficiency[hash] = TorrentEfficiency(hash, new_statsN.tracker, new_statsN.category, new_statsN.tags, age,
                                                  seeding_time, new_statsN.ratio, upload_speed, new_statsN.size)

inefficient_torrents = []
threshold = 0.0
freeable_size = 0

for torrent in sorted(torrents_efficiency.values(), key=lambda torrent: torrent.efficiency, reverse=True):
    if is_torrent_potentially_removable(torrent):
        print(
            f"Potentially removable torrent: {torrent.hash} ({torrent.private_tracker} / {torrent.category}) : {torrent.human_readable_efficiency()} (Size: {human_readable_size(torrent.size)}, age: {torrent.human_readable_age()}, seeding time: {torrent.human_readable_seeding_time()})")
        if threshold >= torrent.efficiency >= 0 and "inefficient" not in torrent.tags:
            print(f"Adding tag 'inefficient' to {torrent.hash} ({torrent.private_tracker})")
            inefficient_torrents.append(torrent)
            freeable_size += torrent.size


torrents_hashes = [torrent.hash for torrent in inefficient_torrents]
print(f"Found {len(torrents_hashes)} torrents to be tagged as 'inefficient'. Would free {human_readable_size(freeable_size)}")
for torrent_hash in torrents_hashes:
    qbt_client.torrents_addTags(hashes=[torrent_hash], tags=["inefficient"])

# todo: apprise/pushover

    # another script (or this one, tbd) will compare with previous stats
    # uploaded_since = statsN.uploaded - statsN-1.uploaded
    # efficiency = uploaded_since / size
    # ie efficiency is upload rate by size taken on disk : if two files upload at the same rate, then the best one is
    # the tiniest one
    # exclude:
    # - below 1 ratio and added less than 2 weeks ago (cf H&R rules of torrentleech)
    # - not tagged ratio-XXX
    # - tagged sonar-tv/radaar/?
