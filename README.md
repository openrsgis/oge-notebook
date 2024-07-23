# 项目介绍
OGE教育版改造，基于Python3.8开发，主要功能包括：
- 通过WPS服务调用外部算子
- 通过文件和Python内部数据结构转换接口实现数据转换

# 开发者注意事项
为了保证开发过程中协作的顺利进行，请在开发中遵循以下规范：
1. 关于代码风格：参考https://www.runoob.com/w3cnote/google-python-styleguide.html. 着重注意其中的变量命名规范和缩进规范。
2. 关于类型注解：python不强制要求类型注解，但对于OGE内部的函数，**强烈建议显式定义函数参数类型和返回值类型**，以便后续开发工作。
3. 关于注释：所有涉及到用户调用的函数，都要有完整的文档字符串注释。详见https://www.runoob.com/w3cnote/google-python-styleguide.html.
4. 关于代码检查工具：建议在上传前，使用pylint和black进行代码检查。可在vscode和pyCharm中安装对应插件。
5. 关于逻辑抽象：建议不要实现超过70行的函数。如果超过这个长度，尽量将函数内逻辑拆分抽象到不同函数中。
6. 关于私有变量和函数：python不强制要求定义变量和函数的可见性，换言之，python内的所有变量及函数默认都是public的。对于面向用户调用的对象，请将其中不希望用户可见的函数和对象通过双下划线，显式标记为私有。

# 单元测试
使用Pytest进行单元测试。
1. 安装pytest:如果你还没有安装pytest，可以通过pip安装：pip install pytest
2. 在test路径下，编写测试函数：
   测试函数是使用pytest进行单元测试的基本单元。测试函数应该以test_为前缀。例如：
``` python
def test_addition():
    assert 1 + 1 == 2
```
3. 断言:使用assert语句来验证测试结果是否符合预期。
4. 参数化测试:pytest支持参数化测试，允许你使用不同的输入值来测试同一个测试函数：
``` python
import pytest

def test_addition(a, b, expected):
    assert a + b == expected

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (3, 2, 5),
    (-1, -1, -2)
])
def test_addition_parametrized(a, b, expected):
    test_addition(a, b, expected)
```
5. 测试fixtures:
pytest允许你定义fixtures，这些是测试前的准备和测试后的清理工作。例如，你可以设置一个数据库连接或创建一个测试用的文件：
6. 运行测试:
在命令行中，你可以使用pytest命令来运行测试。pytest会自动发现以test_为前缀的函数，并执行它们：
``` bash
pytest
```