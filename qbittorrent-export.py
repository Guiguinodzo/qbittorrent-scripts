import time

import qbittorrentapi

from lib.config import read_config
from lib.tracker import private_trackers, torrent_matches_private_tracker, initialize_private_trackers
from lib.export import TorrentExport, TORRENT_EXPORT_HEADER

config = read_config("config.json")
initialize_private_trackers(config)

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

now = int(time.time())  # epoch seconds (if needed time_ns())

filename = f"exports/{now}.csv"
with open(filename, "x") as f:
    # header
    f.write(f"{TORRENT_EXPORT_HEADER}\n")

    for torrent in qbt_client.torrents_info():

        matching_private_trackers = list(filter(
            lambda private_tracker: torrent_matches_private_tracker(torrent, private_tracker),
            private_trackers
        ))
        private_tracker_of_torrent = None
        if len(matching_private_trackers) > 1:
            print(f"Multiple private trackers found for {torrent.name} ({torrent.info.hash}): skipping")
            continue
        elif len(matching_private_trackers) == 1:
            private_tracker_of_torrent = matching_private_trackers[0]

        torrent_id = torrent.hash
        tags = [t.strip() for t in torrent.info.tags.split(",") if t.strip()]
        uploaded = torrent.uploaded
        downloaded = torrent.downloaded
        size = torrent.size
        tracker = private_tracker_of_torrent.name if private_tracker_of_torrent is not None else "public"
        added_on = torrent.added_on  # epoch
        completed_on = torrent.completion_on
        complete = torrent.amount_left == 0

        if completed_on > 0 and not complete:
            print(f"ERROR: torrent {torrent_id} has completed_on ({completed_on}) but is not complete")

        torrent_export = TorrentExport(torrent_id, size, downloaded, uploaded, complete, tracker, tags, added_on,
                                       completed_on, now)
        # write line to file
        f.write(f"{torrent_export.asCsvLine()}\n")

        print(torrent_export.asCsvLine())

