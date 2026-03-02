import json
from typing import TextIO
import importlib.resources as res 
from pathlib import Path

class Library():

    # At runtime, this will be populated with declared and included instructions
    working_lib = []

    # Declared ISAs
    core_isas = {}          # These ISAs are supported by default - simply include them to use
    extra_isas = {}         # Extra/custom ISAs must be declared before they can be included for use

    def __init__(self):

        # Declare the core ISAs (within json/ directory)
        for file in res.files("rvasm.json").iterdir():                              # Iterate through every JSON file
            if (file.name.endswith(".json")):
                with file.open("r", encoding="utf-8-sig") as f:
                    json_data = json.load(f)
                    for isa_name, isa_data in json_data.items():                        # Add the ISA data to the dictionary
                        self.core_isas[isa_name] = isa_data

    class LibraryError(Exception):
        def __init__(self, message: str):
            super().__init__(message)

    # Method to declare extra/custom ISA(s) using a JSON file
    def DeclareFromJSONData(self, json_data: json):
        for isa_name, isa_data in json_data.items():    # Iterate through ISAs
            self.extra_isas[isa_name] = isa_data        # and add the data to the dictionary

        # Check for duplicate instructions added to the working library
        seen_instructions = []
        for entry in self.working_lib:
            if (entry["instr"] in seen_instructions):
                raise self.LibraryError(f"Found multiple definitions for the same instruction ({entry['instr']}) when compiling the working library.")
            seen_instructions.append(entry["instr"])

    # Method to update the working library based on a given include list
    def UpdateWorkingLibrary(self, include: list[str]):
        isa_found = False
        for isa_to_include in include:                                      # Iterate through every ISA in the include list
            for collection in (self.core_isas, self.extra_isas):                # Repeat for both core and extra ISA dictionaries
                if (collection.get(isa_to_include)):
                    isa_found = True
                    for instruction in collection.get(isa_to_include):
                        instr_to_add = instruction.copy()
                        self.working_lib.append(instr_to_add)                   # Append the instruction to the working library
            if (not isa_found):
                raise self.LibraryError(f"Could not recognise ISA: {isa_to_include}")
    
    # Method to lookup an instruction from the working library
    def WorkingLibraryLookUp(self, search_term: str):
        for instruction in self.working_lib:
            if (instruction["instr"] == search_term):
                    return instruction