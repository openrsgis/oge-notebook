# Coverage类，包含元信息和image信息
import metadata
import image


class Coverage:
    """Coverage类，包含元信息和image信息"""

    def __init__(self, coverage_metadata=None, coverage_image=None) -> None:
        self.__metadata: metadata.CoverageMetadata = coverage_metadata
        self.image: image.Image = coverage_image

    def set_metadata(self, coverage_metadata: metadata.CoverageMetadata):
        """设置coverage的元信息

        Args:
            coverage_metadata (metadata.CoverageMetadata): 输入的元信息
        """
        self.__metadata: metadata.CoverageMetadata = coverage_metadata

    # 这里实现Coverage处理的基本函数，如坐标系转换、数据类型转换等
    def set_crs(self):
        """设置图像的坐标系"""
        pass

    # 这里实现Coverage获取metadata属性的方法
    def get_crs(self):
        """获取图像坐标系"""
        return self.__metadata.crs
