# 主要的处理函数
# 调用处理
def process(process_name: str, *args, **kwargs):
    pass


# 获取图像
def getCoverage(coverage_id):
    pass


# 获取CoverageCollection，这个要实现lazy加载，即筛选条件都先放进来的基础上，在真正使用数据时再读取
def get_coverage_collection(product_id):
    pass


# 图像队列，图像在处理过程中不会使用相互之间的信息，这个也要实现lazy加载
def get_coverage_queue(product_id):
    pass


def get_feature_collection(feature_collection_id):
    pass
