
import oge_cores
import oge_cores.coverage.coverage


def test_coverage():
    coverage = oge_cores.coverage.coverage.get_coverage("a","B")
    assert type(coverage) == type(coverage)