import re

from rvasm.classes.library import Library
from rvasm.util.exceptions import ASMSyntaxError
from rvasm.util.exceptions import ASMIncludeError
from rvasm.util.exceptions import ASMDeveloperError

class Tokeniser():

    def __init__(self, library):
        self.library = library

    def Tokenise(self, line: str):
        tokenised_instruction = {}
        library_data = None
        format_string = None
        instr = None

        # Split the instruction into parts
        parts = re.split(r"[,()\s]+", line)                 # Split for whitespace, commas and brackets
        parts = [p.strip() for p in parts if p.strip()]     # Prune separators and useless parts
        instr = parts[0]                                    # Identify the instruction keyword

        # Firstly, retrieve the data about the instruction from the library
        for include in self.library.GetWorkingLibrary():
            for entry in include:
                if (instr == entry[0]):
                    library_data = entry

        # Throw an error if the instruction can't be found in the working library
        if (library_data == None):
            raise ASMIncludeError("Unknown instruction which cannot be found in the working library.", instr)

        # Retrieve the format string from the library
        for format, value in self.library.GetFormats().items():
            if (library_data[1] == format):
                format_string = value
        if (format_string == None):
            raise ASMDeveloperError("Couldn't find an instruction format!", library_data[1])

        # Tokenise the format string
        fparts = re.split(r"[,()\s]+", format_string)           # Split for whitespace, commas and brackets
        fparts = [fp.strip() for fp in fparts if fp.strip()]    # Prune separators and useless parts
        
        # Match together each field with the corresponding value in the written instruction
        for i, fp in enumerate(fparts):
            tokenised_instruction[fp] = parts[i]

        return tokenised_instruction
    