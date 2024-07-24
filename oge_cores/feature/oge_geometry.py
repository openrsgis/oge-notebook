"""OGeometry类，负责矢量的lazy加载"""

from oge_cores.common import ogefiles
from osgeo import ogr


class OGeometry(ogr.Geometry):
    """管理矢量的File"""

    def __init__(self, geometry_type: str=None, get_feature_function=None, feature_file: ogefiles.FeatureFile = None):
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
        # 矢量加载回调函数，使用闭包或偏函数的方式传入，在使用文件时调用
        self.__get_feature_function = get_feature_function
        self.__feature_file: ogefiles.FeatureFile = feature_file

    @property
    def type(self):
        """获取矢量类型信息"""
        return self.__type
    
    def check_geometry(self):
        """检查图像是否存在，否则会下载图像。所有函数要先调用该函数进行检查。"""
        if self.__feature_file is None:
            if self.__get_feature_function is not None:
                # 下载图像到coverageFile
                self.__feature_file = self.__get_feature_function()
            else:
                raise ValueError(
                    f"发生了一个错误： {self.__feature_file} 不存在且无下载函数！"
                )



