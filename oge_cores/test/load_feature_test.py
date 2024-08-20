import sys
sys.path.append("../oge-notebook")
import requests
import json
from oge_cores.utils.geojson import geojson_to_geometry
# 定义URL
url = 'http://192.168.0.5:18085/datasource/vector/get/ByID?productKey=9999'

# 发送GET请求
response = requests.get(url)
# 检查请求是否成功
if response.status_code == 200:
    # 处理响应内容
    data = response.json()  # 如果响应是JSON格式
    json_object = json.loads(data[0])
    print(json_object)
    # geo = geojson_to_geometry(json_object)
    # buff = geo.Buffer(1)
    # print(buff)
# 将Python字典写入到JSON文件
    # with open('output.json', 'w') as json_file:
    #     json.dump(json_object, json_file)
else:
    print(f"请求失败，状态码：{response.status_code}")

