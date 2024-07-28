from oge_cores.feature.oge_geometry import OGeometry
from oge_cores.common.ogefiles import FeatureFile
from oge_cores.utils import feature_utils
from oge_cores.feature.feature import *
from osgeo.ogr import Geometry
from osgeo import ogr
from osgeo import osr


def test_polygon_geometry_to_feature():
    """geometry是用户直接使用的，其他的对象都是系统内部隐式完成的"""
    # feature_file = FeatureFile("D:/JAVAprogram/oge-notebook/vector_1700818309513.geojson")
    # geo = OGeometry('point', None, feature_file)
    # 创建坐标系对象
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(4326)  # 使用WGS 84坐标系
    # 创建Polygon几何对象
    polygon = ogr.Geometry(ogr.wkbPolygon)

    # 创建外环
    outer_ring = ogr.Geometry(ogr.wkbLinearRing)
    # 添加外环的点，这里创建一个矩形
    outer_ring.AddPoint(0, 0)  # 左下角
    outer_ring.AddPoint(10, 0)  # 右下角
    outer_ring.AddPoint(10, 10)  # 右上角
    outer_ring.AddPoint(0, 10)  # 左上角
    outer_ring.AddPoint(0, 0)  # 回到起点闭合多边形

    # 将外环添加到多边形
    polygon.AddGeometry(outer_ring)

    # 将坐标系赋给几何对象
    polygon.AssignSpatialReference(spatial_ref)
    # 输出WKT格式的几何对象以验证
    geo = polygon.ExportToWkt()

    print(polygon.GetGeometryType())

    ye = feature_utils.from_geometry(feature_crs=4326, feature_attribute=None, geometry=polygon)

    print(polygon)


def test_point_geometry_to_feature():
    """geometry是用户直接使用的，其他的对象都是系统内部隐式完成的"""
    # feature_file = FeatureFile("D:/JAVAprogram/oge-notebook/vector_1700818309513.geojson")
    # geo = OGeometry('point', None, feature_file)
    # 创建坐标系对象
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(4326)  # 使用WGS 84坐标系
    # 创建Polygon几何对象
    points = ogr.Geometry(ogr.wkbPoint)

    # 添加外环的点，这里创建一个矩形
    points.AddPoint(0, 0)  # 左下角

    # 将坐标系赋给几何对象
    points.AssignSpatialReference(spatial_ref)
    # 输出WKT格式的几何对象以验证
    geo = points.ExportToWkt()
    print(geo)

    print(points.GetGeometryType())

    ye = feature_utils.from_geometry(feature_crs=4326, feature_attribute=None, geometry=points)


def test_line_geometry_to_feature():
    """geometry是用户直接使用的，其他的对象都是系统内部隐式完成的"""
    # 创建坐标系对象
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(4326)  # 使用WGS 84坐标系
    # 创建Polygon几何对象
    line = ogr.Geometry(ogr.wkbLineString)
    # line = ogr.Geometry(ogr.wkbLinearRing)

    line.AddPoint(0, 0)  # 左下角
    line.AddPoint(10, 0)  # 右下角
    # line.AddPoint(0, 0)  # 回到起点闭合多边形

    # 将坐标系赋给几何对象
    line.AssignSpatialReference(spatial_ref)
    # 输出WKT格式的几何对象以验证
    geo = line.ExportToWkt()

    print(line.GetGeometryType())

    ye = feature_utils.from_geometry(feature_crs=4326, feature_attribute=None, geometry=line)

    print(line)


def test_feature_to_geometry():
    """ogemetry是用户直接使用的，其他的对象都是系统内部隐式完成的"""
    feature_file = FeatureFile("D:/JAVAprogram/oge-notebook/test.geojson")
    geo = OGeometry('polygon', None, feature_file)
    fet = Feature(feature_crs=4326, feature_attribute=None, feature_geometry=geo)

    geo_F = feature_utils.to_geometry(fet)
    print(geo_F)


if __name__ == "__main__":
    test_polygon_geometry_to_feature()
    test_feature_to_geometry()

    test_point_geometry_to_feature()
    test_feature_to_geometry()

    test_line_geometry_to_feature()
    test_feature_to_geometry()