import qbittorrentapi
import lib.tracker
from lib.config import read_config, Config

def handle_private_torrent(torrent: qbittorrentapi.torrents.TorrentDictionary, private_tracker: lib.tracker.Tracker):
    raw_tags = getattr(torrent, "tags", getattr(torrent.info, "tags", ""))  # support both .tags and .info.tags
    if isinstance(raw_tags, str):
        tags_list = [t.strip() for t in raw_tags.split(",") if t.strip()]
    else:
        tags_list = list(raw_tags)

    tag_found = any((private_tracker.tag == tag) for tag in tags_list)
    print(f"tracker: {private_tracker.name} (tag: {tags_list})")
    print(f"torrent: {torrent.name} ({torrent.info.hash})  - tags: {torrent.info.tags}")
    print(f"tag found ? {tag_found}")

    if not tag_found:
        torrent.add_tags([private_tracker.tag])
        print(f"Added {private_tracker.tag} to {torrent.name} ({torrent.info.hash})")

def handle_public_torrent(torrent: qbittorrentapi.torrents.TorrentDictionary):
    raw_tags = getattr(torrent, "tags", getattr(torrent.info, "tags", ""))  # support both .tags and .info.tags
    if isinstance(raw_tags, str):
        tags_list = [t.strip() for t in raw_tags.split(",") if t.strip()]
    else:
        tags_list = list(raw_tags)

    public_tag = "public"

    tag_found = any((public_tag == tag) for tag in tags_list)
    print(f"torrent: {torrent.name} ({torrent.info.hash})  - tags: {torrent.info.tags}")
    print(f"tag found ? {tag_found}")

    if not tag_found:
        torrent.add_tags([public_tag])
        print(f"Added {public_tag} to {torrent.name} ({torrent.info.hash})")


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

freeleech_tag = "freeleech"
total_downloaded = 0
total_downloaded_no_freeleech = 0
total_uploaded = 0

for private_tracker in lib.tracker.private_trackers:
    urls = private_tracker.urls()
    print(f"Tracker {private_tracker.name}: {urls}")


for torrent in qbt_client.torrents_info():

    matching_private_trackers = list(filter(lambda private_tracker : lib.tracker.torrent_matches_private_tracker(torrent, private_tracker), lib.tracker.private_trackers))

    if len(matching_private_trackers) == 0:
        # print(f"No private tracker found for {torrent.name} ({torrent.info.hash}): skipping")
        handle_public_torrent(torrent)

    elif len(matching_private_trackers) > 1:
        print(f"Multiple private trackers found for {torrent.name} ({torrent.info.hash}): skipping")
        continue

    else:
        handle_private_torrent(torrent, matching_private_trackers[0])

