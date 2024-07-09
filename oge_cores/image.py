"""Image类，负责图像的lazy加载"""

import ogefiles


class Image:
    """管理图像的File"""

    def __init__(self, get_coverage_function=None, coverage_file=None):
        self.__coverage_file: ogefiles.CoverageFile = coverage_file
        # 图像加载回调函数，使用闭包或偏函数的方式传入，在使用文件时调用
        self.__get_coverage_function = get_coverage_function

    def check_image(self, func):
        """修饰器，用于在所有调用函数执行前检查文件是否存在，如果不存在会进行下载

        Args:
            func : 修饰器内函数
        """

        def wrapper(*args, **kwargs):
            if self.__coverage_file is None:
                if self.__get_coverage_function is not None:
                    # 下载图像到coverageFile
                    self.__coverage_file = self.__get_coverage_function()
            func(*args, **kwargs)

        return wrapper

    @check_image
    def to_numpy_array(self):
        """转为np"""
        pass
