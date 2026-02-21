

class ASMSyntaxError(Exception):
    def __init__(self, message: str, line_num: int, line: str):
        super().__init__(message, line_num, line)

class ASMIncludeError(Exception):
    def __init__(self, message: str, include_name: str):
        super().__init__(message, include_name)

class ASMDeveloperError(Exception):
    def __init__(self, message: str):
        super().__init__(message)