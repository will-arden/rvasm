from classes.RVAsm import RVAsm

rvasm = RVAsm()

with open("test.asm", "r", encoding="utf-8") as file:
    rvasm.Assemble(file)