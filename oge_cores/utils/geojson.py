import json


class GeoJson:
    import json
    def __init__(self):
        self.Base = {
            "features": [
            ],
            "type": "FeatureCollection",
        }

    # 被打印的方法
    def __str__(self):
        return self.json.dumps(self.Base)

    # 被迭代的方法
    def __iter__(self):
        return self.Base['features']

    # 返回元素数量
    def __len__(self):
        return len(self.Base["features"])

    # 保存JSON文件
    def save(self, filename: str):
        with open(filename, mode='w', encoding='utf-8') as f:
            self.json.dump(self.Base, indent=4, ensure_ascii=False, fp=f)

    # 读取JSON文件
    def read(self, filename: str):
        with open(filename, mode='r', encoding='utf-8') as f:
            try:
                data = self.json.load(f)
                self.Base['features'] = data['features']
            except:
                print('文件格式不正确，读取失败。')

    # 添加要素，私有方法
    def __add(self, type: str, coordinates: list, properties={}):
        feature = {
            "geometry": {
                "type": type,
                "coordinates": coordinates
            },
            "properties": properties,
            "type": "Feature"
        }
        self.Base['features'].append(feature)

    # 添加图形对象
    def add_geometry(self, geometry, properties):
        self.__add(type=geometry['type'], coordinates=geometry["coordinates"], properties=properties)

    # 添加点要素
    def addPoint(self, coordinates: list, properties={}):
        if len(coordinates) == 2:
            self.__add('Point', coordinates, properties)

    # 添加线要素
    def addLineString(self, coordinates: list, properties={}):
        if len(coordinates) >= 2:
            self.__add('LineString', coordinates, properties)

    # 添加面要素
    def addPolygon(self, coordinates: list, properties={}):
        if len(coordinates) >= 3:
            self.__add('Polygon', coordinates, properties)

    # 合并图层
    def merge(self, another):
        try:
            for item in another:
                self.Base['features'].append(item)
        except:
            print('合并图层失败')


from osgeo import ogr
from osgeo import osr

ogr_dir = {
    'UNKNOWN': "unknown",
    "POINT": "point",
    "LINESTRING": "line",
    "POLYGON": "polygon",
    4: "multiPoint",
    5: "multiLineString",
    6: "multiPolygon",
    7: "geometryCollection"
}

json_dir = {
    "unknown": 0,
    "point": 1,
    "lineString": 2,
    "polygon": 3,
    "multiPoint": 4,
    "multiLineString": 5,
    "multiPolygon": 6,
    "geometryCollection": 7,
}


# 将Geometry对象转换为GeoJSON
def geometry_to_geojson(geometry, feature_attribute=None):
    """
    将geometry对象转为geojson格式
    Args:
        geometry: ogr.Geometry
        feature_attribute:

    Returns:
        data:
        {
            "features": [
                {
                    "geometry": {
                        "type": str,
                        "coordinates": []
                    },
                    "properties": [],
                    "type": "Feature"
                }
            ],
            "type": "FeatureCollection"
        }
    """
    if geometry is None:
        return None
    if feature_attribute is None:
        feature_attribute = []

    geojson = {
        "type": "Feature",
        "geometry": {
            "type": ogr_dir[geometry.GetGeometryName()],
            "coordinates": []
        }
    }

    # 根据几何类型填充坐标
    if geojson["geometry"]["type"] in ['point']:
        geojson["geometry"]["coordinates"] = point_2_geojson(geometry)
    elif geojson["geometry"]["type"] in ["line"]:
        geojson["geometry"]["coordinates"] = line_2_geojson(geometry)
    elif geojson["geometry"]["type"] in ["polygon"]:
        geojson["geometry"]["coordinates"] = polygon_2_geojson(geometry)
    else:
        raise ValueError("Invalid geometry_type. Must be one of: 'point', 'line', or 'polygon'.")

    # 检查格式是否匹配
    check_type(geojson["geometry"]["type"], geojson["geometry"]["coordinates"])

    data = GeoJson()
    data.add_geometry(geojson['geometry'], properties=feature_attribute)
    return data


