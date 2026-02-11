TORRENT_EXPORT_HEADER = "hash;size;downloaded;uploaded;ratio;complete;tracker;category;tags;added_on;completed_on;timestamp"

class TorrentExport:
    hash: str
    size: int
    downloaded: int
    uploaded: int
    ratio: float
    complete: bool
    tracker: str
    category: str
    tags: list[str]
    added_on: int
    completed_on: int
    timestamp: int

    def __init__(self, torrent_hash, size, downloaded, uploaded, complete, tracker, category, tags, added_on, completed_on,
                 timestamp):
        self.hash = torrent_hash
        self.size = size
        self.downloaded = downloaded
        self.uploaded = uploaded
        self.ratio = uploaded / size if size > 0 else 0
        self.complete = complete
        self.tracker = tracker
        self.category = category
        self.tags = tags
        self.added_on = added_on
        self.completed_on = completed_on
        self.timestamp = timestamp

    def asCsvLine(self) -> str:
        return f"{self.hash};{self.size};{self.downloaded};{self.uploaded};{self.ratio};{self.complete};{self.tracker};{self.category};{','.join(self.tags)};{self.added_on};{self.completed_on};{self.timestamp}"

def parse_torrent_export_from_csv_line(csv_line: str) -> TorrentExport:
    fields = csv_line.split(";")
    if len(fields) == 11: # without category
        return TorrentExport(fields[0], int(fields[1]), int(fields[2]), int(fields[3]), fields[5] == "True", fields[6], "unknown",
                         fields[7].split(","), int(fields[8]), int(fields[9]), int(fields[10]))
    else:
        return TorrentExport(fields[0], int(fields[1]), int(fields[2]), int(fields[3]), fields[5] == "True", fields[6], fields[7],
                         fields[8].split(","), int(fields[9]), int(fields[10]), int(fields[11]))
