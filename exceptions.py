

class ASMSyntaxError(Exception):
    def __init__(self, message: str, line_num: int, line: str):
        super().__init__(message)
        self.line_num = line_num
        self.line = line

class ASMIncludeError(Exception):
    def __init__(self, message: str, include_name: str):
        super().__init__(message)
        self.include_name = include_name

class ASMDeveloperError(Exception):
    def __init__(self, message: str):
        super().__init__(message)