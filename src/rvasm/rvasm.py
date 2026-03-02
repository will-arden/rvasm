import argparse
import json
from typing import TextIO

from .library import Library
from .processor import Processor

def main():

    # Handle arguments
    parser = argparse.ArgumentParser(description="A Python-based, JSON-driven RISC-V assembler.")
    parser.add_argument("input", help="input file path")
    parser.add_argument("-o", "--output", help="output file path")
    parser.add_argument("-f", "--format", help="output format (binary/hex)")
    parser.add_argument("-i", "--include", nargs="*", help="specify any number of JSON files detailing extra/custom ISA(s)")
    args = parser.parse_args()

    # Create a new RVAsm object per command
    rvasm = RVAsm()

    with open(args.input, "r", encoding="utf-8") as asm_file:

        # Placeholder variables to pass to rvasm object
        OUTPUT = None
        OUTPUT_FORMAT = None
        INCLUDE = None

        # Overwrite placeholders with any arguments (if present)
        if (args.output):
            OUTPUT = args.output
        if (args.format):
            OUTPUT_FORMAT = args.format
        if (args.include):
            INCLUDE = args.include

        # Include ISAs
        if (INCLUDE and len(INCLUDE) > 0):
            for json_path in INCLUDE:
                with open(json_path, "r") as json_file:
                    rvasm.IncludeFromJSON(json_file)
        
        # Go!
        rvasm.Assemble(asm_file, output=OUTPUT, output_format=OUTPUT_FORMAT)

class RVAsm():

    def __init__(self):
        self.library = Library()                                                # Create a new Library object

        self.default_includes = ["RV32I"]                                       # Specify ISAs to include by default
        self.user_includes = []                                                 # Placeholder for user-specified inclusions
        self._UpdateWorkingLibrary(self.default_includes + self.user_includes)  # Update and compile the working library based on the include list

        self.processor = Processor(self.library)                                # Create a Processor object with the shared library
        self.bin = None                                                         # Placeholder for the assembled machine code

    class RVAsmError(Exception):
        def __init__(self, message: str):
            super().__init__(message)

    # Method to assemble a '.asm' file
    def Assemble(self, file: TextIO, output:str=None, output_format:str=None):

        # Internally set default arguments (easier for argparse)
        if (not output):
            output = "out.dat"
        if (not output_format):
            output_format = "hex"

        # Reset the processor
        self.processor.Reset()
        
        # Process each line of the .asm file, catching any exceptions and reporting as debug information
        for i, line in enumerate(file):
            try:
                self.processor.ProcessLine(line)
            except Exception as e:
                print(f"\n{type(e).__name__} caused the following line to fail:")
                print(line.rstrip("\n"))
                print(f"{e}")
                exit()

        self.bin = self.processor.GenerateBinaries()        # Create the machine code
        self._WriteOutput(                                  # Output the file to the current directory
                filename=output,
                output_format=output_format
            )

    # Method to reset the assembler
    def Reset(self):
        self.processor.Reset()
        self.user_includes = []
        self._UpdateWorkingLibrary()

    # Method to include ISA data from a JSON file
    def IncludeFromJSON(self, json_file: TextIO):
        json_data = json.load(json_file)
        self.library.DeclareFromJSONData(json_data)

        # Update the include list
        for isa_name, isa_data in json_data.items():
            if not (isa_name in self.user_includes):
                self._IncludeISA(isa_name)
        
    # Method to include an ISA of a particular name for use
    def _IncludeISA(self, name):
        if not (name in self.user_includes):                                    # Avoid double-inclusions
            self.user_includes.append(name)                                     # Append the name of the ISA to the user includes
        self._UpdateWorkingLibrary(self.default_includes + self.user_includes)  # Update the working library

    # Method to update the working library following changes to the include list
    def _UpdateWorkingLibrary(self, total_include_list: list[str]):
        self.library.UpdateWorkingLibrary(total_include_list)

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
