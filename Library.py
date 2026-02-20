from exceptions import ASMDeveloperError
from exceptions import ASMIncludeError

class Library():

    # At runtime, this will be populated with the included instructions
    include = []
    working_lib = []

    # List of expected instruction formats
    formats = {
        "F0": "instr rd, rs1, rs2"
    }

    # Empty ISAs will be populated with tuples on class initialisation
    # Format: (instr: str, format: str, opcode: str, funct3: str, funct7: str)
    ISAs = {
        "RV32I": []
    }

    def __init__(self):

        # Format: (instr: str, format: str, opcode: str, funct3: str, funct7: str)
        self._AddToISA("RV32I", ("addi", "F0", "0010011", "000", None))


    # Method to make adding new instructions easy and readable (only intended for use within this class)
    def _AddToISA(self, ISA: str, data: tuple):
        if not (ISA in self.ISAs):
            raise ASMDeveloperError("You can't add to an ISA which doesn't exist!")
        self.ISAs[ISA].append(data)

    # Method to compile a working library from the include list
    def _CompileWorkingLibrary(self):
        for i in self.include:
            for isa_name, isa_data in self.ISAs.items():
                if (i == isa_name):
                    self.working_lib.append(isa_data)

        # Check for duplicate instructions added to the working library
        seen_instructions = []
        for include in self.working_lib:
            for entry in include:
                if (entry[0] in seen_instructions):
                    raise ASMIncludeError("Found multiple definitions for the same instruction when compiling the working library.", entry[0])
                seen_instructions.append(entry[0])

    # Method to update the working library
    def UpdateWorkingLibrary(self, include: list[str]):
        self.include = include
        self._CompileWorkingLibrary()       # For now, just re-compile everything

    # Method to return the instruction formats
    def GetFormats(self):
        return self.formats
    
    # Method to return the working library
    def GetWorkingLibrary(self):
        return self.working_lib
    
    # Method to return a specific ISA, given its name (e.g. "RV32I")
    def _GetISA(self, name):
        return self.ISAs[name]