from oge_cores.feature import oge_geometry
from oge_cores.common.ogefiles import FeatureFile
from osgeo import ogr
from oge_cores.feature.feature import Feature
from oge_cores.common import ogefiles
from oge_cores.feature.oge_geometry import OGeometry
from oge_cores.utils.geojson import GeoJson, geometry_to_geojson, geojson_to_geometry
from osgeo.ogr import Geometry
import json


def from_geometry(feature_crs=None, feature_attribute=None, geometry: Geometry = None) -> Feature:
    """
    将Geometry对象转为Feature对象, 同时将Feature对象以geojson格式保存到指定路径下

    Args:
        feature_crs:
        feature_attribute:
        ogeometry:

    Returns:
        Feature
    """
    # 指定保存feature对象的路径
    path = "D:/JAVAprogram/oge-notebook/test.geojson"
    # 将Geometry对象以geojson格式保存到指定路径下
    geojson = geometry_to_geojson(geometry)

    with open('polygon.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=4)

    # 读取geojson文件，将Geometry对象转为Feature对象
    oge_geometry_file = FeatureFile(path)
    ogeometry = OGeometry(geometry_type=geometry.type, get_feature_function=None, feature_file=oge_geometry_file)
    feature = Feature(feature_crs=feature_crs, feature_attribute=feature_attribute, feature_geometry=ogeometry)

    return feature


def to_geometry(feature: Feature):
    """
    加载Feature对象的file路径内的Geometry数据，将Feature对象转为Geometry对象，返回Geometry数据

    Args:
        feature:

    Returns:
        OGeometry
    """
    if feature.geometry is None:
        return None
    # 加载Feature对象包含的OGeometry对象
    ogeometry = feature.geometry

    # 读取OGeometry对象file_path属性包含的Geometry数据
    geometry = ogeometry.get_geometry()

    return geometry
