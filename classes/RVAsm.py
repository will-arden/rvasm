# Packages
from typing import TextIO

# Local imports
from classes.Library import Library
from classes.Processor import Processor
from util.exceptions import ASMIncludeError

class RVAsm():

    def __init__(self):
        self.library = Library()
        self.include = ["RV32I"]
        self._UpdateWorkingLibrary()
        self.processor = Processor(self.library)

    # Method to update the working library following changes to the include list
    def _UpdateWorkingLibrary(self):
        self.library.UpdateWorkingLibrary(self.include)

    # Method to reset the assembler
    def Reset(self):
        self.processor.Reset()
        self.include = ["RV32I"]
        self._UpdateWorkingLibrary()

    # Method to include an ISA of a particular name for use
    def IncludeISA(self, name):
        if (name in self.include):
            raise ASMIncludeError("ISA name can only be included once.", name)
        self.include.append(name)
        self._UpdateWorkingLibrary()

    # Method to assemble a .asm file, producing a .dat output
    def Assemble(self, file: TextIO):

        # Reset the processor (but maintain includes)
        self.processor.Reset()
        
        # Process each line of the .asm file
        for i, line in enumerate(file):
            self.processor.ProcessLine(line)

        # Second pass to resolve labels
        self.processor.MagicWand()

        # Create the machine code
        self.processor.GenerateMachineCode()

        # Output the file to the current directory
        
