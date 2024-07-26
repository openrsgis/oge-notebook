from oge_cores.feature.oge_geometry import OGeometry
from oge_cores.common.ogefiles import FeatureFile
from oge_cores.utils.feature_utils import from_geometry

def test_feature():
    feature_file = FeatureFile("D:/JAVAprogram/oge-notebook/point.shp")

    geo = OGeometry('point', None, feature_file)
    geo_F = geo.to_geometry()
    ye = from_geometry(feature_crs=4326, feature_attribute=None, geometry=geo_F)
    # geo.AddPoint(1,2)
    print(geo)