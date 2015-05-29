# loader.py  23/04/2015  D.J.Whale
#
# Load numeric data into memory
# Useful for loading a 'binary' file into the simulator

def load(filename, memory, startaddr=0):
    """Load from a file into memory"""

    f = open(filename, "rt")
    addr = startaddr

    for line in f.readlines():
        line = line.strip()
        if len(line) != 0:
            instr = int(line)
            memory[addr] = instr
            addr += 1

    f.close()


def showmem(memory, start=0, end=None):
    """Show a range of a memory region"""

    print("MEMORY:")
    if end == None:
        end = len(memory)
    for addr in range(start, end):
        print(str(addr) + " " + str(memory[addr]))

# END

