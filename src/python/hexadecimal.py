# hexadecimal.py  21/08/2015  D.J.Whale
#
# Read and write hexadecimal 8 bit (2 char) or 16 bit (4 char) unsigned numbers
# with zero padding

DEFAULT_WIDTH=4

def read(file=None):
    if file == None:
        v = raw_input()
    else:
        v = file.readline()
    return int(v, 16)


def write(number, width=DEFAULT_WIDTH, file=None):
    format = "%%0%dX" % width
    v = format % number
    if file == None:
        print(v)
    else:
        file.write(v)
        file.write('\n')

# END
