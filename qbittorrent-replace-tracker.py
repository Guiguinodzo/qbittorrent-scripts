# from https://github.com/qbittorrent/qBittorrent/issues/18539#issuecomment-1574066467

from datetime import datetime
import qbittorrentapi
from lib.tracker import initialize_private_trackers, get_tracker

from lib.config import read_config

# See the example with credentials at https://github.com/rmartin16/qbittorrent-api/blob/main/README.md
config = read_config("config.json")
initialize_private_trackers(config)

conn_info = dict(
    host=config.qbittorrent.host,
    port=config.qbittorrent.port,
    username=config.qbittorrent.username,
    password=config.qbittorrent.password
)

qbt_client = qbittorrentapi.Client(**conn_info)
qbt_client.auth_log_in()

ygg_tracker = get_tracker("ygg")
api_key = ygg_tracker.api_key
tracker_to_replace = f"http://connect.maxp2p.org:8080/{api_key}/announce"
tracker_replacement = f"http://tracker.p2p-world.net:8080/{api_key}/announce"

for torrent in qbt_client.torrents_info():
    removed_tracker = False
    for tracker in torrent.trackers:
        if tracker_to_replace in tracker.url:
            torrent.remove_trackers(urls=[tracker.url])
            print(f"Removed {tracker.url} from #{datetime.fromtimestamp(torrent.added_on)}# {torrent.name}")
            removed_tracker = True

    if removed_tracker:
        tracker_replacement_exists = False
        for tracker in torrent.trackers:
            if tracker_replacement in tracker.url:
                tracker_replacement_exists = True

        if not tracker_replacement_exists:
            torrent.add_trackers(tracker_replacement)
            print(f"Added {tracker_replacement} to #{datetime.fromtimestamp(torrent.added_on)}# {torrent.name}")
        else:
            print(f"Tracker {tracker_replacement} already set for #{datetime.fromtimestamp(torrent.added_on)}# {torrent.name}")
