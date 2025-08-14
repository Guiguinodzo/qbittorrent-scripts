class QbittorrentConfig:
    host: str
    port: int
    username: str
    password: str

class TrackerConfig:
    name: str
    api_key: str
    tag: str
    urls: list[str]


class Config:
    qbittorrent: QbittorrentConfig
    trackers: list[TrackerConfig]


def read_config(path: str) -> Config:
    config = Config()
    try:
        import json

        with open(path, "r") as f:
            config_raw = json.load(f)
            config.qbittorrent = QbittorrentConfig()
            config.qbittorrent.host = config_raw["qbittorrent"]["host"]
            config.qbittorrent.port = config_raw["qbittorrent"]["port"]
            config.qbittorrent.username = config_raw["qbittorrent"]["username"]
            config.qbittorrent.password = config_raw["qbittorrent"]["password"]
            config.trackers = []
            for tracker_name in config_raw["trackers"].keys():
                tracker_raw = config_raw["trackers"][tracker_name]
                tracker = TrackerConfig()
                tracker.name = tracker_name
                tracker.api_key = tracker_raw["api_key"]
                tracker.tag = tracker_raw["tag"]
                tracker.urls = tracker_raw["urls"]
                config.trackers.append(tracker)
    except Exception as e:
        print(f"Failed to load config.json: {e}")
        exit(1)
    return config