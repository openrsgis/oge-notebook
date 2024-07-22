# Coverage类，包含元信息和image信息
from oge_cores import metadata
from oge_cores import oge_image
from oge_cores import ogefiles


class Coverage:
    """Coverage类，包含元信息和image信息"""

    def __init__(
        self,
        coverage_metadata: metadata.CoverageMetadata = None,
        coverage_image: oge_image.Image = None,
    ) -> None:
        self.__metadata: metadata.CoverageMetadata = coverage_metadata
        self.__image: oge_image.Image = coverage_image

    def set_metadata(self, coverage_metadata: metadata.CoverageMetadata):
        """设置coverage的元信息

        Args:
            coverage_metadata (metadata.CoverageMetadata): 输入的元信息
        """
        self.__metadata: metadata.CoverageMetadata = coverage_metadata

    # 这里实现Coverage获取metadata属性的方法
    @property
    def crs(self):
        """获取图像坐标系"""
        return self.__metadata.crs

    @property
    def lat(self):
        """获取图像经度"""
        return self.__metadata.lat

    @property
    def lng(self):
        """获取图像纬度"""
        return self.__metadata.lng

    @property
    def extent(self):
        """获取图像范围"""
        return self.__metadata.extent

    @property
    def bands(self):
        """获取图像波段名称"""
        return self.__metadata.bands

    @property
    def bands_num(self):
        """获取图像波段数"""
        return self.__metadata.bands_num

    def to_numpy_array(self):
        """将图像转为numpy array"""
        self.__image.to_numpy_array()


def get_coverage_file_from_service(product_Id: str, coverage_Id: str) -> str:
    """从Coverage服务获取文件地址

    Args:
        product_Id (str): 产品名
        coverage_Id (str): 图像名

    Returns:
        产品保存路径
    """
    return ""


def get_coverage(product_Id: str, coverage_Id: str) -> Coverage:
    # TODO: 请求一次 or 请求两次？
    # TODO: 先不实现lazy加载的功能，等CoverageCollection相关函数完善时予以实现
    file_path = get_coverage_file_from_service(product_Id, coverage_Id)
    file_metadata = metadata.get_coverage_metadata_from_service(product_Id, coverage_Id)

    return Coverage(
        file_metadata, oge_image.Image(coverage_file=ogefiles.CoverageFile(file_path))
    )
