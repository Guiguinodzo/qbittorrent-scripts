import sys

import qbittorrentapi
import lib.tracker
from lib.config import read_config, Config

config = read_config("config.json")
lib.tracker.initialize_private_trackers(config)

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

hash = sys.argv[0]

torrents = qbt_client.torrents_info()
for torrent in torrents:
    print(f"{torrent.info.hash} -> {torrent.info.name}")

matching_torrent = filter(lambda torrent : torrent.info.hash == hash, qbt_client.torrents_info())

for torrent in matching_torrent:
    print(f"Matching torrent: {torrent.info.name}")
