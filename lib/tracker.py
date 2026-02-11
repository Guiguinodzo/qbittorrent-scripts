import qbittorrentapi
from lib.config import Config


class Tracker:
    name: str
    api_key: str
    _urls: list[str]
    tag: str

    def __init__(self, name: str, api_key: str, tag: str, urls: list[str]):
        self.name = name
        self.api_key = api_key
        self._urls = urls
        self.tag = tag

    def urls(self) -> list[str]:
        return list(map(lambda url: url.replace('${API_KEY}', self.api_key), self._urls))

    def url_matches_tracker(self, input_url: str):
        return any(tracker_url in input_url for tracker_url in self.urls())

private_trackers = []

def initialize_private_trackers(config: Config):
    for private_tracker in config.trackers:
        private_trackers.append(Tracker(private_tracker.name, private_tracker.api_key, private_tracker.tag, private_tracker.urls))


def torrent_matches_private_tracker(torrent: qbittorrentapi.torrents.TorrentDictionary, private_tracker: Tracker):
    for tracker in torrent.trackers:
        if private_tracker.url_matches_tracker(tracker.url):
            return True
    return False

def get_tracker(name: str) -> Tracker | None:
    for private_tracker in private_trackers:
        if private_tracker.name == name:
            return private_tracker
    return None