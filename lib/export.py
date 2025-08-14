TORRENT_EXPORT_HEADER = "hash;size;downloaded;uploaded;ratio;complete;tracker;tags;added_on;completed_on;timestamp"

class TorrentExport:
    hash: str
    size: int
    downloaded: int
    uploaded: int
    ratio: float
    complete: bool
    tracker: str
    tags: list[str]
    added_on: int
    completed_on: int
    timestamp: int

    def __init__(self, hash, size, downloaded, uploaded, complete, tracker, tags, added_on, completed_on, timestamp):
        self.hash = hash
        self.size = size
        self.downloaded = downloaded
        self.uploaded = uploaded
        self.ratio = uploaded / size
        self.complete = complete
        self.tracker = tracker
        self.tags = tags
        self.added_on = added_on
        self.completed_on = completed_on
        self.timestamp = timestamp

    def asCsvLine(self) -> str:
        return f"{self.hash};{self.size};{self.downloaded};{self.uploaded};{self.ratio};{self.complete};{self.tracker};{','.join(self.tags)};{self.added_on};{self.completed_on};{self.timestamp}"

def parse_torrent_export_from_csv_line(csv_line: str) -> TorrentExport:
    fields = csv_line.split(";")
    return TorrentExport(
        fields[0],
        int(fields[1]),
        int(fields[2]),
        int(fields[3]),
        fields[4] == "True",
        fields[5],
        fields[6].split(","),
        int(fields[7]),
        int(fields[8]),
        int(fields[9])
    )