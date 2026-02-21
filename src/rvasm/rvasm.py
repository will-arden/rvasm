# Packages
from typing import TextIO

# Local imports
from .classes.library import Library
from .classes.processor import Processor
from .util.exceptions import ASMIncludeError

class RVAsm():

    def __init__(self):
        self.library = Library()                        # Create a new Library object
        self.include = ["RV32I"]                        # Include RV32I as a minimum
        self._UpdateWorkingLibrary()                    # Update and compile the working library based on the include list
        self.processor = Processor(self.library)        # Create a Processor object with the shared library
        self.bin = None                                 # Variable to hold the assembled machine code

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
    def Assemble(self, file: TextIO, output="out.dat", output_format="hex"):

        self.processor.Reset()                              # Reset the processor (but maintain includes)
        
        for i, line in enumerate(file):                     # Process each line of the .asm file
            self.processor.ProcessLine(line)

        self.processor.MagicWand()                          # Second pass to resolve labels
        self.bin = self.processor.GenerateBinaries()        # Create the machine code
        self._WriteOutput(                                  # Output the file to the current directory
            filename=output,
            output_format=output_format)


    # Method to update the working library following changes to the include list
    def _UpdateWorkingLibrary(self):
        self.library.UpdateWorkingLibrary(self.include)

    # Method to write the to an output file
    def _WriteOutput(self, filename="out.dat", output_format="hex"):
        write_content = self.bin

        with open(filename, "w") as f:
            for line in write_content:

                # If "hex" is selected as the format, convert each line to a hexadecimal number
                if (output_format.lower() == "hex"):
                    line = format(int(line, 2), "0" + str(int(len(line) / 4)) + "x")

                # Write each line to the output file
                f.write(line + "\n")