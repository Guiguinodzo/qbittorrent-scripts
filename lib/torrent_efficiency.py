class TorrentEfficiency:
    """
    Class represents the torrents info to evaluate its efficiency
    :cvar hash: id of the torrent
    :cvar private_tracker: name of the private tracker if any
    :cvar tags: list of tags
    :cvar age: age in seconds
    :cvar seeding_time: seeding time in seconds
    :cvar ratio: ratio
    :cvar upload_rate: bytes uploaded per second
    :cvar size: size in bytes
    """
    hash: str
    private_tracker: str
    tags: list[str]
    age: int
    seeding_time: int
    ratio: float
    upload_rate: float
    size: int
    efficiency: float

    def __init__(self, hash: str, private_tracker: str, tags: list[str], age: int, seeding_time: int, ratio: float,
                 upload_rate: float, size: int):
        """
        :param hash: id of the torrent
        :param private_tracker: name of the private tracker if any
        :param tags: list of tags
        :param age: age in seconds
        :param seeding_time: seeding time in seconds
        :param ratio: ratio
        :param upload_rate: bytes uploaded per second
        :param size: size in bytes
        """
        self.hash = hash
        self.private_tracker = private_tracker
        self.tags = tags
        self.age = age
        self.seeding_time = seeding_time
        self.ratio = ratio
        self.upload_rate = upload_rate
        self.size = size
        self.efficiency = upload_rate / size

