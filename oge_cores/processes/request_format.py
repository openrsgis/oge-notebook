class Requestformat:
    def __init__(
        self,
        request_name,
        format_must_list: list = None,
        format_optional_dict: dict = None,
    ) -> None:
        self.request_name = request_name
        self.format_must_list = format_must_list  # 必填参数列表，按顺序输入
        self.format_optional_dict = format_optional_dict  # 可选参数列表，按字典格式输入
