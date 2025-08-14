DEFAULT_EXCLUDE_TAGS = ["sonar-tv", "radaar"]

class CleaningRules:
    tracker: str
    minimumAge: int
    minimumRatio: float
    exclude_tags: list[str]

    def __init__(self, tracker: str, minimum_age: int, minimum_ratio: float, exclude_tags: list[str]):
        self.tracker = tracker
        self.minimumAge = minimum_age
        self.minimumRatio = minimum_ratio
        self.exclude_tags = exclude_tags

TRACKER_CLEANING_RULES = {
    "ygg": CleaningRules("ygg", 86400 * 3, 2.0),
    "torrentleech": CleaningRules("torrentleech", 86400 * 14, 1.00)
}
