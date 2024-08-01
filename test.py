from oge_cores.processes import requester

from oge_cores.processes import process_utils, request_format, requester
from oge_cores.coverage import get_coverage_from_file

from oge_cores.config import config

c = get_coverage_from_file("oge_cores/test/test_data/test.tif")
input_format = requester.requester.get_models_inputs("a")
res = process_utils.inputs2request(input_format, "Landsat_wh_s.tif",True,0,"area_wh.shp","sample_wh.shp","name",1,"1.txt","11.txt",10,2,10,True,True,0.01)
result = requester.requester.post_wps(config.endpoint,"DecisionTreeClassifier",res)
print(result)