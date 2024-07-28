import oge_cores.common.metadata as metadata


def test_metadata():
    path = "oge_cores/test/test_data/test.tif"
    coverage_metadata = metadata.get_coverage_metadata_from_file(path)
    coverage_metadata.print_metadata()
