from oge_cores.coverage import coverage
from oge_cores.filter import filter


class Coverage_Collection:
    def __init__(self) -> None:
        # 使用list存储的
        self.collection = []

    def filter(self, filter: filter.Filter) -> None:
        pass
