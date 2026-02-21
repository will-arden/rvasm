import re

from classes.Library import Library
from util.exceptions import ASMSyntaxError
from util.exceptions import ASMIncludeError

class Tokeniser():

    def __init__(self, library):
        self.library = library

    def Tokenise(self, line: str):
        library_data = None
        format_string = None
        instr = None

        # Split the instruction into parts
        parts = re.split(r"[,()\s]+", line)                 # Split for whitespace, commas and brackets
        parts = [p.strip() for p in parts if p.strip()]     # Prune separators and useless parts
        instr = parts[0]                                    # Identify the instruction keyword

        # print(f"Parts = {parts}")

        # Firstly, retrieve the data about the instruction from the library
        for include in self.library.GetWorkingLibrary():
            for entry in include:
                if (instr == entry[0]):
                    library_data = entry

        # Throw an error if the instruction can't be found in the working library
        if (library_data == None):
            raise ASMIncludeError("Unknown instruction which cannot be found in the working library.", instr)

        # Retrieve the format string from the library


        # Extract the fields from the instruction

        # Return the tokenised instruction

    def _ObtainFormatString(self, line: str, entry: str):
        return True