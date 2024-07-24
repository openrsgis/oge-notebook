"""Image类，负责图像的lazy加载"""

from oge_cores import ogefiles
from osgeo import ogr


def check_feature(func):
    """修饰器，用于在所有调用函数执行前检查文件是否存在，如果不存在会进行下载

    Args:
        func : 修饰器内函数
    """

    def wrapper(self, *args, **kwargs):
        if self.___file is None:
            if self.__get_feature_function is not None:
                # 下载矢量到featureFile
                self.__feature_file = self.__get_feature_function()
        func(*args, **kwargs)

    return wrapper


class OGeometry(ogr.Geometry):
    """管理矢量的File"""

    def __init__(self, geometry_type: str=None):
        valid_options = ['point', 'line', 'polygon']
        if geometry_type not in valid_options:
            raise ValueError("Invalid geometry_type. Must be one of: 'point', 'line', or 'polygon'.")

        if geometry_type == 'point':
            super().__init__(ogr.wkbPoint)
        elif geometry_type == 'line':
            super().__init__(ogr.wkbLineString)
        elif geometry_type == 'polygon':
            super().__init__(ogr.wkbPolygon)

        self.__type = geometry_type
        # 图像加载回调函数，使用闭包或偏函数的方式传入，在使用文件时调用
        self.__feature_file =  check_feature

        @property
        def type(self):
            """获取矢量类型信息"""
            return self.__type



