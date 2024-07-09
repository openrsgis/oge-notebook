"""OGE文件类"""
from abc import abstractmethod
import os

FOLDERPATH = "./folder"  # TODO:建议从全局变量里获取


# 指向文件位置的指针类
class _FilePointer:
    def __init__(self, file_name) -> None:
        self.__file_path = f"{FOLDERPATH}/{file_name}"


    def get_file(self):
        """获取文件路径

        Returns:
            str: 文件路径
        """
        return self.__file_path

    def set_file_name(self, new_file_name):
        """修改文件名

        Args:
            new_file_name (str): 新文件文件名
        """
        self.__file_path = f"{FOLDERPATH}/{new_file_name}"

    # 调用析构函数删除文件
    def __del__(self):
        if os.path.exists(self.__file_path):
            # os.remove(self.filePath)
            print(f"File {self.__file_path} has been deleted.")

class InternalFile:
    """内部文件类，所有文件类的基类
    """
    def __init__(self, file_name) -> None:
        self.__file_path: _FilePointer = _FilePointer(file_name)

    @abstractmethod
    def read_file(self):
        """文件读取接口，每个文件类都需要实现该接口"""

    def __copy__(self):
        cls = self.__class__
        new_obj = cls.__new__(cls)
        new_obj.__dict__.update(self.__dict__)
        return new_obj

    def get_file_path(self) -> str:
        """获取文件路径

        Returns:
            str: 文件路径
        """
        return self.__file_path.get_file()

    def set_file_name(self, new_file_name: str):
        """修改文件名

        Args:
            new_file_name (str): 新的文件名
        """
        self.__file_path.set_file_name(new_file_name)


class TextFile(InternalFile):
    """文本文件File类"""
    def read_file(self) -> str:
        content = None
        with open(self.get_file_path(), "r", encoding="utf-8") as file:
            content = file.read()

        return content



class CoverageFile(InternalFile):
    """栅格文件类    """
    # TODO: 添加经纬度等元信息接口

    def read_file(self):
        pass


# TODO: 矢量的实现方法
class FeatureFile(InternalFile):
    """矢量文件类"""
    def read_file(self):
        pass
    