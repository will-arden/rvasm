from rvasm.tokeniser import Tokeniser

class Processor():

    def __init__(self, library):
        self.library = library                  # Shared Library object
        self.instructions = []                  # Store tokenised instructions
        self.labels = []                        # Store labels with a program index
        self.index = 0                          # Program index (program counter / 4)
        self.tokeniser = Tokeniser(library)     # Object responsible for tokenising instructions

    class ProcessorError(Exception):
        def __init__(self, message):
            super().__init__(message)

    # Method to reset the Processor, ready for another file to assemble
    def Reset(self):
        self.instructions = []
        self.labels = []

    # Method to process the next line of the assembly file
    def ProcessLine(self, line: str):

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
        tokens = self.tokeniser.Tokenise(line)

        # Look-up the library data for this instruction
        lib_data = self.library.WorkingLibraryLookUp(tokens["instr"])
        if (lib_data == None):
            raise self.ProcessorError(f"Could not find instruction {tokens['instr']} in the working library.")

        # Iterate through the tokens
        for key, value in tokens.items():

            # No need to check the instruction keyword; this must be correct
            if (key == "instr"):
                continue

            # Ensure any x's are removed from register fields, then convert to an integer between 0-31
            if (key in ("rd", "rs1", "rs2")):
                tokens[key] = tokens[key].replace("x", "")
                tokens[key] = int(tokens[key])
                if (tokens[key] < 0 or tokens[key] > 31):
                    raise self.ProcessorError(f"Register {str(tokens[key])} outside of range 0-31.")
                
                # Convert the now integer register fields into binary strings of the correct length
                tokens[key] = format(tokens[key], "05b")

            # Identify keys which have plain-text values (these might be labels)
            if (value.isalpha()):
                
                # TODO: some specific strings might be mappable to some other function

                # Resolve unknown plain-text values to labels
                for lbl in self.labels:
                    if (lbl["name"] == tokens[key]):
                        tokens[key] = lbl["index"] * int(lib_data["width"] / 8)

            # Convert immediate values to integers (if they are not already)
            if (key == "imm"):
                tokens[key] = int(tokens[key])

        # Finally, increment the index and append the instruction to the list of parsed instructions
        self.index += 1
        print(f"Appending instruction: {tokens}")
        self.instructions.append(tokens)

    # Method to generate the final machine code
    def GenerateBinaries(self):
        machine_code = []

        for row in self.instructions:
            lib_data = self.library.WorkingLibraryLookUp(row["instr"])

            line = None
            opcode = lib_data["opcode"]
            funct3 = lib_data["funct3"]
            funct7 = lib_data["funct7"]
            
            # Pattern is dependent on the instruction type
            match lib_data["encoding"]:

                case "R":
                    line = funct7 + row["rs2"] + row["rs1"] + funct3 + row["rd"] + opcode

                case "I":
                    line = format(row["imm"], "012b") + row["rs1"] + funct3 + row["rd"] + opcode

                case "S":
                    immediate = format(row["imm"], "012b")
                    line = immediate[0:7] + row["rs2"] + row["rs1"] + funct3 + immediate[7:] + opcode

                case "B":
                    immediate = format(row["imm"], "013b")
                    line = immediate[0] + immediate[2:8] + row["rs2"] + row["rs1"] + funct3 + immediate[8:12] + immediate[1] + opcode

                case "U":
                    immediate = format(row["imm"], "032b")
                    line = immediate[:19] + row["rd"] + opcode

                case "J":
                    immediate = format(row["imm"], "032b")
                    line = immediate[:20] + row["rd"] + opcode

                case _:
                    raise self.ProcessorError(f"Could not associate instruction type {lib_data[3]} with a known value!")

            # Check that the length of the instruction matches what is expected
            if (len(line) != lib_data["width"]):
                raise self.ProcessorError("Encountered an unexpected instruction length while generating machine code.")
            
            # Append the line to the list of machine code lines
            machine_code.append(line)
        
        return machine_code
    