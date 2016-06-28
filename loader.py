# loader.py  23/04/2015  D.J.Whale
#
# Load numeric data into memory
# Useful for loading a 'binary' file into the simulator

import io

def load(filename, memory, startaddr=0):
    """Load from a file into memory"""

    f = open(filename, "rt")
    addr = startaddr

    while True:
        instr = io.read(file=f)
        if instr != None:
            memory[addr] = instr
            addr += 1
        else:
            break

    f.close()


def showmem(memory, start=0, end=None):
    """Show a range of a memory region"""

    print("MEMORY:")
    if end == None:
        end = len(memory)
    for addr in range(start, end):
        print(str(addr) + " " + str(memory[addr]))

# END

