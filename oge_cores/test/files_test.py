import oge_cores.common.ogefiles
import oge_cores.coverage.oge_image


def test_file():
    tiff_file = oge_cores.common.ogefiles.CoverageFile("")
    assert oge_cores.common.ogefiles.file_pointer_dict.get_file_num() == 1

    tiff_file1 = tiff_file
    assert oge_cores.common.ogefiles.file_pointer_dict.get_file_num() == 1

    del tiff_file
    assert oge_cores.common.ogefiles.file_pointer_dict.get_file_num() == 1

    del tiff_file1
    assert oge_cores.common.ogefiles.file_pointer_dict.get_file_num() == 0

    txt_file = oge_cores.common.ogefiles.TextFile("1")
    assert oge_cores.common.ogefiles.file_pointer_dict.get_file_num() == 1


def test_image():
    tiff_file = "oge_cores/test/test_data/test.tif"

    img = oge_cores.coverage.oge_image.Image(coverage_file_path=tiff_file)

    img1 = img
    assert oge_cores.common.ogefiles.file_pointer_dict.get_file_num() == 1
    img.to_numpy_array()

    coverage = oge_cores.coverage.coverage.get_coverage("a", "B")
    assert oge_cores.common.ogefiles.file_pointer_dict.get_file_num() == 2
