# io.py  21/08/2015  D.J.Whale
#
# Handle the input/output streams to a running program.
# This decides how to read and write data to and from a running program,
# or to and from a stored program file.
#
# Depending on the configuration, it can use decimal, binary or hexadecimal
# of any width in characters/bytes. You can also set a default base and width
# that will be used if not supplied.

import decimal
import binary
import hexadecimal

DECIMAL     = 10
BINARY      = 2
HEXADECIMAL = 16

thebase = DECIMAL

def configure(base):
    global thebase
    thebase = base


def read(base=None, width=None, file=None):
    if base == None:
        base = thebase

    if base == DECIMAL:
        return decimal.read(width=width, file=file)
    elif base == BINARY:
        return binary.read(width=width, file=file)
    elif base == HEXADECIMAL:
        return hexadecimal.read(width=width, file=file)
    else:
        raise ValueError("Unsupported base:" + str(base))


def write(number, base=None, width=None, file=None):
    if base == None:
        base = thebase

    if base == DECIMAL:
        decimal.write(number, width=width, file=file)
    elif base == BINARY:
        binary.write(number, width=width, file=file)
    elif base == HEXADECIMAL:
        hexadecimal.write(number, width=width, file=file)
    else:
        raise ValueError("Unsupported base:" + str(base))

#def writeln(number, base=None, width= None, file=file):
#    write(number, base=base, width=width, file=file)
#    if file == None:


# END