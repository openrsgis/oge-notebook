# Coverage类，包含元信息和image信息
from oge_cores.common import metadata
from oge_cores.coverage import oge_image
from oge_cores.common import ogefiles
from oge_cores.utils import coverage_utils, uuid4


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

    @property
    def metadata(self):
        return self.__metadata

    # 这里实现Coverage获取metadata属性的方法
    @property
    def crs(self):
        """获取图像坐标系"""
        return self.__metadata.crs

    @property
    def geo_transform(self):
        """获取图像范围"""
        return self.__metadata.geo_transform

    @property
    def bands(self):
        """获取图像波段名称"""
        return self.__metadata.bands

    @property
    def bands_num(self):
        """获取图像波段数"""
        return self.__metadata.bands_num

    @property
    def dtype(self):
        return self.__metadata.dtype

    @property
    def cols(self):
        return self.__metadata.cols

    @property
    def rows(self):
        return self.__metadata.rows

    @property
    def file_path(self):
        return self.__image.get_coverage_file().get_file_path()

    def to_numpy_array(self):
        """将图像转为numpy array, (高度, 宽度, 通道数)"""
        np_array = self.__image.to_numpy_array()
        if len(np_array.shape) == 3:
            np_array = np_array.transpose(1, 2, 0)
        return np_array


def get_coverage_file_from_service(product_id: str, coverage_id: str) -> str:
    """从Coverage服务获取文件地址

    Args:
        product_Id (str): 产品名
        coverage_Id (str): 图像名

    Returns:
        产品保存路径
    """
    return ""


def get_coverage(product_id: str, coverage_id: str) -> Coverage:
    """获取图像，以Coverage类的形式返回"""
    # TODO: 请求一次 or 请求两次？
    # TODO: 先不实现lazy加载的功能，等CoverageCollection相关函数完善时予以实现
    file_path = get_coverage_file_from_service(product_id, coverage_id)
    file_metadata = metadata.get_coverage_metadata_from_service(product_id, coverage_id)

    return Coverage(file_metadata, oge_image.Image(file_path))


def get_coverage_from_file(path: str) -> Coverage:
    """从文件构建Coverage对象"""
    coverage_metadata = metadata.get_coverage_metadata_from_file(path)
    image = oge_image.Image(coverage_file_path=path)

    return Coverage(coverage_metadata, image)


def numpy_array_metadata2coverage(
    numpy_array, coverage_metadata: metadata.CoverageMetadata
):
    """将numpy的array，和metadata一并转为Coverage类"""
    file_path = f"./{uuid4.random_uuid()}.tiff"
    coverage_utils.write_img(
        file_path, coverage_metadata.crs, coverage_metadata.geo_transform, numpy_array
    )

    return Coverage(
        coverage_metadata, oge_image.Image(coverage_file_path=file_path, del_able=True)
    )


def numpy_array2coverage(numpy_array, crs: str, geo_transform: tuple):
    """将numpy的array，和crs与geo_transform信息转为Coverage类"""
    file_path = f"./{uuid4.random_uuid()}.tiff"
    coverage_utils.write_img(file_path, crs, geo_transform, numpy_array)

    band_num = 1
    if len(numpy_array.shape) == 3:
        band_num = numpy_array.shape[2]

    return Coverage(
        metadata.CoverageMetadata(
            crs=crs,
            geo_transform=geo_transform,
            bands=[str(i) for i in range(1, 1 + band_num)],
            cols=numpy_array.shape[1],
            rows=numpy_array.shape[0],
            dtype=numpy_array.dtype,
        ),
        oge_image.Image(coverage_file_path=file_path, del_able=True),
    )
