# rvasm: A Python-Based RISC-V Assembler
**rvasm** aims to provide a simple and easy-to-use RISC-V assembler, as both a **command-line tool** and a **Python package**. **rvasm** makes it easy to define and use **custom instructions**, simply by providing a JSON file.

## Getting started
You can install **rvasm** using `pip`, as follows:

> `pip install rvasm`

**rvasm** can be used either as a **command-line tool**, or as a **Python package** which can be used in a Python program.

The command-line tool can be used to assemble an RV32I text file, as demonstrated below:
> `rvasm my_file.asm`

This will produce an output file `out.mem`, containing your assembled RV32I in hexadecimal. For help on other command-line options, use:
> `rvasm --help`

Here is an example on how you can use **rvasm** in a Python project:
>```python
>import rvasm
>my_assembler = rvasm.RVAsm()                # Create an Assembler object
>with open("my_input_file.asm", "r") as f:   # Open the assembly file
>    my_assembler.Assemble(f)                # Generate the machine code
>```

## Assembling custom instructions
**rvasm** makes assembling custom instructions straightforward.

Firstly, create a **JSON file** detailing your custom instructions ([use this reference](https://github.com/will-arden/rvasm/tree/main/src/rvasm/json/RV32I.json)). You can specify one or more RISC-V extensions in the same file, or use multiple files. An example would be like so:
> ```json
> {
>     "MY_CUSTOM_EXTENSION": [
>         {
>             "instr": "addi",
>             "format": "instr rd, rs1, imm",
>             "width": 32,
>             "encoding": "imm[11:0] & rs1[4:0] & funct3[2:0] & rd[4:0] & opcode[6:0]",
>             "opcode": "0010011",
>             "funct3": "000",
>             "funct7": null
>         }
>     ]
> }
> ```

To include the new extension(s) from the command line, use the `--include` option, as below:
> `rvasm my_file.asm --include my_custom_extension.json`

The following example shows how you can use **rvasm** to assemble custom RISC-V instructions in your Python code:
> ```python
> import rvasm
> asm = rvasm.RVAsm()
> with open("my_custom_extension.json", "r") as f:
>     asm.IncludeFromJSON(f)
> with open("my_file.asm", "r") as f:
>     asm.Assemble(f)
> ```

This project is a work-in-progress, so please keep checking in! Feel free to create issues and suggest improvements.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
