from oge_cores.processes import process_utils,request_format,requester
from oge_cores.coverage import get_coverage_from_file
def test_request():
    c = get_coverage_from_file("oge_cores/test/test_data/test.tif")
    f = request_format.Requestformat("a",{"coverage":"coverage","a":"string"},{"b":"int"})

    process_utils.inputs2request(f,c,"a")
    assert process_utils.inputs2request(f,c,"a",1) == process_utils.inputs2request(f,coverage = c, a = "a",b = 1)
import json
def post_wps(endpoint, process_name, data) -> dict:
        """发送post请求

        Args:
        endpoint: 服务地址
        data(dict): 请求参数
        """
        # 格式转换
        data = [{key: value} for key, value in data.items()]
        input_json = {
            "identifier": process_name,
            "request_from": "self.id",
            "work_dir": "self.work_dir",
            "inputs": data,
            "mode": "sync",
        }
        json_data = json.dumps(input_json)
        print(json_data)
def test_format():
    input_format = requester.requester.get_models_inputs("a")
    res = process_utils.inputs2request(input_format,"a","b","c","d")
    post_wps("a","a",res)