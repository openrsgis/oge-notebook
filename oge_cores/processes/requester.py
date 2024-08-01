"""process请求类"""

from typing import Dict
from pywps import Service, ComplexInput, LiteralInput
import requests
import json
import sys

from oge_cores.processes import request_format
from oge_cores.processes import process_utils
from oge_cores.config import config


class Requester:
    """用于与算子间的通信请求，单例类，会在引入时更新"""

    # TODO: 从模型服务中心获取现有模型及元信息
    def __init__(self) -> None:
        # 从模型到地址的映射关系
        self._endpoint: str = config.endpoint

        # 从模型名称到输入的映射关系。第一位是进程id，后续是模型输入。输入输出最好都是动态地从数据库中获取。其次是从tomcat某个文件下获取。最后本地保存一份副本。
        self.models_input: Dict[str, list] = {}

        # 从模型名称到输出数据结构的映射关系，一个模型可以有多个输出
        self.models_output: Dict[str, list] = {}
        self.update_models()
        self.update_models_endpoint()
        self.work_dir = config.work_dir  # 工作路径，即临时文件保存路径。脚本可以直接读取本地配置文件，获取配置信息。要不要脚本和临时文件在一个路径下？
        self.id = "id"  # jupyter调用者id

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
            process_name (str): 请求的process名称

        Returns:
            返回结果，可以返回多个键值对格式结果
        """
        endpoint = self.get_endpoint()
        if endpoint is None:
            raise KeyError(f"发生了一个错误：{process_name} 算子服务不存在！")

        inputs_formats = self.get_models_inputs(process_name)

        # 转换数据类型为输入的格式
        input = process_utils.inputs2request(inputs_formats, args, kwargs)
        # TODO:调用WPS服务,得到results
        results = self.post_wps(endpoint, process_name, input)

        # results根据转为对应的返回值，返回给用户
        output_res = process_utils.response2outputs(results)

        if len(output_res) == 1:
            return output_res[0]
        else:
            return output_res

    # 先通过本地json文件读取，后面再通过网络接口获取
    def get_models_inputs(self, process_name) -> request_format.Requestformat:
        # TODO:修改获取模型方法
        with open(
            "C:\\Users\\滕宝鑫\\Desktop\\OGE\\oge-notebook\\oge-notebook\\oge_cores\\test\\test_data\\DecisionTreeClassifier.json",
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)
        input_list = data["inputs"]
        input_must_dict = {}
        input_optional_dict = {}

        for input in input_list:
            if input["optional"] is not True:
                input_must_dict[input["identifier"]] = input["data_type"]
            elif input["optional"] is True:
                input_optional_dict[input["identifier"]] = input["data_type"]
        return request_format.Requestformat(
            process_name, input_must_dict, input_optional_dict
        )

    def get_models_outputs(self, process_name) -> request_format.Requestformat:
        # TODO:修改获取模型方法
        return request_format.Requestformat(process_name)

    # 为空时返回None
    def get_endpoint(self) -> str:
        return self._endpoint

    def post_wps(self, endpoint, process_name, data) -> dict:
        """发送post请求

        Args:
        endpoint: 服务地址
        data(dict): 请求参数
        """
        # 格式转换
        data = data
        input_json = {
            "identifier": process_name,
            "request_from": self.id,
            "host_output_path": self.work_dir,
            "inputs": data,
            "mode": "sync",
        }
        # print(json.dumps(data))
        json_data = json.dumps(input_json)
        print(json_data)
        try:
            response = self.post(endpoint, json_data, 60)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 500:
                print(f"算子调用过程出现内部错误: 502")
            elif err.response.status_code == 502:
                print(f"发生HTTP错误: 502")

            sys.exit(1)
        if response.status_code == 200:
            res = json.loads(response.text)

            if res["status"] == "FAILED":
                raise ValueError(
                    f"{res['identifier']}算子调用时出现错误：{res['message']}"
                )

            if res["status"] == "ERROR":
                raise ValueError(
                    f"{res['identifier']}算子执行过程中出现错误：{res['message']}"
                )

        return json.loads(response.text)

    def post(self, endpoint, data, timeout=60):
        response = requests.post(
            endpoint,
            data=data,
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )
        return response


# 单例对象
requester = Requester()
