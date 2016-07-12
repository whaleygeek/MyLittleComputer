# binary.py  21/08/2015  D.J.Whale
#
# Read and write binary data as bytes (8 bit) and words (16 bits)

DEFAULT_WIDTH = 8

def read(width=DEFAULT_WIDTH, file=None):
    """Read a binary number and return as range 0-255 or 0-65535"""
    if file == None:
        v = raw_input()
    else:
        v = file.readline()
    return int(v, 2)


def write(number, width=DEFAULT_WIDTH, file=None):
    """Write a binary number"""
    f = "{0:0%db}" % width
    v = f.format(number)
    if file == None:
        print(v)
    else:
        file.write(v)
        file.write('\n')

# END
