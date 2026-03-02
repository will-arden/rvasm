import re

from rvasm.library import Library

class Tokeniser():

    def __init__(self, library):
        self.library = library

    class TokeniserError(Exception):
        def __init__(self, message: str):
            super().__init__(message)

    # Method to tokenise an instruction
    def Tokenise(self, line: str):
        tokenised_instruction = {}
        library_data = None
        instr = None

        # Split the instruction into parts
        parts = re.split(r"[,()\s]+", line)                 # Split for whitespace, commas and brackets
        parts = [p.strip() for p in parts if p.strip()]     # Prune separators and useless parts
        instr = parts[0]                                    # Identify the instruction keyword

        # Firstly, retrieve the data about the instruction from the library
        library_data = self.library.WorkingLibraryLookUp(instr)

        # Throw an error if the instruction can't be found in the working library
        if (library_data == None):
            raise self.TokeniserError(f"Unknown instruction {instr} which cannot be found in the working library.")

        # Retrieve the format string from the library
        if (library_data["format"] == None):
            raise self.TokeniserError(f"Couldn't find the instruction format: {library_data['format']}")

        # Tokenise the format string
        fparts = re.split(r"[,()\s]+", library_data["format"])      # Split for whitespace, commas and brackets
        fparts = [fp.strip() for fp in fparts if fp.strip()]        # Prune separators and useless parts
        
        # Match together each field with the corresponding value in the written instruction
        for i, fp in enumerate(fparts):
            tokenised_instruction[fp] = parts[i].lower()

        return tokenised_instruction
    