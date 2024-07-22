"""OGE文件类"""

from abc import abstractmethod
import os

FOLDERPATH = "./folder"  # TODO:建议从全局变量里获取


# 指向文件位置的指针Dict, 单例类
class FilePointerDict:
    """单例类，记录指向文件位置的指针Dict及管理方法"""

    def __init__(self) -> None:
        self.__file_path_dict: dict = {}

    def add_file_reference(self, file_name: str):
        """获取文件路径

        Returns:
            str: 文件路径
        """
        if file_name in self.__file_path_dict:
            self.__file_path_dict[file_name] += 1
        else:
            self.__file_path_dict[file_name] = 1

    def remove_file_reference(self, file_name: str):
        """修改文件名

        Args:
            new_file_name (str): 新文件文件名
        """
        if file_name in self.__file_path_dict:
            self.__file_path_dict[file_name] -= 1
            if self.__file_path_dict[file_name] <= 0:
                self._del_file(file_name)

    # 删除文件
    def _del_file(self, file_name):
        if os.path.exists(file_name):
            # os.remove(self.filePath)
            print(f"File {file_name} has been deleted.")


file_pointer_dict = FilePointerDict()


class InternalFile:
    """内部文件类，所有文件类的基类"""

    def __init__(self, file_name: str) -> None:
        self.__file_path: str = file_name
        file_pointer_dict.add_file_reference(file_name)

    @abstractmethod
    def read_file(self):
        """文件读取接口，每个文件类都需要实现该接口"""

    def __copy__(self):
        file_pointer_dict.add_file_reference(self.__file_path)
        cls = self.__class__
        new_obj = cls.__new__(cls)
        new_obj.__dict__.update(self.__dict__)
        return new_obj

    # 析构函数，移除对该文件的引用
    def __del__(self):
        file_pointer_dict.remove_file_reference(self.__file_path)

    def get_file_path(self) -> str:
        """获取文件路径

        Returns:
            str: 文件路径
        """
        return self.__file_path

    def set_file_name(self, new_file_name: str):
        """修改文件名

        Args:
            new_file_name (str): 新的文件名
        """
        self.__file_path = new_file_name


class TextFile(InternalFile):
    """文本文件File类"""

    def read_file(self) -> str:
        content = None
        with open(self.get_file_path(), "r", encoding="utf-8") as file:
            content = file.read()

        return content


class CoverageFile(InternalFile):
    """栅格文件类"""

    # TODO: 添加经纬度等元信息接口

    def read_file(self):
        pass


# TODO: 矢量的实现方法
class FeatureFile(InternalFile):
    """矢量文件类"""

    def read_file(self):
        pass