"""元信息类"""

from typing import List
from osgeo import gdal
import numpy as np
from oge_cores.common import dtype as dt


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

    # TODO: 需要构建图像数据格式到numpy array数据格式的映射关系
    def __init__(
        self,
        crs: str = None,
        geo_transform: tuple = None,
        bands: List[str] = None,
        cols: int = None,
        rows: int = None,
        dtype=None,
    ) -> None:
        self.__crs: str = crs
        self.__geo_transform: tuple = geo_transform
        self.__bands: List[str] = bands
        self.__cols = cols
        self.__rows = rows
        self.__dtype = dtype

    # TODO:从文件中读取数据并写入到本地变量中,一次性读取所有元信息 Q:有没有这个必要？可以先不实现用到的时候再实现。
    # 所有元信息参数的get方法
    @property
    def crs(self) -> str:
        return self.__crs

    @property
    def geo_transform(self) -> tuple:
        return self.__geo_transform

    @property
    def bands(self) -> List[str]:
        return self.__bands

    @property
    def bands_num(self) -> int:
        return len(self.__bands)

    @property
    def dtype(self):
        return self.__dtype

    @property
    def cols(self):
        return self.__cols

    @property
    def rows(self):
        return self.__rows

    def print_metadata(self):
        print(self.crs)
        print(self.dtype)
        print(self.bands)
        print(self.bands_num)
        print(self.geo_transform)
        print(self.cols)
        print(self.rows)


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
    dataset = None
    try:
        dataset = gdal.Open(path)
    except Exception as e:
        print(f"An error occurred: {e}")

    # 获取投影信息
    geo_transform = dataset.GetGeoTransform()

    # 获取投影坐标系
    projection = dataset.GetProjection()
    crs_1, crs_2 = projection.split('"')[-4].lower(), projection.split('"')[-2]
    crs = f"{crs_1}:{crs_2}"

    # 获取波段数和波段名称
    band_count = dataset.RasterCount
    band_names = []
    for i in range(1, band_count + 1):
        band_names.append(dataset.GetRasterBand(i).GetDescription())

    # 获取图像数据类型
    dtype = dataset.ReadAsArray().dtype

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    del dataset

    return CoverageMetadata(crs, geo_transform, band_names, cols, rows, dtype)

    # band_data_list = []

    # # # 逐个读取每个波段的数据
    # # for i in range(1, band_count+1):
    # #     band = dataset.GetRasterBand(i)
    # #     band_data = band.ReadAsArray()
    # #     band_data_list.append(band_data)

    # # band_data_array = np.array(band_data_list)
