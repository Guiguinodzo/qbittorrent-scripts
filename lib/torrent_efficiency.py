def human_readable_duration(seconds: int) -> str:
    if seconds > 3600 * 24:
        return f"{seconds / 3600 / 24:.2f}days"
    if seconds > 3600:
        return f"{seconds / 3600:.2f}h"
    elif seconds > 60:
        return f"{seconds / 60:.2f}m"
    else:
        return f"{seconds}s"

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
    category: str
    tags: list[str]
    age: int
    seeding_time: int
    ratio: float
    upload_rate: float
    size: int
    efficiency: float

    def __init__(self, hash: str, private_tracker: str, category: str, tags: list[str], age: int, seeding_time: int, ratio: float,
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
        self.category = category
        self.tags = tags
        self.age = age
        self.seeding_time = seeding_time
        self.ratio = ratio
        self.upload_rate = upload_rate
        self.size = size
        self.efficiency = upload_rate / size if size > 0 else -1.0

    def human_readable_efficiency(self) -> str:
        if self.efficiency > 1:
            return f"{self.efficiency:.2f} b/b/s"
        elif self.efficiency * 1024 > 1:
            return f"{self.efficiency * 1024:.2f} b/kb/s"
        elif self.efficiency * 1024 * 1024 > 1:
            return f"{self.efficiency * 1024 * 1024 :.2f} b/mb/s"
        elif self.efficiency * 1024 * 1024 * 1024 > 1:
            return f"{self.efficiency * 1024 * 1024 * 1024:.2f} b/GB/s"
        else:
            return f"{self.efficiency} b/b/s"

    def human_readable_seeding_time(self) -> str:
        return human_readable_duration(self.seeding_time)

    def human_readable_age(self) -> str:
        return human_readable_duration(self.age)

