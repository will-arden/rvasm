from Library import Library
from exceptions import ASMSyntaxError

class Tokeniser():

    def __init__(self, library):
        self.library = library

    def Tokenise(self, line: str):
        library_data = None
        format_string = None

        # Firstly, retrieve the data about the instruction from the library
        for entry in self.library.GetWorkingLibrary():
            pass

    def _ObtainFormatString(self, line: str, entry: str):
        return True