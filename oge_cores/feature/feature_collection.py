from oge_cores.feature import feature
from oge_cores.filter import filter


class FeatureCollection:
    def __init__(self) -> None:
        self.collection = []

    def filter(self, filter: filter.Filter) -> None:
        pass
