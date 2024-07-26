from oge_cores.feature import oge_geometry
from oge_cores.common.ogefiles import FeatureFile
from osgeo import ogr
from oge_cores.feature.feature import Feature
from oge_cores.common import ogefiles
from oge_cores.feature.oge_geometry import OGeometry

def from_geometry(feature_crs, feature_attribute, geometry):
    layer = geometry
    # 指定Shapefile的路径
    shp_path = "D:\JAVAprogram\oge-notebook\path_to_your_shapefile.shp"
    # 获取Shapefile的驱动器
    driver = ogr.GetDriverByName("ESRI Shapefile")

    # 创建新的数据源，即Shapefile文件
    data_source = driver.CreateDataSource(shp_path)

    # 定义图层的几何类型，例如点(wkbPoint)
    layer_name = "NewLayer"
    layer_geom_type = ogr.wkbPoint

    # 创建新的图层，并复制给定的layer的几何类型和属性
    layer_dest = data_source.CreateLayer(layer.GetName(), srs=layer.GetSpatialRef(), geom_type=layer.GetGeomType())

    # 复制layer中的字段
    for field_def in layer.schema:
        field_def_copy = ogr.FieldDefn(field_def.GetName(), field_def.GetType())
        layer_dest.CreateField(field_def_copy)

    # 复制layer中的要素
    layer_def = layer.GetLayerDefn()
    for feature in layer:
        feature_copy = ogr.Feature(layer_def)
        feature_copy.SetFrom(feature)
        layer_dest.CreateFeature(feature_copy)
        feature_copy.Destroy()

    # 保存数据源的更改
    data_source.FlushCache()

    # 关闭数据源
    data_source.Destroy()

    oge_geometry_file = FeatureFile(shp_path)
    ogeometry = OGeometry(geometry_type='point', get_feature_function=None, feature_file=oge_geometry_file)
    feature = Feature(feature_crs=4326, feature_attribute=None, feature_geometry=geometry)
    return feature