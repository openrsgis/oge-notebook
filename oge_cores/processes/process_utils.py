from oge_cores.processes import request_format
from oge_cores.coverage import Coverage, get_coverage_from_file


def parse_arguments(arg_type: str, arg):
    if arg_type == "Coverage":
        if isinstance(arg, Coverage) is not True:
            raise TypeError(f"{arg} is {type(arg)}, not Coverage!")
        print(arg.file_path)
        return arg.file_path

    if arg_type == "Feature":
        pass

    if arg_type == "String":
        return str(arg)

    if arg_type == "int":
        return int(arg)

    if arg_type == "float":
        return float(arg)


def parse_output_args(arg_type: str, arg):
    if arg_type == "Coverage":
        return get_coverage_from_file(arg)

    if arg_type == "Feature":
        pass


def inputs2request(input_formats: request_format.Requestformat, *args, **kwargs):
    """输入的参数解包为请求的输入格式"""
    if len(args) != len(input_formats.format_must_list):
        raise TypeError(
            f"算子{input_formats.request_name}输入的参数和需要输入的格式不匹配！"
        )

    res_args = []
    for index, arg in enumerate(args):
        # 参考input_formats.format_list判断其类别
        res_args.append(parse_arguments(input_formats.format_must_list[index], arg))

    res_kwargs = {}

    for key, arg in kwargs:
        if key not in input_formats.format_optional_dict:
            raise TypeError(
                f"算子{input_formats.request_name}的输入参数{key}不存在！请检查输入参数。"
            )
        res_kwargs[key] = parse_arguments(input_formats.format_optional_dict[key], arg)
    return res_args, res_kwargs


def response2outputs(output_formats: request_format.Requestformat, *args) -> list:
    """返回的结果，解包为对应的数据格式返回"""
    if len(args) == len(output_formats.format_must_list):
        raise TypeError(
            f"算子{output_formats.request_name}输出的参数和需要输出的格式不匹配！请联系管理员检查该算子。"
        )

    res = []
    for index, arg in enumerate(args):
        res.append(parse_output_args(output_formats[index], arg))

    return res


if __name__ == "__main__":
    input_formats = request_format.Requestformat("test", ["Coverage"], None)
    from oge_cores import coverage

    c = coverage.get_coverage_from_file(
        "C:\\Users\\滕宝鑫\\Desktop\\OGE\\oge-notebook\\oge-notebook\\oge_cores\\test\\test_data\\test.tif"
    )

    print(inputs2request(input_formats, c))
