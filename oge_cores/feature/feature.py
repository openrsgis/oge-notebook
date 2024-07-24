# Feature类，包含属性信息和几何信息
from oge_cores.feature import oge_geometry
from oge_cores.common import ogefiles

class Feature:
    """Feature类，包含几何信息和属性信息"""

    def __init__(self, feature_crs=4326, feature_attribute=None, feature_geometry=None) -> None:
        self.__geometry: oge_geometry.OGeometry = feature_geometry
        self.__attribute: dict = feature_attribute
        self.__crs: int = feature_crs
    def set_geometry(self, feature_geometry: oge_geometry.OGeometry):
        """设置feature的几何信息

        Args:
            feature_geometry (oge_geometry.Geometry): 输入的几何
        """
        self.__geometry: oge_geometry.OGeometry = feature_geometry

    def set_attribute(self, feature_attribute: dict):
        """设置feature的属性信息

        Args:
            feature_attribute (dict): 输入的属性
        """
        self.__attribute: dict = feature_attribute
    
    @property
    def geometry(self):
        """获取矢量几何信息"""
        return self.__geometry
    
    @property
    def attribute(self):
        """获取矢量属性信息"""
        return self.__attribute
    
    @property
    def crs(self):
        """获取矢量坐标系"""
        return self.__crs
    
    def to_geojson(self):
        """转为geojson"""
        pass

    def to_wkt(self):
        """转为wkt"""
        pass
        

def get_feature_file_from_service(product_id: str) -> str:
    """从Feature服务获取文件地址

    Args:
        product_Id (str): 产品名

    Returns:
        产品保存路径
    """
    return ""

def get_feature_attribute_from_service(product_id: str) -> dict:
    """从Feature服务获取属性信息

    Args:
        product_Id (str): 产品名

    Returns:
        产品属性信息
    """
    return {}

def get_feature_crs_from_service(product_id: str) -> int:
    """从Feature服务获取坐标系信息

    Args:
        product_Id (str): 产品名

    Returns:
        产品属性信息
    """
    return int

def get_feature(product_id: str) -> Feature:
    """从Feature服务获取要素对象

    Args:
        product_Id (str): 产品名

    Returns:
        产品属性信息
    """
    file_path = get_feature_file_from_service(product_id)
    file_attribute = get_feature_attribute_from_service(product_id)
    file_crs = get_feature_crs_from_service(product_id)
    
    return Feature(
        file_crs, file_attribute, oge_geometry.OGeometry(feature_file=ogefiles.FeatureFile(file_path))
    )
