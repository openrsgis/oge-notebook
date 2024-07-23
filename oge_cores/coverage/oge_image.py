"""Image类，负责图像的lazy加载"""

from oge_cores.common import ogefiles


class Image:
    """管理图像的File"""

    def __init__(
        self, get_coverage_function=None, coverage_file: ogefiles.CoverageFile = None
    ):
        self.__coverage_file: ogefiles.CoverageFile = coverage_file

        # 图像加载回调函数，使用闭包或偏函数的方式传入，在使用文件时调用
        self.__get_coverage_function = get_coverage_function

    def set_coverage_file(self, new_coverage_file: ogefiles.CoverageFile):
        self.__coverage_file = new_coverage_file

    def set_coverage_function(self, new_coverage_function):
        self.__coverage_file = new_coverage_function

    def check_image(self):
        """检查图像是否存在，否则会下载图像。所有函数要先调用该函数进行检查。"""
        if self.__coverage_file is None:
            if self.__get_coverage_function is not None:
                # 下载图像到coverageFile
                self.__coverage_file = self.__get_coverage_function()
            else:
                raise ValueError(
                    f"发生了一个错误： {self.__coverage_file} 不存在且无下载函数！"
                )

    def to_numpy_array(self):
        """转为np"""
        self.check_image()
        pass
