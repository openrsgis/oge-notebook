"""元信息类"""

from typing import List


class Metadata:
    """元信息基类"""

    def __init__(self) -> None:
        pass


# TODO：添加分辨率、数据类型等元信息
class CoverageMetadata(Metadata):
    """Coverage元信息类

    Args:
        Metadata (_type_): 基类
    """

    def __init__(
        self,
        crs: str = None,
        lng: float = None,
        lat: float = None,
        extent: List[float] = None,
        bands: List[str] = None,
    ) -> None:
        self.__crs: str = crs
        self.__lng: float = lng
        self.__lat: float = lat
        self.__extent: List[float] = extent
        self.__bands: List[str] = bands

    # TODO:从文件中读取数据并写入到本地变量中,一次性读取所有元信息 Q:有没有这个必要？可以先不实现用到的时候再实现。
    # 所有元信息参数的get方法
    @property
    def crs(self) -> str:
        return self.__crs

    @property
    def lng(self) -> float:
        return self.__lng

    @property
    def lat(self) -> float:
        return self.__lat

    @property
    def extent(self) -> List[float]:
        return self.__extent

    @property
    def bands(self) -> List[str]:
        return self.__bands

    @property
    def bands_num(self) -> int:
        return len(self.__bands)


class FeatureMetadata(Metadata):
    """矢量数据元信息

    Args:
        Metadata (_type_): _description_
    """

    def __init__(self) -> None:
        self.__crs: str = None

    @property
    def crs(self) -> str:
        return self.__crs


def get_coverage_metadata_from_service(
    product_Id: str, coverage_Id: str
) -> CoverageMetadata:
    """从Coverage服务获取元数据

    Args:
        product_Id (str): 产品名
        coverage_Id (str): 图像名

    Returns:
        元数据
    """
    return CoverageMetadata()


def get_coverage_metadata_from_file(path: str) -> CoverageMetadata:
    """从tiff文件中读取元数据

    Args:
        path (str): 文件路径

    Returns:
        元数据
    """
    pass
