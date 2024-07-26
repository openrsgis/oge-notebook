"""OGeometry类，负责矢量的lazy加载"""

from osgeo import ogr
from oge_cores.common import ogefiles


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

    def to_geometry(self):
        # 指定Shapefile的路径
        shp_path = self.__feature_file.get_file_path()
        # shp_path = "path_to_your_shapefile.shp"

        # 获取驱动器，这里是Shapefile的驱动器
        driver = ogr.GetDriverByName("ESRI Shapefile")

        # 打开数据源，也就是Shapefile文件
        data_source = driver.Open(shp_path, 0)  # 参数0表示只读模式，1表示读写模式

        if data_source is None:
            print(f"Could not open file {shp_path}")
        else:
            # 获取数据源中的第一层，一般一个Shapefile只有一个层
            layer = data_source.GetLayer()


            # 遍历层中的所有特征
            for feature in layer:
                # 获取特征的属性
                properties = feature.items()
                print(properties)

                # 获取特征的几何形状
                geometry = feature.GetGeometryRef()
                print(geometry)

            # 关闭数据源
            # data_source.Destroy()
            return layer


