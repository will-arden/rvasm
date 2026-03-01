# rvasm: A Python-Based RISC-V Assembler
**rvasm** aims to provide a simple and easy-to-use RISC-V assembler, as both a **command-line tool** and a **Python package**.

## Getting started
You can install **rvasm** using `pip`, as follows:

> `pip install rvasm`

**rvasm** can be used either as a **command-line tool**, or as a **Python package** which can be used in a Python program.

The command-line tool can be used to assemble an RV32I text file, as demonstrated below:
> `rvasm my_file.asm`

This will produce an output file `out.dat`, containing your assembled RV32I in hexadecimal. For help on other command-line options, use:
> `rvasm --help`

Here is an example on how you can use **rvasm** in a Python project:
>```
>import rvasm
>my_assembler = rvasm.RVAsm()                # Create an Assembler object
>with open("my_input_file.asm", "r") as f:   # Open the assembly file
>    my_assembler.Assemble(f)                # Generate the machine code
>```

## Assembling custom instructions
More is coming on this soon...