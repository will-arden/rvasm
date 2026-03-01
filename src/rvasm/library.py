class Library():

    # At runtime, this will be populated with the included instructions
    include = []
    working_lib = []

    # List of expected instruction formats
    formats = {
        "F0": "instr rd, rs1, rs2",
        "F1": "instr rd, imm",
        "F2": "instr rs1, rs2, imm",
        "F3": "instr rd, rs1, imm",
        "F4": "instr rd, imm(rs1)",
        "F5": "instr rs2, imm(rs1)",
        "F6": "instr"
    }

    # Empty ISAs will be populated with tuples on class initialisation
    # Format: (instr: str, format: str, opcode: str, funct3: str, funct7: str)
    ISAs = {
        "RV32I": []
    }

    def __init__(self):

        # Format: (instr: str, format: str, length (bits): int, type: str, opcode: str, funct3: str, funct7: str)
        self._AddToISA("RV32I", ("lui", "F1", 32, "U", "0110111", None, None))
        self._AddToISA("RV32I", ("auipc", "F1", 32, "U", "0010111", None, None))
        self._AddToISA("RV32I", ("jal", "F1", 32, "J", "1101111", None, None))
        self._AddToISA("RV32I", ("beq", "F2", 32, "B", "1100011", "000", None))
        self._AddToISA("RV32I", ("bne", "F2", 32, "B", "1100011", "001", None))
        self._AddToISA("RV32I", ("blt", "F2", 32, "B", "1100011", "100", None))
        self._AddToISA("RV32I", ("bge", "F2", 32, "B", "1100011", "101", None))
        self._AddToISA("RV32I", ("bltu", "F2", 32, "B", "1100011", "110", None))
        self._AddToISA("RV32I", ("bgeu", "F2", 32, "B", "1100011", "111", None))
        self._AddToISA("RV32I", ("jalr", "F3", 32, "I", "1100111", "000", None))
        self._AddToISA("RV32I", ("lb", "F4", 32, "I", "0000011", "000", None))
        self._AddToISA("RV32I", ("lh", "F4", 32, "I", "0000011", "001", None))
        self._AddToISA("RV32I", ("lw", "F4", 32, "I", "0000011", "010", None))
        self._AddToISA("RV32I", ("lbu", "F4", 32, "I", "0000011", "100", None))
        self._AddToISA("RV32I", ("lhu", "F4", 32, "I", "0000011", "101", None))
        self._AddToISA("RV32I", ("addi", "F3", 32, "I", "0010011", "000", None))
        self._AddToISA("RV32I", ("slti", "F3", 32, "I", "0010011", "010", None))
        self._AddToISA("RV32I", ("sltiu", "F3", 32, "I", "0010011", "011", None))
        self._AddToISA("RV32I", ("xori", "F3", 32, "I", "0010011", "100", None))
        self._AddToISA("RV32I", ("ori", "F3", 32, "I", "0010011", "110", None))
        self._AddToISA("RV32I", ("andi", "F3", 32, "I", "0010011", "111", None))
        self._AddToISA("RV32I", ("sb", "F5", 32, "S", "0100011", "000", None))
        self._AddToISA("RV32I", ("sh", "F5", 32, "S", "0100011", "001", None))
        self._AddToISA("RV32I", ("sw", "F5", 32, "S", "0100011", "010", None))
        self._AddToISA("RV32I", ("slli", "F3", 32, "I", "0010011", "001", "0000000"))
        self._AddToISA("RV32I", ("srli", "F3", 32, "I", "0010011", "101", "0000000"))
        self._AddToISA("RV32I", ("srai", "F3", 32, "I", "0010011", "101", "0100000"))
        self._AddToISA("RV32I", ("add", "F0", 32, "R", "0110011", "000", "0000000"))
        self._AddToISA("RV32I", ("sub", "F0", 32, "R", "0110011", "000", "0100000"))
        self._AddToISA("RV32I", ("sll", "F0", 32, "R", "0110011", "001", "0000000"))
        self._AddToISA("RV32I", ("slt", "F0", 32, "R", "0110011", "010", "0000000"))
        self._AddToISA("RV32I", ("sltu", "F0", 32, "R", "0110011", "011", "0000000"))
        self._AddToISA("RV32I", ("xor", "F0", 32, "R", "0110011", "100", "0000000"))
        self._AddToISA("RV32I", ("srl", "F0", 32, "R", "0110011", "101", "0000000"))
        self._AddToISA("RV32I", ("sra", "F0", 32, "R", "0110011", "101", "0100000"))
        self._AddToISA("RV32I", ("or", "F0", 32, "R", "0110011", "110", "0000000"))
        self._AddToISA("RV32I", ("and", "F0", 32, "R", "0110011", "111", "0000000"))
        self._AddToISA("RV32I", ("fence", "F6", 32, "", "0001111", "000", None))
        self._AddToISA("RV32I", ("ecall", "F6", 32, "", "1110011", "000", None))
        self._AddToISA("RV32I", ("ebreak", "F6", 32, "", "1110011", "000", None))

    class LibraryError(Exception):
        def __init__(self, message: str):
            super().__init__(message)


    # Method to make adding new instructions easy and readable (only intended for use within this class)
    def _AddToISA(self, ISA: str, data: tuple):
        if not (ISA in self.ISAs):
            raise self.LibraryError(f"You can't add an instruction to an ISA ({ISA}) which doesn't exist!")
        self.ISAs[ISA].append(data)

    # Method to compile a working library from the include list
    def _CompileWorkingLibrary(self):
        for i in self.include:
            for isa_name, isa_data in self.ISAs.items():
                if (i == isa_name):
                    self.working_lib.append(isa_data)
        # self.working_lib = {n[0]: n[1:] for n in self.working_lib}

        # Check for duplicate instructions added to the working library
        seen_instructions = []
        for include in self.working_lib:
            for entry in include:
                if (entry[0] in seen_instructions):
                    raise self.LibraryError(f"Found multiple definitions for the same instruction ({entry[0]}) when compiling the working library.")
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
    
    # Method to lookup an instruction from the working library
    def WorkingLibraryLookUp(self, search_term):
        for isa in self.working_lib:
            for entry in isa:
                if (entry[0] == search_term):
                    return entry