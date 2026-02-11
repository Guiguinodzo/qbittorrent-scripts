import qbittorrentapi

from lib.config import read_config


def torrent_is_active(torrent: qbittorrentapi.torrents.TorrentDictionary):
    return torrent.state in (
        "uploading",
        "queuedUP",
        "checkingUP",
        "forcedUP",
        "allocating",
        "downloading",
        "metaDL",
        "queuedDL",
        "checkingDL",
        "forcedDL",
        "checkingResumeData"
    )

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

nb_torrents = 0
nb_public_torrents = 0
nb_public_torrents_stopped = 0
nb_public_torrents_resumed = 0

for torrent in qbt_client.torrents_info():

    nb_torrents += 1

    if not "public" in torrent.info.tags:
        # print(f"Skipping {torrent.name} because it doesn't have the 'public' tag (tags: {torrent.info.tags})")
        continue

    nb_public_torrents += 1

    ratio = torrent.ratio
    active_torrent = torrent_is_active(torrent)

    if ratio > 2.0 and active_torrent:
        print(f"Stopping {torrent.name} ({torrent.info.hash}) because ratio is high enough: {torrent.ratio} (current state: {torrent.state})")
        nb_public_torrents_stopped += 1
        torrent.stop()

    elif ratio < 1.0 and not active_torrent and not "import-transmission" in torrent.info.tags:
        print(f"Resuming {torrent.name} ({torrent.info.hash}) because ratio is too low: {torrent.ratio}")
        nb_public_torrents_resumed += 1
        torrent.resume()

    elif "import-transmission" in torrent.info.tags and active_torrent:
        print(f"Stopping {torrent.name} ({torrent.info.hash}) because it was imported from transmission")
        nb_public_torrents_stopped += 1
        torrent.stop()

print(f"Total torrents: {nb_torrents}")
print(f"Total public torrents: {nb_public_torrents}")
print(f"Total public torrents stopped: {nb_public_torrents_stopped}")
print(f"Total public torrents resumed: {nb_public_torrents_resumed}")