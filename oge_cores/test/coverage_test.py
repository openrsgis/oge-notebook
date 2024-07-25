from oge_cores.coverage import coverage



def test_coverage():
    c = coverage.get_coverage_from_file("oge_cores/test/test_data/test.tif")
    array = c.to_numpy_array()
    array = array + 1
    c1 = coverage.numpy_array_metadata2coverage(array,c.metadata)

    c2 = coverage.numpy_array2coverage(array,c1.crs,c1.geo_transform)

    assert c1.dtype == c2.dtype
    print(c2.rows)
    print(c2.cols)
    assert c1.cols == c2.cols
    assert c1.bands_num == c2.bands_num