
import oge_cores
import oge_cores.coverage.coverage



def test_coverage():
    c = oge_cores.coverage.coverage.get_coverage_from_file("oge_cores/test/test_data/test.tif")
    array = c.to_numpy_array()
    assert array.shape[0] > 0