from oge_cores.processes import request_format


def inputs2request(inputs, input_formats: request_format.Requestformat) -> list:
    """输入的参数解包为请求的输入格式"""
    if len(inputs) == len(input_formats):
        raise TypeError(
            f"算子{input_formats.request_name}输入的参数和需要输入的格式不匹配！"
        )
    return []


def response2outputs(outputs, output_formats: request_format.Requestformat) -> list:
    """返回的结果，解包为对应的数据格式返回"""
    if len(outputs) == len(output_formats):
        raise TypeError(
            f"算子{output_formats.request_name}输入的参数和需要输入的格式不匹配！"
        )

    return []
