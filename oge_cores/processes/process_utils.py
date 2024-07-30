from oge_cores.processes import request_format
from oge_cores.coverage import Coverage, get_coverage_from_file
from oge_cores.feature.feature import Feature, get_feature_from_file


def parse_input_args(arg_type: str, arg):
    arg_type = arg_type.lower()
    if arg_type == "coverage":
        if isinstance(arg, Coverage) is not True:
            raise TypeError(f"{arg} is {type(arg)}, not Coverage!")
        return arg.file_path

    if arg_type == "feature":
        if isinstance(arg, Feature) is not True:
            raise TypeError(f"{arg} is {type(arg)}, not Feature!")
        return arg.file_path

    if arg_type == "string":
        return str(arg)

    if arg_type == "int":
        return int(arg)

    if arg_type == "float":
        return float(arg)


def parse_output_args(arg_type: str, arg):
    arg_type = arg_type.lower()
    if arg_type == "coverage":
        return get_coverage_from_file(arg)

    if arg_type == "feature":
        return get_feature_from_file(arg)

    if arg_type == "geometry":
        pass

    if arg_type == "string":
        return arg
    
    if arg_type == "int":
        return int(arg)
    
    if arg_type == "float":
        return float(arg)


# TODO:这个解析要做优化，要能处理以args输入和kwargs格式输入的情况
def inputs2request(input_formats: request_format.Requestformat, *args, **kwargs):
    """输入的参数解包为请求的输入格式"""

    res_kwargs = {} # key:名称，value:值

    # 输入key检查
    for key, value in kwargs.items():
        if (
            key not in input_formats.format_must_dict
            and key not in input_formats.format_optional_dict
        ):
            raise RuntimeError( f"输入参数{key}不在该输入函数的参数列表中！请检查输入参数。")
    if len(args) + len(kwargs) > len(input_formats.format_must_dict) + len(
        input_formats.format_optional_dict
    ):
        raise RuntimeError(f"输入参数数量 {len(args) + len(kwargs)} 超过了应该输入的参数数量 {len(input_formats.format_must_dict) + len(input_formats.format_optional_dict)}！")

    format_must_list = list(input_formats.format_must_dict.items())
    # 分两种情况考虑
    if len(args) <= len(format_must_list):
        for i in range(len(args)):
            key, value = format_must_list[i]
            res_kwargs[key] = parse_input_args(value, args[i])

        for i in range(len(args), len(format_must_list)):
            res_kwargs[format_must_list[i][0]] = parse_input_args(
                format_must_list[i][1], kwargs[format_must_list[i][0]]
            )
        if len(res_kwargs) < len(format_must_list):
            raise ValueError(f"输入参数数小于必须输入的参数数！请检查输入参数！")
        for key, value in input_formats.format_optional_dict.items():
            if key in kwargs:
                res_kwargs[key] = parse_input_args(value, kwargs[key])

    elif len(args) > len(format_must_list):
        format_optional_list = list(input_formats.format_optional_dict.items())
        for i in range(len(format_must_list)):
            key, value = format_must_list[i]
            res_kwargs[key] = parse_input_args(value, args[i])
        for i in range(len(format_optional_list)):
            key, value = format_optional_list[i]
            res_kwargs[key] = parse_input_args(value, args[i + len(format_must_list)])

        for key, value in kwargs.items():
            res_kwargs[key] = parse_input_args(
                input_formats.format_optional_dict[key], value
            )

    return res_kwargs


def response2outputs(output_dict: dict) -> dict:
    result_list = []
    status = output_dict["status"]
    if status == "ERROR":
        raise RuntimeError(
            f"{output_dict['name']} 执行中出现错误！错误信息：{output_dict['message']}"
        )
    elif status == "FAILED":
        raise RuntimeError(f"{output_dict['name']} 执行中出现错误！请联系管理员解决。")
    elif status == "SUCCESS":
        output_list = output_dict["result"]
        for item in output_list:
            result_list.append(parse_output_args(item["type"], item["value"]))

    return result_list


def response_output_formats2outputs(
    output_formats: request_format.Requestformat, res_dict: dict
) -> list:
    """返回的结果，解包为对应的数据格式返回"""
    res = []

    if output_formats.format_must_dict is not None:
        if len(res_dict) != len(output_formats.format_must_dict):
            raise TypeError(
                f"算子{output_formats.request_name}输出的参数和需要输出的格式不匹配！请联系管理员检查该算子。"
            )

        for key, value in res_dict.items():
            res.append(parse_output_args(output_formats.format_must_dict[key], value))

    return res


if __name__ == "__main__":
    input_formats = request_format.Requestformat("test", ["Coverage"], None)
    from oge_cores import coverage

    c = coverage.get_coverage_from_file(
        "C:\\Users\\滕宝鑫\\Desktop\\OGE\\oge-notebook\\oge-notebook\\oge_cores\\test\\test_data\\test.tif"
    )

    print(inputs2request(input_formats, c))
