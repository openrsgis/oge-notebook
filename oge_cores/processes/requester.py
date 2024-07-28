"""process请求类"""

from typing import Dict
from pywps import Service, ComplexInput, LiteralInput
import requests
import json

from oge_cores.processes import request_format
from oge_cores.processes import process_utils


class Requester:
    """用于与算子间的通信请求，单例类，会在引入时更新"""

    # TODO: 从模型服务中心获取现有模型及元信息
    def __init__(self) -> None:
        # 从模型到地址的映射关系
        self.models_endpoint: Dict[str, str] = {}

        # 从模型名称到输入的映射关系。第一位是进程id，后续是模型输入。输入输出最好都是动态地从数据库中获取。其次是从tomcat某个文件下获取。最后本地保存一份副本。
        self.models_input: Dict[str, list] = {}

        # 从模型名称到输出数据结构的映射关系，一个模型可以有多个输出
        self.models_output: Dict[str, list] = {}
        self.update_models()
        self.update_models_endpoint()

    # TODO: 从模型服务中心获取现有模型地址。第一次更新后，每次调用请求失败时触发该请求
    def update_models_endpoint(self) -> None:
        pass

    # TODO: 从模型文件或数据库中更新目前的模型输入输出。第一次调用时更新，后续什么时候更新？
    def update_models(self) -> None:
        pass

    # TODO:使用不确定数量的位置参数和不确定数量的关键字参数调用请求,先实现wps请求
    def process(self, process_name, *args, **kwargs):
        """进行请求
        Args:
            process_name (str): 请求的process字符串

        Returns:
            返回结果，可以返回多个键值对格式结果
        """
        endpoint = self.get_models_endpoint(process_name)
        if endpoint is None:
            raise KeyError(f"发生了一个错误：{process_name} 算子服务不存在！")
        service = Service(endpoint)

        inputs_formats = self.get_models_inputs(process_name)

        # 转换数据类型为输入的格式
        input = process_utils.inputs2request(inputs_formats, args, kwargs)
        # TODO:调用WPS服务,得到results
        results = self.post(endpoint, input)

        # results根据转为对应的返回值，返回给用户
        outputs_formats = self.get_models_outputs(process_name)
        # outputs_formats = request_format.Requestformat("a",["Coverage"])

        output_res = process_utils.response2outputs(outputs_formats, results)

        if len(output_res) == 1:
            return output_res[0]
        else:
            return output_res

    def get_models_inputs(self, process_name) -> request_format.Requestformat:
        # TODO:修改获取模型方法
        return request_format.Requestformat(process_name)

    def get_models_outputs(self, process_name) -> request_format.Requestformat:
        # TODO:修改获取模型方法
        return request_format.Requestformat(process_name)

    # 为空时返回None
    def get_models_endpoint(self, process_name) -> str:
        return ""

    def post(self, endpoint, data) -> list:
        """发送post请求

        Args:
        endpoint: 服务地址
        data(dict): 请求参数
        """
        response = requests.post(
            endpoint,
            data=data,
            headers={"Content-Type": "application/json"},
            timeout=60,
        )
        return json.loads(response.text)[0]["data"]


# 单例对象
requester = Requester()
