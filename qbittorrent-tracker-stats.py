# from https://github.com/qbittorrent/qBittorrent/issues/18539#issuecomment-1574066467
from datetime import datetime

import qbittorrentapi

from lib.config import read_config
from lib.misc import human_readable_size
from lib.tracker import initialize_private_trackers, private_trackers, get_tracker

# def human_readable_size(size_in_bytes: int) -> str:
#     if abs(size_in_bytes) < 1024:
#         return f"{size_in_bytes} bytes"
#     elif abs(size_in_bytes) < 1024 * 1024:
#         return f"{size_in_bytes / 1024:.2f} KB"
#     elif abs(size_in_bytes) < 1024 * 1024 * 1024:
#         return f"{size_in_bytes / 1024 / 1024:.2f} MB"
#     else:
#         return f"{size_in_bytes / 1024 / 1024 / 1024:.2f} GB"


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

try:
    qbt_client.auth_log_in()
    print("Successfully authenticated")
except qbittorrentapi.LoginFailed as e:
    print(f"Failed to authenticate: {e}")

freeleech_tag = "freeleech"
total_downloaded = 0
total_downloaded_no_freeleech = 0

total_uploaded = 0

tracker_urls = get_tracker("torrentleech").urls()

for torrent in qbt_client.torrents_info():
    is_target_tracker = False
    for tracker in torrent.trackers:
        for tracker_url in tracker_urls:
            is_target_tracker |= tracker_url in tracker.url

    if not is_target_tracker:
        # print(f"Skipping {torrent.name} because it doesn't have a tracker in {tracker_urls}")
        continue

    name = torrent.name
    downloaded = torrent.downloaded
    uploaded = torrent.uploaded
    is_freeleech = freeleech_tag in torrent.tags

    # print(f"{name}: {downloaded} bytes downloaded, {uploaded} bytes uploaded, freelech: {'yes' if is_freeleech else 'no'}")
    # print(f"{torrent.info.hash};{downloaded};{uploaded};{is_freeleech};{name}")

    total_downloaded += downloaded
    total_uploaded += uploaded
    if not is_freeleech:
        total_downloaded_no_freeleech += downloaded

print("Values are based on the CLIENT, it does not take into account dl/ul form others clients (such as transmission)")
print(f"Total downloaded                        : {total_downloaded} bytes ({human_readable_size(total_downloaded)})")
print(f"Total uploaded                          : {total_uploaded} bytes ({human_readable_size(total_uploaded)})")
print(f"Total downloaded (excluding freeleech)  : {total_downloaded_no_freeleech} bytes ({human_readable_size(total_downloaded_no_freeleech)})")
print(f"Credit                                  : {total_uploaded - total_downloaded_no_freeleech} bytes ({human_readable_size(total_uploaded - total_downloaded_no_freeleech)})")
