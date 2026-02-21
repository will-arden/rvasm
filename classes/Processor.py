from classes.Tokeniser import Tokeniser
from util.exceptions import ASMSyntaxError
from util.exceptions import ASMLogicError

class Processor():

    def __init__(self, library):
        self.library = library                  # Library accessible to all classes
        self.instructions = []                  # Store tokenised instructions
        self.labels = []                        # Store labels with a program index
        self.index = 0                          # Program index (program counter / 4)
        self.line_counter = 0                   # Count of the number of lines processed
        self.tokeniser = Tokeniser(library)     # Object responsible for tokenising instructions

        # TODO: I need a class for crunching the tokenised instructions into machine code

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
                raise ASMSyntaxError("Unexpected characters following label declaration.", self.line_number, line)

            label = {"name": label_parts[0], "index": self.index}
            self.labels.append(label)
            return

        # Parse instructions
        instr = self.tokeniser.Tokenise(line)
        self.index += 1
        self.instructions.append(instr)

    # Method which replaces labels with actual addresses, converts immediates to their proper value, etc.
    def MagicWand(self):
        for row in self.instructions:

            # Look-up the library data for this instruction
            row_data = self.library.WorkingLibraryLookUp(row["instr"])

            for key, value in row.items():

                # Ensure every field is lower-case
                row[key] = row[key].lower()

                # No need to check instruction keyword
                if (key == "instr"):
                    continue

                # Ensure any x's are removed from register fields, then convert to an integer between 0-31
                if (key in ("rd", "rs1", "rs2")):
                    row[key] = row[key].replace("x", "")
                    row[key] = int(row[key])
                    if (row[key] < 0 or row[key] > 31):
                        raise ASMLogicError("Register outside of range 0-31.", str(row[key]))
                    
                # Resolve labels
                if ((key == "imm") and (not row[key].isdigit())):
                    for lbl in self.labels:
                        if (lbl["name"] == row[key]):
                            row[key] = lbl["index"] * int(row_data[2] / 8)


    # Method to generate the final machine code
    def GenerateMachineCode(self):
        pass