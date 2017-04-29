# decimal.py  21/08/2015  D.J.Whale
#
# Read and write decimal 3 digit unsigned numbers
# with zero padding


DEFAULT_WIDTH = 3

def read(width=None, file=None):
    #print("read")
    """return a decimal number in range 000-999"""
    # default width is 3 characters, but you can ask for wider

    if width == None:
        width = DEFAULT_WIDTH

    if file == None: # stdin, strip blank lines
        #print("stdin")
        while True:
            try:
                try:
                    line = raw_input()
                except:
                    line = input()
            except EOFError:
                #print(" EOF")
                return None # EOF

            line = line.strip() # strip wrapping spaces and newline char
            if len(line) != 0:
                instr = int(line)
                #print(" instr:" + str(instr))
                return instr

    else: # from file, strip blank lines
        #print("file")
        #raise RuntimeError("HERE")
        while True:
            line = file.readline()
            if line == "":
                #print(" EOF")
                return None # EOF
            line = line.strip() # strip wrapping spaces and newline char
            if len(line) != 0:
                instr = int(line)
                #print(" instr:" + str(instr))
                return instr



def write(number, width=None, file=None):
    #print("write: %s %s %s %s" %( str(number) , str(type(number)), str(width), str(type(width))))
    """write a decimal number 000-999 zero padded"""

    if width == None:
        width = DEFAULT_WIDTH

    if file == None: # stdout
        print(str(number).zfill(width))
    else: # to file
        file.write(str(number).zfill(width) + "\n")


# END
