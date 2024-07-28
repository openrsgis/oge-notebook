"""OGeometry类，负责矢量的lazy加载"""

from osgeo import ogr
from oge_cores.common import ogefiles
from oge_cores.utils.geojson import GeoJson
from oge_cores.utils.geojson import geojson_to_geometry

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
        """检查矢量是否存在，否则会下载矢量。所有函数要先调用该函数进行检查。"""
        if self.__feature_file is None:
            if self.__get_feature_function is not None:
                # 下载图像到coverageFile
                self.__feature_file = self.__get_feature_function()
            else:
                raise ValueError(
                    f"发生了一个错误： {self.__feature_file} 不存在且无下载函数！"
                )

    def get_geometry(self):
        """
        加载OGeojson对象中的ogejson文件，读取数据并返回数据中的geometry部分
        Returns: geometry data

        """
        # 指定Shapefile的路径
        if self.__feature_file is None:
            print(f"OGeometry object has no feature_file")
            return None
        file_path = self.__feature_file.get_file_path()
        # shp_path = "path_to_your_shapefile.shp"

        data = GeoJson()
        data.read(file_path)

        if not data.Base['features']:
            print(f"Could not open file {file_path}")
        else:
            # 获取数据源中的第一层，一般一个Shapefile只有一个层
            features = data.Base["features"]
            for feature in features:
                geometry = feature["geometry"]
            return geojson_to_geometry(geometry)


