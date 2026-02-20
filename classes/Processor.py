from classes.Tokeniser import Tokeniser
from util.exceptions import ASMSyntaxError

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

        # Parse instructions
        instr = self.tokeniser.Tokenise(line)
        self.instructions.append(instr)

    # Method which iterates over the instructions, replacing labels with actual addresses
    def ResolveLabels(self):
        pass

    # Method to generate the final machine code
    def GenerateMachineCode(self):
        pass