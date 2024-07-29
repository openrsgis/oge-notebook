class Requestformat:
    def __init__(
        self,
        request_name,
        format_must_dict: dict = None,
        format_optional_dict: dict = None,
    ) -> None:
        self.request_name = request_name
        self.format_must_dict = format_must_dict  # 必填参数字典，该字典是有序的
        self.format_optional_dict = format_optional_dict  # 可选参数字典，按字典格式输入，该字典是有序的
