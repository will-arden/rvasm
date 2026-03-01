from rvasm.classes.tokeniser import Tokeniser

class Processor():

    def __init__(self, library):
        self.library = library                  # Library accessible to all classes
        self.instructions = []                  # Store tokenised instructions
        self.labels = []                        # Store labels with a program index
        self.index = 0                          # Program index (program counter / 4)
        self.line_counter = 0                   # Count of the number of lines processed
        self.tokeniser = Tokeniser(library)     # Object responsible for tokenising instructions

    class ProcessorError(Exception):
        def __init__(self, message):
            super().__init__(message)

    # Method to reset the Processor, ready for another file to assemble
    def Reset(self):
        self.instructions = []
        self.labels = []

    # Method to process the next line of the assembly file
    def ProcessLine(self, line):

        line = line.rstrip()                # Strip the newline character from the line
        line = line.split("#")[0]           # Ignore comments
        line = line.strip()                 # Remove whitespace

        # Ignore empty lines
        if (not line):
            return
        
        # Parse labels
        if (":" in line):
            label_parts = line.split(":")

            if (label_parts[1].rstrip()):
                raise self.ProcessorError(f"Unexpected characters following label declaration: {line}")

            label = {"name": label_parts[0], "index": self.index}
            self.labels.append(label)
            return

        # Tokenise instructions
        instr = self.tokeniser.Tokenise(line)

        # Look-up the library data for this instruction
        lib_data = self.library.WorkingLibraryLookUp(instr["instr"])

        # Iterate through the parts of the tokenised instruction, ensuring they are all in order
        for key, value in instr.items():

            # No need to check the instruction keyword
            if (key == "instr"):
                continue

            # Ensure any x's are removed from register fields, then convert to an integer between 0-31
            if (key in ("rd", "rs1", "rs2")):
                instr[key] = instr[key].replace("x", "")
                instr[key] = int(instr[key])
                if (instr[key] < 0 or instr[key] > 31):
                    raise self.ProcessorError(f"Register {str(instr[key])} outside of range 0-31.")
                
            # Resolve labels
            if ((key == "imm") and (not instr[key].isdigit())):
                for lbl in self.labels:
                    if (lbl["name"] == instr[key]):
                        instr[key] = lbl["index"] * int(lib_data[2] / 8)

            # Convert immediate values to integers (if they are not already)
            if (key == "imm"):
                instr[key] = int(instr[key])

        # When done, increment the index and append the instruction to the list of parsed instructions
        self.index += 1
        self.instructions.append(instr)


    # Method to generate the final machine code
    def GenerateBinaries(self):
        machine_code = []

        for row in self.instructions:
            row_data = self.library.WorkingLibraryLookUp(row["instr"])

            line = None
            opcode = row_data[4]
            funct3 = row_data[5]
            funct7 = row_data[6]
            
            # Pattern is dependent on the instruction type
            match row_data[3]:

                case "R":
                    line = funct7 + format(row["rs2"], "05b") + format(row["rs1"], "05b") + funct3 + format(row["rd"], "05b") + opcode

                case "I":
                    line = format(row["imm"], "012b") + format(row["rs1"], "05b") + funct3 + format(row["rd"], "05b") + opcode

                case "S":
                    immediate = format(row["imm"], "012b")
                    line = immediate[0:7] + format(row["rs2"], "05b") + format(row["rs1"], "05b") + funct3 + immediate[7:] + opcode

                case "B":
                    immediate = format(row["imm"], "013b")
                    line = immediate[0] + immediate[2:8] + format(row["rs2"], "05b") + format(row["rs1"], "05b") + funct3 + immediate[8:12] + immediate[1] + opcode

                case "U":
                    immediate = format(row["imm"], "032b")
                    line = immediate[:19] + format(row["rd"], "05b") + opcode

                case "J":
                    immediate = format(row["imm"], "032b")
                    line = immediate[:20] + format(row["rd"], "05b") + opcode

                case _:
                    raise ASMDeveloperError("Could not associate instruction type with a known value!")

            # Check that the length of the instruction matches what is expected
            if (len(line) != row_data[2]):
                raise self.ProcessorError("Encountered an unexpected instruction length while generating machine code.")
            
            # Append the line to the list of machine code lines
            machine_code.append(line)
        
        return machine_code
    