# 将GeoJSON转换为Geometry对象
def geojson_to_geometry(geojson, feature_crs=4326):
    """
    将geojson格式的geometry数据转为geometry对象
    Args:
        geojson: 格式形如
            {
                "type": "Feature",
                "geometry": {
                    "type": str,
                    "coordinates": []
                }
            }
        feature_crs:
        feature_attribute:

    Returns:
        geometry: ogr.Geometry
    """
    if geojson is None:
        return None
    if not geojson["geometry"]["coordinates"]:
        print("geojson has no coordinates")

    # 创建坐标系对象
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(feature_crs)

    # 获取geojson保存对象的类型
    geotype = geojson['geometry']['type']

    # 检查geojson中数据和对应的类型是否一致
    check_type(geotype, geojson["geometry"]["coordinates"])

    # 创建Polygon几何对象,根据几何类型填充坐标
    if geotype in ['point']:
        geometry = geojson_2_point(geojson["geometry"]["coordinates"])
    elif geotype in ["line"]:
        geometry = geojson_2_line(geojson["geometry"]["coordinates"])
    elif geotype in ["polygon"]:
        geometry = geojson_2_polygon(geojson["geometry"]["coordinates"])
    else:
        raise ValueError("Invalid geometry_type. Must be one of: 'point', 'line', or 'polygon'.")

    # 将坐标系赋给几何对象
    geometry.AssignSpatialReference(spatial_ref)

    # 检查geometry格式是否和geojson中保持一致
    assert geotype == ogr_dir[geometry.GetGeometryName()], "geometry doesn't match the type of original data"

    return geometry


def point_tuple_2_list(point):
    """
    因为geometry读取出来的坐标是元组，而且根据坐标系的不同，点的坐标可能是（x，y）也可能是（x，y，z），
    故采用此函数将其转为json可以保存的列表
    Args:
        point:

    Returns:

    """
    json_str = json.dumps(point)
    return json.loads(json_str)


def polygon_2_geojson(geometry):
    """
    获取polygon类型的geometry所包含的数据
    Args:
        geometry:

    Returns:

    """
    polygon = geometry
    coordinates = []
    ring_len = polygon.GetGeometryCount()
    if ring_len == 0:
        print("geometry has no coordinates")

    # 获取外环
    outer_ring = polygon.GetGeometryRef(0)
    ring = []
    for i in range(outer_ring.GetPointCount()):
        point = outer_ring.GetPoint(i)
        ring.append(point_tuple_2_list(point))
    coordinates.append(ring)

    # 获取内环
    for i in range(1, polygon.GetGeometryCount()):
        inner_ring = polygon.GetGeometryRef(i)
        ring = []
        for j in range(inner_ring.GetPointCount()):
            point = outer_ring.GetPoint(j)
            ring.append(point_tuple_2_list(point))
        coordinates.append(ring)

    return coordinates


def point_2_geojson(geometry):
    """
    获取point类型的geometry所包含的数据
    Args:
        geometry:

    Returns:

    """
    points = geometry
    coordinates = []

    # 获取点
    for i in range(points.GetPointCount()):
        point = points.GetPoint(i)
        for coord in point:
            coordinates.append(coord)

    return coordinates


def line_2_geojson(geometry):
    """
    获取line类型的geometry所包含的数据
    Args:
        geometry:

    Returns:

    """
    line = geometry
    coordinates = []

    # 获取线
    for i in range(line.GetPointCount()):
        point = line.GetPoint(i)
        coordinates.append(point_tuple_2_list(point))

    return coordinates


def geojson_2_polygon(coordinates):
    """
    获取polygon类型的geometry所包含的数据
    Args:
        coordinates:

    Returns:

    """
    # 创建Polygon几何对象
    polygon = ogr.Geometry(ogr.wkbPolygon)

    # 填充面
    for line in coordinates:
        # 创建Polygon几何对象
        geometry_line = ogr.Geometry(ogr.wkbLinearRing)

        for point in line:
            geometry_line.AddPoint(point[0], point[1], point[2])
        polygon.AddGeometry(geometry_line)

    return polygon


def geojson_2_point(coordinates):
    """
    获取point类型的geometry所包含的数据
    Args:
        coordinates:

    Returns:

    """
    # 创建Polygon几何对象
    points = ogr.Geometry(ogr.wkbPoint)

    # 填充点
    point = coordinates
    points.AddPoint(point[0], point[1], point[2])

    return points


def geojson_2_line(coordinates):
    """
    获取line类型的geometry所包含的数据
    Args:
        coordinates:

    Returns:

    """
    # 创建Polygon几何对象
    line = ogr.Geometry(ogr.wkbLineString)

    # 填充线
    for point in coordinates:
        line.AddPoint(point[0], point[1], point[2])

    return line


def check_type(type, coordinates):
    """检查geojson保存数据的type和保存的type类型是否一致"""
    list_num = sum(isinstance(item, list) for item in coordinates)
    flag = True
    if list_num == 0:
        flag = (type == 'point')
    elif list_num == 2:
        flag = (type == 'line')
    elif list_num > 3:
        flag = (type == 'polygon')
    if not flag:
        raise ValueError("Geometry_type doesn't match coordinates, please check your geojson."
                         "Point must have one point. Line must have two points. Polygon have more than two points")
