from oge_cores.processes import process_utils,request_format
from oge_cores.coverage import get_coverage_from_file
def test_request():
    c = get_coverage_from_file("oge_cores/test/test_data/test.tif")
    f = request_format.Requestformat("a",{"coverage":"Coverage","a":"string"},{"b":"int"})

    process_utils.inputs2request(f,c,"a")
    process_utils.inputs2request(f,c,"a",1)
    process_utils.inputs2request(f,coverage = c, a = "s",b = 1)