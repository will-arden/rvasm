from pathlib import Path
import json

class Inspector():

    def __init__(self):

        # Inspect all JSON files
        dir = Path(__file__).parent / "json"
        for json_file in dir.glob("*.json"):
            with open(json_file, "r") as f:
                json_data = json.load(f)
                self.InspectJSON(json_data)

    class InspectorError(Exception):
        def __init__(self, message: str):
            super().__init__(message)

    # Method to inspect a JSON file containing ISA information
    def InspectJSON(self, json_data: json):
        
        # Check if any illegal characters are found in the instruction formats
        for extension_name, extension_data in json_data.items():
            for instruction in extension_data:
                for attr, val in instruction.items():
                    match attr:

                        case "instr":
                            legal_chars = ".abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                            if (val == None or val == ""):
                                raise self.InspectorError(f"Empty attribute '{attr}' found in instruction '{instruction['instr']} in extension {extension_name}.'")
                            for c in val:
                                if (c not in legal_chars):
                                    raise self.InspectorError(f"Illegal character '{c}' found in attribute '{attr}' of instruction '{instruction['instr']}' in extension '{extension_name}'.")

                        case "format":
                            legal_chars = " ,()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                            if (val == None or val == ""):
                                raise self.InspectorError(f"Empty attribute '{attr}' found in instruction '{instruction['instr']} in extension {extension_name}.'")
                            for c in val:
                                if (c not in legal_chars):
                                    raise self.InspectorError(f"Illegal character '{c}' found in attribute '{attr}' of instruction '{instruction['instr']}' in extension '{extension_name}'.")

                        case "width":
                            if not (isinstance(val, int)) or (val < 8) or (val % 8 != 0):
                                raise self.InspectorError(f"Illegal width field found for instruction '{instruction['instr']}' in extension '{extension_name}'. Only integers are permitted.")

                        case "encoding":
                            legal_chars = " ,[:]&abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                            if (val == None or val == ""):
                                raise self.InspectorError(f"Empty attribute '{attr}' found in instruction '{instruction['instr']} in extension {extension_name}.'")
                            for c in val:
                                if (c not in legal_chars):
                                    raise self.InspectorError(f"Illegal character '{c}' found in attribute '{attr}' of instruction '{instruction['instr']}' in extension '{extension_name}'.")

                        case "opcode":
                            legal_chars = "01"
                            if (val == None or val == ""):
                                raise self.InspectorError(f"Empty attribute '{attr}' found in instruction '{instruction['instr']} in extension {extension_name}.'")
                            for c in val:
                                if (c not in legal_chars):
                                    raise self.InspectorError(f"Illegal character '{c}' found in attribute '{attr}' of instruction '{instruction['instr']}' in extension '{extension_name}'.")

                        case "funct3":
                            legal_chars = "01"
                            if (val == None or val == ""):
                                continue
                            for c in val:
                                if (c not in legal_chars):
                                    raise self.InspectorError(f"Illegal character '{c}' found in attribute '{attr}' of instruction '{instruction['instr']}' in extension '{extension_name}'.")

                        case "funct7":
                            legal_chars = "01"
                            if (val == None or val == ""):
                                continue
                            for c in val:
                                if (c not in legal_chars):
                                    raise self.InspectorError(f"Illegal character '{c}' found in attribute '{attr}' of instruction '{instruction['instr']}' in extension '{extension_name}'.")

                        
                        # Raise an error for unexpected attributes
                        case _:
                            raise self.InspectorError(f"Unexpected attribute '{attr}' found for {extension_name} instruction {instruction['instr']} in JSON file")