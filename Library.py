from exceptions import ASMDeveloperError

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
            for key, value in self.ISAs.items():
                if (i == key):
                    self.working_lib.append(value)

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