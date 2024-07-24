from oge_cores.feature.oge_geometry import OGeometry


def test_feature():
    geo = OGeometry('point')
    geo.AddPoint(1,2)
    print(geo)