DEFAULT_EXCLUDE_CATEGORIES = ["tv-sonarr", "radarr", "manual"]

class CleaningRules:
    tracker: str
    minimumAge: int
    minimumRatio: float
    exclude_categories: list[str]

    def __init__(self, tracker: str, minimum_age: int, minimum_ratio: float, exclude_categories: list[str]):
        self.tracker = tracker
        self.minimumAge = minimum_age
        self.minimumRatio = minimum_ratio
        self.exclude_categories = exclude_categories

TRACKER_CLEANING_RULES = {
    "ygg": CleaningRules("ygg", 86400 * 3, 2.0, DEFAULT_EXCLUDE_CATEGORIES),
    "torrentleech": CleaningRules("torrentleech", 86400 * 14, 1.00, DEFAULT_EXCLUDE_CATEGORIES)
}
