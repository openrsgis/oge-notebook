"""WPS请求类"""

from typing import Dict


class WpsRequester:
    """用于与算子间的WPS通信请求"""

    # TODO: 从模型服务中心获取现有模型及元信息
    def __init__(self) -> None:
        # 从模型到地址的映射关系
        self.models: Dict[str, str] = Dict()

    # TODO: 从模型服务中心获取现有模型及元信息
    def get_processes(self) -> None:
        pass

    # TODO:使用不确定数量的位置参数和不确定数量的关键字参数调用WPS请求
    def request_WPS(self, process_name, *args, **kwargs):
        pass
