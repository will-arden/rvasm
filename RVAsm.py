# Packages
from typing import TextIO

# Local imports
from Processor import Processor

class RVAsm():

    def __init__(self):
        self.Processor = Processor()

    # Method to assemble a .asm file, producing a .dat output
    def Assemble(self, file: TextIO):
        
        # Process each line of the .asm file
        for i, line in enumerate(file):
            print(f"Line {i}: {line}")
