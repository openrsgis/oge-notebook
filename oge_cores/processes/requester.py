"""process请求类"""

from typing import Dict
from pywps import Service, ComplexInput, LiteralInput


class Requester:
    """用于与算子间的通信请求，单例类，会在引入时更新"""

    # TODO: 从模型服务中心获取现有模型及元信息
    def __init__(self) -> None:
        # 从模型到地址的映射关系
        self.models_endpoint: Dict[str, str] = Dict()

        # 从模型名称到输入的映射关系。第一位是进程id，后续是模型输入。输入输出最好都是动态地从数据库中获取。其次是从tomcat某个文件下获取。最后本地保存一份副本。
        self.models_input: Dict[str, list] = Dict()

        # 从模型名称到输出数据结构的映射关系，一个模型可以有多个输出
        self.models_output: Dict[str, list] = Dict()
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

        """ TODO:将 *args根据inputs_formats整理为对应的格式。形如：
        inputs = [
            LiteralInput('input_id', 'input_value', 'input description'),
            # 其他输入...
        ]
        """
        # 调用WPS服务,得到results
        results = None

        # results根据转为对应的返回值，返回给用户
        outputs_formats = self.get_models_outputs(process_name)

        return []

    def get_models_inputs(self, process_name) -> list:
        return []

    def get_models_outputs(self, process_name) -> list:
        return []

    # 为空时返回None
    def get_models_endpoint(self, process_name) -> str:
        return ""


# 单例对象
requester = Requester()
