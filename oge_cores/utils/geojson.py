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
    def add_geometry(self, geometry):
        self.__add(type=geometry['type'], coordinates=geometry["coordinates"])

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
    0: "Unknown",
    1: "Point",
    2: "LineString",
    3: "Polygon",
    4: "MultiPoint",
    5: "MultiLineString",
    6: "MultiPolygon",
    7: "GeometryCollection",
}


# 将Geometry对象转换为GeoJSON
def geometry_to_geojson(geometry):
    if geometry is None:
        return None

    geojson = {
        "type": "Feature",
        "geometry": {
            "type": geometry.GetGeometryType(),
            "coordinates": []
        },
        "properties": {}
    }
    for ring in geometry:
        pass

    # 根据几何类型填充坐标
    if geojson["geometry"]["type"] in ['point']:
        geojson["geometry"]["coordinates"] = [geometry.GetX(), geometry.GetY()]
    elif geojson["geometry"]["type"] in ["Polygon"]:
        # 这里需要根据具体的几何类型进行遍历和转换
        # 示例仅展示点的情况，多边形和线字符串需要相应处理
        geojson["geometry"]["coordinates"] = [
            [ring.X(), ring.Y()] for ring in geometry
        ]

    return geojson


# 将GeoJSON转换为Geometry对象
def geojson_to_geometry(geojson):
    if geojson is None:
        return None
    # 创建坐标系对象
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(4326)  # 使用WGS 84坐标系

    # 创建Polygon几何对象
    polygon = ogr.Geometry(ogr.wkbPolygon)

    # 获取GeoJSON中的坐标
    coordinates = geojson['geometry']['coordinates'][0]  # 外环坐标

    # 添加外环
    outer_ring = ogr.Geometry(ogr.wkbLinearRing)
    for x, y in coordinates:
        outer_ring.AddPoint(x, y)
    outer_ring.AddPoint(coordinates[0][0], coordinates[0][1])  # 闭合外环
    polygon.AddGeometry(outer_ring)

    # 将坐标系赋给几何对象
    polygon.AssignSpatialReference(spatial_ref)

    # 现在polygon对象是一个包含GeoJSON多边形的ogr.Geometry对象
    print(polygon.ExportToWkt())  # 输出WKT格式的几何对象以验证

    # 根据几何类型填充坐标
    if geojson["geometry"]["type"] in ['point']:
        geojson["geometry"]["coordinates"] = [geometry.GetX(), geometry.GetY()]
    elif geojson["geometry"]["type"] in ['multipoint', 'linestring', 'multilinestring']:
        # 这里需要根据具体的几何类型进行遍历和转换
        # 示例仅展示点的情况，多边形和线字符串需要相应处理
        pass

    return geojson