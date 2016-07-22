# compiler.py  12/05/2015  D.J.Whale
#
# A very simple high level language compiler
#
# Based on from Aho, Sethi and Ullman "Compilers: Principles, techniques and tools"
# pages 48-78.
#
# This code implements a recursive-descent parser, with 1 character lookahead.
#
# This version does the following:
#   Parses a program provided on stdin
#   (optional interactive mode)
#   generates LMC assembly instructions
#   generates LMC DAT instructions
#   supports an expression grammar only
#   integer numbers, + - brackets ( and )
#   Lines terminated by ;
#
# Example program:
#   1+2;
#   3-1;
#   1+(3-2);
#   (((1+2)+3)+4);
#   (1+2)-(1+1);
#   ^D
#
# The output from this compiler can be fed into the LMC assembler.py
# to generate a program, that can be executed with the LMC simulator.py


import sys
import symtab

def trace(msg):
    pass #print("# " + str(msg))


#===== FRONT END ==============================================================
#----- ERROR HANDLING ---------------------------------------------------------

def error(reason=None):
    """Raise an error message and stop the compiler"""

    errorpos = pos+1
    msg = "error:(" + str(lineno) + "," + str(errorpos) + ")"
    if reason != None:
        msg += ":" + reason
    print(msg)
    print(inbuf)
    print(' ' * errorpos + '^')
    sys.exit()



#----- CHARACTER HELPERS ------------------------------------------------------

def isdigit(ch):
    """Is this character a digit?"""

    if ch >= '0' and ch <= '9':
        return True
    return False


