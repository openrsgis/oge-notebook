import json


class GeoJson:
    def __init__(self):
        self.Base = {
            "spatialReference": "",
            "features": [
            ],
            "type": "FeatureCollection",
        }

    # 被打印的方法
    def __str__(self):
        return json.dumps(self.Base)

    # 被迭代的方法
    def __iter__(self):
        return self.Base["features"]

    # 返回元素数量
    def __len__(self):
        return len(self.Base["features"])

    # 保存JSON文件
    def save(self, filename: str):
        with open(filename, mode='w', encoding='utf-8') as f:
            json.dump(self.Base, indent=4, ensure_ascii=False, fp=f)

    # 读取JSON文件
    def read(self, filename: str):
        with open(filename, mode='r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if "spatialReference" in data and data["spatialReference"]:
                    self.Base["spatialReference"] = data["spatialReference"]
                else:
                    self.Base["spatialReference"] = "4326"
                self.Base["features"] = data["features"]
            except:
                print('文件格式不正确，读取失败。')

    # 添加要素，私有方法
    def __add(self, type: str, coordinates: list, properties={}, crs: str="4326"):
        feature = {
            "geometry": {
                "type": type,
                "coordinates": coordinates
            },
            "properties": properties,
            "type": "Feature"
        }
        self.Base['features'].append(feature)
        self.Base['spatialReference'] = crs
    # 添加图形对象
    def add_geometry(self, geometry, properties, crs):
        self.__add(type=geometry['type'], coordinates=geometry["coordinates"], properties=properties, crs=crs)

    # 添加点要素
    def addPoint(self, coordinates: list, properties={}, crs="4326"):
        if len(coordinates) == 2:
            self.__add('Point', coordinates, properties, crs)

    # 添加线要素
    def addLineString(self, coordinates: list, properties={}, crs="4326"):
        if len(coordinates) >= 2:
            self.__add('LineString', coordinates, properties, crs)

    # 添加面要素
    def addPolygon(self, coordinates: list, properties={}, crs="4326"):
        if len(coordinates) >= 3:
            self.__add('Polygon', coordinates, properties, crs)

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
    'UNKNOWN': "Unknown",
    "POINT": "Point",
    "LINESTRING": "LineString",
    "POLYGON": "Polygon",
    4: "multiPoint",
    5: "multiLineString",
    6: "multiPolygon",
    7: "geometryCollection"
}

json_dir = {
    "Unknown": 0,
    "Point": 1,
    "LineString": 2,
    "Polygon": 3,
    "multiPoint": 4,
    "multiLineString": 5,
    "multiPolygon": 6,
    "geometryCollection": 7,
}


# 将Geometry对象转换为GeoJSON
def geometry_to_geojson(geometry, feature_attribute=None, feature_crs=None):
    """
    将geometry对象转为geojson格式
    Args:
        geometry: ogr.Geometry
        feature_attribute:

    Returns:
        data:
        {
            "spatialReference": "",
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
    if feature_crs is None:
        feature_crs = "4326"

    geojson = {
        "type": "Feature",
        "geometry": {
            "type": ogr_dir[geometry.GetGeometryName()],
            "coordinates": []
        }
    }

    # 根据几何类型填充坐标
    if geojson["geometry"]["type"] in ogr_dir['POINT']:
        geojson["geometry"]["coordinates"] = point_2_geojson(geometry)
    elif geojson["geometry"]["type"] in ogr_dir['LINESTRING']:
        geojson["geometry"]["coordinates"] = line_2_geojson(geometry)
    elif geojson["geometry"]["type"] in ogr_dir['POLYGON']:
        geojson["geometry"]["coordinates"] = polygon_2_geojson(geometry)
    else:
        raise TypeError(
            f"Invalid geometry_type. Must be one of: {ogr_dir['POINT']}, {ogr_dir['LINESTRING']}, or {ogr_dir['POLYGON']}.")

    # 检查格式是否匹配
    check_type(geojson["geometry"]["type"], geojson["geometry"]["coordinates"])

    data = GeoJson()
    data.add_geometry(geojson['geometry'], properties=feature_attribute, crs=feature_crs)
    return data


# 将GeoJSON转换为Geometry对象
def geojson_to_geometry(geojson):
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

    # 获取geojson保存对象的类型
    geotype = geojson['geometry']['type']

    # 检查geojson中数据和对应的类型是否一致
    check_type(geotype, geojson["geometry"]["coordinates"])

    # 创建Polygon几何对象,根据几何类型填充坐标
    if geotype in ogr_dir['POINT']:
        geometry = geojson_2_point(geojson["geometry"]["coordinates"])
    elif geotype in ogr_dir["LINESTRING"]:
        geometry = geojson_2_line(geojson["geometry"]["coordinates"])
    elif geotype in ogr_dir["POLYGON"]:
        geometry = geojson_2_polygon(geojson["geometry"]["coordinates"])
    else:
        raise TypeError(
            f"Invalid geometry_type. Must be one of: {ogr_dir['POINT']}, {ogr_dir['LINESTRING']}, or {ogr_dir['POLYGON']}.")

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
            geometry_line.AddPoint(point[0], point[1])
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
    points.AddPoint(point[0], point[1])

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
        line.AddPoint(point[0], point[1])

    return line


def check_type(type, coordinates):
    """检查geojson保存数据的type和保存的type类型是否一致"""
    
    list_num = get_list_depth(coordinates)
    flag = True
    if list_num == 0:
        flag = (type == ogr_dir["POINT"])
    elif list_num == 2:
        flag = (type == ogr_dir["LINESTRING"])
    elif list_num > 3:
        flag = (type == ogr_dir["POLYGON"])
    if not flag:
        raise TypeError("Geometry_type doesn't match coordinates, please check your geojson."
                        "Point must have one point. Line must have two points. Polygon have more than two points")


def get_list_depth(lst):
    if not isinstance(lst, list):  # 如果不是列表，返回0
        return 0
    
    max_depth = 0  # 用于记录最大深度
    for element in lst:
        depth = get_list_depth(element)  # 递归地获取子列表的深度
        max_depth = max(max_depth, depth + 1)  # 更新最大深度
        
    return max_depth