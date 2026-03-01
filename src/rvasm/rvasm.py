import argparse
from typing import TextIO

from .classes.library import Library
from .classes.processor import Processor

def main():

    # Handle arguments
    parser = argparse.ArgumentParser(description="A RISC-V assembler.")
    parser.add_argument("input", help="input file path")
    parser.add_argument("-o", "--output", help="output file path")
    parser.add_argument("-f", "--format", help="output format (binary/hex)")
    args = parser.parse_args()

    rvasm = RVAsm()
    with open(args.input, "r", encoding="utf-8") as f:

        # Placeholder variables to pass to rvasm object
        OUTPUT = None
        OUTPUT_FORMAT = None

        # Overwrite placeholders with any arguments (if present)
        if (args.output):
            OUTPUT = args.output
        if (args.format):
            OUTPUT_FORMAT = args.format
        
        # Go!
        rvasm.Assemble(f, output=OUTPUT, output_format=OUTPUT_FORMAT)

class RVAsm():

    def __init__(self):
        self.library = Library()                        # Create a new Library object
        self.include = ["RV32I"]                        # Include RV32I as a minimum
        self._UpdateWorkingLibrary()                    # Update and compile the working library based on the include list
        self.processor = Processor(self.library)        # Create a Processor object with the shared library
        self.bin = None                                 # Variable to hold the assembled machine code

    class RVAsmError(Exception):
        def __init__(self, message: str):
            super().__init__(message)

    # Method to reset the assembler
    def Reset(self):
        self.processor.Reset()
        self.include = ["RV32I"]
        self._UpdateWorkingLibrary()

    # Method to include an ISA of a particular name for use
    def IncludeISA(self, name):
        if (name in self.include):
            raise self.RVAsmError(f"ISA name can only be included once: ({name})")
        self.include.append(name)
        self._UpdateWorkingLibrary()

    # Method to assemble a .asm file, producing a .dat output
    def Assemble(self, file: TextIO, output=None, output_format=None):

        # Internally set default arguments (easier for argparse)
        if (not output):
            output = "out.dat"
        if (not output_format):
            output_format = "hex"

        self.processor.Reset()                              # Reset the processor (but maintain includes)
        
        for i, line in enumerate(file):                     # Process each line of the .asm file
            self.processor.ProcessLine(line)

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