def isalpha(ch):
    """Is this character a letter of any case?"""

    if (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z'):
        return True
    return False


def isalnum(ch):
    """Is this character a digit or a letter of any case?"""

    if isdigit(ch) or isalpha(ch):
        return True
    return False


#----- SCANNER/LEXER ----------------------------------------------------------
#
# Scans through characters in the input stream.
# Strips unwanted whitespace,
# Turns into token numbers with optional values.
#
# tokens:
#   [0-9]+ is a CONST
#   +
#   -
#   (
#   )
#   *
#   /
#   ;
#   a-zA-Z (single character is a variable name, case insensitive)

# Tokens

CONST       = 256
EOLN        = 257
VAR         = 258

def tokname(t):
    """Get the name of this token number"""
    # single character tokens like '+' have their lexical symbol as their name

    if t == CONST:
        return "CONST"
    elif t == EOLN:
        return "EOLN"
    elif t == "VAR":
        return "VAR"
    else:
        return t


# SCANNER STATE

inbuf       = None
lookahead   = None
lineno      = 0
pos         = 0


# Stream management

def get():
    """Get the next character in the input stream"""

    global pos
    if pos >= len(inbuf):
        return None # end of file
    ch = inbuf[pos]
    pos += 1
    #trace("get:" + str(ch))
    return ch


def unget(ch):
    """Put this character back in the input stream"""
    #trace("unget:" + str(ch))
    global pos
    pos -= 1
    if inbuf[pos] != ch:
        raise RuntimeError("Tried to putback wrong char, expected:" + str(inbuf[pos]) + " putback:" + str(ch))


# The actual scanner/lexer

def lexer():
    """The lexical analyser driver that identifies tokens"""

    global lookahead, tokenval, lineno
    while True:
        t = get()
        if t == ' ' or t == '\t':
            pass

        elif t == '\n':
            lineno += 1

        elif isdigit(t):
            tokenval = ord(t) - ord('0')
            t = get()
            while (isdigit(t)):
                tokenval = tokenval*10 + ord(t) - ord('0')
                t = get()
            unget(t)
            #trace("lexer:CONST")
            return CONST

        elif t == None:
            return EOLN

        elif isalpha(t):
            t = t.upper()
            tokenval = t
            return VAR

        else:
            tokenval = None
            #trace("lexer:" + str(t))
            return t


#----- PARSER -----------------------------------------------------------------
#
# Parses a stream of tokens, matches against a grammar.
# Accepts or rejects the program based on whether it fits the grammar or not.


""" GRAMMAR

prog -> expr ; prog
    | empty

expr -> expr + term
    | expr - term
    | term

term -> term * factor
    | term / factor
    | factor

factor -> ( expr )
    | CONST
    | VAR
"""


def expr():
    #trace("expr")
    """Parse an expression"""

    term()
    while True:
        #trace("lookahead:" + str(lookahead))
        if lookahead == '+':
            match('+')
            term()
            emit('+')
        elif lookahead == '-':
            match('-')
            term()
            emit('-')
        else:
            break


def term():
    #trace("term")
    factor()
    while True:
        #trace("lookahead:" + str(lookahead))
        if lookahead == '*':
            match('*')
            factor()
            emit('*')

        elif lookahead == '/':
            match('/')
            factor()
            emit('/')
        else:
            break


def factor():
    #trace("factor")
    #trace("lookahead:" + str(lookahead))
    if lookahead == '(':
        match('(')
        expr()
        match(')')
    elif lookahead == CONST:
        emit(CONST, tokenval)
        match(CONST)
    elif lookahead == VAR:
        emit(VAR, tokenval)
        match(VAR)
    else:
        error("factor:expected factor, got:" + str(lookahead))


def match(t):
    """Match this token"""

    global lookahead

    if lookahead == t:
        #trace("matched:" + str(t))
        lookahead = lexer()
    else:
        error("match:expected " + str(t) + " got:" + str(lookahead))


#----- TEMPORARIES, CONSTANTS, VARIABLES, ABSTRACT MACHINE STACK --------------

# STATE

const_used  = []
var_used    = []
tmp_stack   = []
tmp_used    = {}
stack       = []


# Stack

def poptop():
    """Pop the top item off of the parse stack"""

    top = stack.pop()
    trace("poptop:" + str(top))
    if istmp(top):
        tmp = tmp_stack.pop()
        trace("top popped:" + str(top) + " tmp stack popped:" + str(tmp))
    return top


def pushtmp(tmp):
    """Push a tmp variable on the stack"""

    #Also remember how many times it has been used
    trace("pushtmp:" + str(tmp))
    usetmp(tmp)
    stack.append(maketmp(tmp))
    trace("stack:" + str(stack))


def pushconst(value):
    """push a constant onto the stack, work out it's name first"""

    #If this is a new constant, create a data region for it.
    #If this is an existing constant, just reuse the name.
    trace("pushconst:" + str(value))
    useconst(value)
    stack.append(makeconst(value))
    trace("stack:" + str(stack))


def pushvar(varname):
    """push a variable onto the stack, work out it's name first"""

    #If this is a new variable, create a data region for it.
    #If this is an existing variable, just reuse the name.
    trace("pushvar:" + str(varname))
    usevar(varname)
    stack.append(makevar(varname))
    trace("stack:" + str(stack))


# temporaries (TMP)

def istmp(name):
    """Is this a name of a tmp variable?"""

    return name.startswith("tmp")


def maketmp(name):
    """Make a tmp variable name"""

    return "tmp" + str(name)


def newtmp():
    """Get a usable tmp variable number"""

    tmp = len(tmp_stack)
    tmp_stack.append(tmp)
    return tmp


def usetmp(tmp):
    """Mark this tmp variable as used"""

    trace("#usetmp:" + str(tmp))
    if type(tmp) == str:
        if tmp.startswith("tmp"):
          tmp = int(tmp[3:])

    if not tmp_used.has_key(tmp):
        tmp_used[tmp] = 1
    else:
        tmp_used[tmp] += 1


def unusetmp(tmp):
    """Remove a use of a temporary variable number"""

    #e.g. when the optimiser rewrites or deletes an instruction

    global tmp_used
    trace("#unuse:" + str(tmp))
    if type(tmp) == str:
        if tmp.startswith("tmp"):
            tmp = int(tmp[3:])

    if tmp_used.has_key(tmp):
        tmp_used[tmp] -= 1
        if tmp_used[tmp] == 0:
            del tmp_used[tmp]
            trace("#deleted:" + str(tmp))
            trace("#tmp_used:" + str(tmp_used))


# constants (CONST)

def isconst(name):
    """Is this the name of a const?"""

    return name.startswith("const")


def makeconst(name):
    """Make a constant name"""

    return "const" + str(name)


def useconst(value):
    # Is this a known constant value?

    try:
        const_used.index(value)
    except ValueError:
        const_used.append(value)


# Variables (VARs)

def isvar(name):
    """Is thsi the name of a var?"""

    return name.startswith("var")


def makevar(name):
    """Make a variable name"""

    return "var" + str(name)


def usevar(name):
    # Is this a known variable name?

    try:
        var_used.index(name)
    except ValueError:
        var_used.append(name)



#===== BACK END ===============================================================
#----- EMITTER ----------------------------------------------------------------
#
# Generate code based on the parse stack.

outbuf      = []

def emit(t, tval=None):
    """Emit code for this token"""

    global outbuf
    tac = None

    if t == CONST:
        pushconst(tval)

    elif t == VAR:
        pushvar(tval)

    elif t == '+':
        a = poptop()
        b = poptop()
        tmp = newtmp()
        # Note, a and b are rvalue uses of these items that need counting
        tac = ["ADD", str(a), str(b), maketmp(tmp)]
        pushtmp(tmp)
        if istmp(a): usetmp(a)
        if istmp(b): usetmp(b)

    elif t == '-':
        a = poptop()
        b = poptop()
        tmp = newtmp()
        # Note, a and b are rvalue uses of these items that need counting
        tac = ["SUB", str(b), str(a), maketmp(tmp)]
        pushtmp(tmp)
        if istmp(a): usetmp(a)
        if istmp(b): usetmp(b)

    elif t == '*':
        #temporary, LMC does not have a mult instruction!
        a = poptop()
        b = poptop()
        tmp = newtmp()
        # Note, a and b are rvalue uses of these items that need counting
        tac = ["MUL", str(b), str(a), maketmp(tmp)]
        pushtmp(tmp)
        if istmp(a): usetmp(a)
        if istmp(b): usetmp(b)

    elif t == '/':
        #temporary, LMC does not have a div instruction!
        a = poptop()
        b = poptop()
        tmp = newtmp()
        # Note, a and b are rvalue uses of these items that need counting
        tac = ["DIV", str(b), str(a), maketmp(tmp)]
        pushtmp(tmp)
        if istmp(a): usetmp(a)
        if istmp(b): usetmp(b)

    if tac != None:
        ac = tac_to_ac(tac)
        for c in ac:
            outbuf.append(c)
    #if tac != None:
    #    outbuf.append(tac)


#----- TAC TRANSFORMER --------------------------------------------------------------
#
# Transforms TAC (three address code) into the machine architecture (accumulator code)

def gen_add(op1, op2, res):
    # ADD const0,const1->tmp0 becomes
    #   LDA const0
    #   ADD const1
    #   STA tmp0
    ac = [
        ["LDA", op1],
        ["ADD", op2],
        ["STA", res]
    ]
    return ac


def gen_sub(op1, op2, res):
    # SUB const0, const1->tmp0 becomes
    #   LDA const0
    #   SUB const1
    #   STA tmp0
    ac = [
        ["LDA", op1],
        ["SUB", op2],
        ["STA", res]
    ]
    return ac


def gen_mul(op1, op2, res):
    # There is no multiply instruction in the default LMC processor architecture
    # but we have implemented an extended instruction that does it for us.
    #
    # Note, could also possibly do a jump to a multiply routine,
    # as long as the address of the multiply routine was known.
    # However, this requires us to write the librarian.py and linker.py
    # before we could link in a runtime library.

    # MUL op1, op2->res becomes:
    #   LDA op2
    #   USB
    #   LDA op1
    #   MUL
    #   STA res

    ac = [
        ["LDA", op2],
        ["USB", ""], # USB - use B register in next instruction
        ["LDA", op1],
        ["MUL", ""], # MUL A=B*A
        ["STA", res]
    ]
    return ac


def gen_div(op1, op2, res):
    # There is no divide instruction in the default LMC processor architecture
    # but we have implemented an extended instruction that does it for us.
    #
    # Note, could also possibly do a jump to a divide routine,
    # as long as the address of the multiply routine was known.
    # However, this requires us to write the librarian.py and linker.py
    # before we could link in a runtime library.

    # DIV op1, op2->res becomes:
    #   LDA op2
    #   USB
    #   LDA op1
    #   DIV
    #   STA res

    ac = [
        ["LDA", op2],
        ["USB", ""], # USB - use B register in next instruction
        ["LDA", op1],
        ["DIV", ""], # DIV A=B/A
        ["STA", res]
    ]
    return ac


def tac_to_ac(tac):
    """Translate three-address-code to accumulator-code"""

    # This creates instructions that are compatible with the target architecture
    # which is accumulator based and single operand based.

    # Note this could be written as a rule, in a rule rewrite engine
    # Note this is where we could synthesise lots of things, including
    # inlining shifts and multiply routines from pseudo TAC instructions
    # and the whole tac_to_ac could be done as a rewrite engine.


    operator, op1, op2, res = tac
    if operator == "ADD":
        return gen_add(op1, op2, res)

    elif operator == "SUB":
        return gen_sub(op1, op2, res)

    elif operator == "MUL":
        return gen_mul(op1, op2, res)

    elif operator == "DIV":
        return gen_div(op1, op2, res)

    error("Unknown operator:" + str(operator))


#----- OPTIMISER --------------------------------------------------------------
#
# Remove redundant instructions,
# Remove redundant data

def peephole_redundant_store_load(instrs):
    """Run a peephole optimiser to remove STA name followed by LDA name"""

    # Note this could be implemented as a rule in a rewrite engine instead.
    #trace("on entry:" + str(instrs))
    this_i = 1
    while this_i < len(instrs):
        prev_operator, prev_operand = instrs[this_i-1]
        this_operator, this_operand = instrs[this_i]
        if prev_operator == "STA" and this_operator == "LDA" and this_operand == prev_operand:
            # delete prev and this, they are redundant
            #trace("deleting:" + str(this_i-1) + " " + str(this_i))
            #trace("  " + str(instrs[this_i-1]) + " " + str(instrs[this_i]))
            del instrs[this_i-1]
            del instrs[this_i-1]
            this_i = this_i - 1
            if istmp(prev_operand):
                unusetmp(prev_operand)
            if istmp(this_operand):
                unusetmp(this_operand)
        else:
            this_i += 1

    #trace("on exit:" + str(instrs))


# NOTE: this code could be optimised because operands are swappable with ADD
# but it might be better to do a more determined data flow optimisation pass
# rather than looking for certain patterns.
# alternatively we could use rule rewriting to list match templates and
# rules for rewriting them.

# NOTE: tac_to_ac could be done by a rewrite engine that is rule driven.

#['LDA', 'const4']
#['ADD', 'const3']
#['ADD', 'tmp0']
#['STA', 'tmp0']       ['ADD', 'const5']
#['LDA', 'const5']     xxx
#['ADD', 'tmp0']       xxx



#----- MAIN -------------------------------------------------------------------
#
# Main compiler driver

def main():
    global inbuf, outbuf, pos, tmp_stack, lookahead

    while True:
        try:
            inbuf = raw_input("") # if not isatty don't send prompt, else send prompt (see ark-iotic)
            pos = 0
        except EOFError:
            break

        lookahead = lexer()
        while lookahead != EOLN:
            outbuf = []
            expr()
            match(';')
            final = stack.pop()

            # each subexpression is output at each step
            #TODO: If an assignment statement, don't output the result, squash this.
            #only output an expression if it is not assigned to anything.
            outbuf.append(["LDA", final])
            outbuf.append(["OUT",""])

            # Run an optimisation pass on this code region only
            peephole_redundant_store_load(outbuf)

            # Output all code for this code region
            for i in outbuf:
                opcode, operand = i
                print(opcode + " " + str(operand))
                #print(str(i))

            # empty the tmp stack
            tmp_stack = []

    # Mark the end of the complete program
    print("HLT")


    # Allocate space for constants
    #trace("#" + str(const_used))
    for i in range(len(const_used)):
        value = const_used[i]
        print(makeconst(value) + " DAT " + str(value))

    # Allocate space for temporaries
    #trace("#" + str(tmp_used))
    for t in tmp_used:
        print(maketmp(t) + " DAT")

    # Allocate space for variables
    trace("#" + str(var_used))
    for i in range(len(var_used)):
        name = var_used[i]
        value = 0 # All vars are zero-init
        print(makevar(name) + " DAT " + str(value))


if __name__ == "__main__":
    ## import sys
	## IN_NAME = sys.argv[1] #TODO if -  or not present, use stdin
	## OUT_NAME = sys.argv[2] #TODO if - or not present, use stdout

    main()


# END


