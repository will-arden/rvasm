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
        self.instructions.append(tokens)

    # Method to generate the final machine code
    def GenerateBinaries(self):
        machine_code = []

        # Iterate through each instruction
        for line in self.instructions:
            lib_data = self.library.WorkingLibraryLookUp(line["instr"])     # Fetch the relevant library data
            binary = ""                                                     # Placeholder for binarised instruction

            # Iterate through each field of the encoding
            fields = [p.strip() for p in lib_data["encoding"].split("&")]
            for field in fields:

                # Parse fields which use bit-slicing
                if ("[" in field and "]" in field and ":" in field):
                    fname, remainder = field.split("[", 1)                  # Get the name of the field
                    fupper, remainder = remainder.split(":", 1)             # Get the upper bound
                    flower = remainder.split("]")[0]                        # Get the lower bound
                    (fupper, flower) = (int(fupper), int(flower))           # Convert bounds to integers
                    
                    # Try to retrieve the information from the instruction
                    if (line.get(fname.strip()) is not None):
                        fdata = line.get(fname.strip())

                    # Failing that, try to retrieve the information from the library data
                    elif (lib_data.get(fname.strip()) is not None):
                        fdata = lib_data.get(fname.strip())

                    # If the information can't be found, raise an error
                    else:
                        raise self.ProcessorError(f"Couldn't find information about '{fname.strip()}' in the instruction or in the corresponding library data.")

                    # Add the bits to the binary string of the instruction
                    fvalue = format(fdata, "064b") if isinstance(fdata, int) else fdata
                    binary += fvalue[-1 - fupper : len(fvalue) - flower]

                # Parse fields which index single bits
                elif ("[" in field and "]" in field and not ":" in field):
                    fname, remainder = field.split("[", 1)                  # Get the name of the field
                    findex = int(remainder.split("]", 1)[0])                # Get the index of the bit of interest

                    # Try to retrieve the information from the instruction
                    if (line.get(fname.strip()) is not None):
                        fdata = line.get(fname.strip())
                    
                    # Failing that, try to retrieve the information from the library data
                    elif (lib_data.get(fname.strip()) is not None):
                        fdata = lib_data.get(fname.strip())
                    
                    # If the information can't be found, raise an error
                    else:
                        raise self.ProcessorError(f"Couldn't find information about '{fname.strip()}' in the instruction or in the corresponding library data.")
                
                    # Add the bits to the binary string of the instruction
                    fvalue = format(fdata, "064b") if isinstance(fdata, int) else fdata
                    binary += fvalue[-1 - findex]

                # Where no bit-indexing or bit-slicing is required
                elif (not "[" in field and not "]" in field and not ":" in field):
                    if (line.get(field.strip()) is not None):
                        binary += line.get(field.strip())
                    elif (lib_data.get(field.strip()) is not None):
                        binary += lib_data.get(field.strip())
                    else:
                        raise self.ProcessorError(f"Couldn't find information about '{field.strip()}' in the instruction or in the corresponding library data.")
                
                # Encoding could not be interpreted
                else:
                    raise self.ProcessorError(f"Invalid encoding syntax in JSON data: {field}")

            # Check that the length of the generated binary is valid
            if (len(binary) != lib_data.get("width")):
                raise self.ProcessorError(f"Expected the width of the '{lib_data['instr']}' instruction to be {lib_data['width']}; got {len(binary)}.")
            
            # Append the binary instruction to the list of machine code instructions
            machine_code.append(binary)
        
        return machine_code
    