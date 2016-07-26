# compiler.py  12/05/2015  D.J.Whale
#
# A very simple high level language compiler
#
# Based on the book: Aho, Sethi and Ullman "Compilers: Principles, techniques and tools", 1986.
# ISBN 0-201-10194-7
# pages 48-78.
#
# This code implements a recursive-descent parser, with 1 character look-ahead.
#
# This version does the following:
#   Parses a program provided on stdin
#   (optional interactive mode)
#   generates LMC assembly instructions
#   generates LMC DAT instructions
#   supports an expression grammar only
#   integer numbers, + - brackets ( and )
#   Lines terminated by ;
#   also supports reading of variables A-Z
#   (TODO, lvalue assignment still needs to be added)
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

def trace(msg):
    pass ##print("# " + str(msg))


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


#----- INPUT STREAM MANAGEMENT ------------------------------------------------

lineno = 0
inbuf  = None
pos    = 0


def get():
    """Get the next character in the input stream"""

    global pos
    if pos >= len(inbuf):
        return EOLN # end of line
    ch = inbuf[pos]
    pos += 1
    return ch


def unget(ch):
    """Put this character back in the input stream"""

    global pos
    pos -= 1
    if inbuf[pos] != ch:
        raise RuntimeError("Tried to putback wrong char, expected:" + str(inbuf[pos]) + " putback:" + str(ch))


def readline():
    """Read a single line of input and return it, or return EOF if no more left"""

    global lineno

    try:
        line = raw_input("") # if not isatty don't send prompt, else send prompt
        lineno += 1
        return line

    except EOFError:
        return EOF


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
EOLN        = '\n' #TODO: Phase this out eventually
VAR         = 258
EOF         = 259

def tokname(token):
    """Get the name of this token number"""

    # single character tokens like '+' have their lexical symbol as their name

    #TODO: This could be improved with a table lookup for token>256??
    if token == CONST:
        return "CONST"
    elif token == EOLN:
        return "EOLN"
    elif token == "VAR":
        return "VAR"
    else:
        return token


# SCANNER STATE

lookahead   = None


# The actual scanner/lexer

def lexer():
    """The lexical analyser driver that identifies tokens"""

    global lookahead, tokenval

    while True:
        token = get()
        if token == ' ' or token == '\t': # or token == '\n' or token == '\r':
            # strip whitespace
            pass

        elif token.isdigit():
            tokenval = ord(token) - ord('0')
            token = get()
            while (token.isdigit()):
                tokenval = tokenval*10 + ord(token) - ord('0')
                token = get()
            unget(token)
            return CONST

        elif token.isalpha():
            tokenval = token.upper()
            return VAR

        else:
            # All other tokens use their ascii representation (e.g. '+' is a '+')
            tokenval = None
            return token


#----- PARSER -----------------------------------------------------------------
#
# Parses a stream of tokens, matches against a grammar.
# Accepts or rejects the program based on whether it fits the grammar or not.

"""Assignment to lvalues will probably add something like this:
prog->expr ; EOLN prog
    | assignment ; EOLN prog
    | empty

assignment->VAR = expr

"""

""" This is the desired grammar to parse:

(Aho, Sethi and Ullman, p70)
Note the addition of EOLN in prog, so that it is easy to process one line at a time.
This is actually a bit spurious as the semicolon marks the end of the expression,
so we might take out the EOLN requirement later and allow expressions to overhang
multiple lines (especially useful if they are large).

start->prog EOF

prog -> expr ; EOLN prog
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


But we want to build a recursive-descent parser, and the above grammar is
left-recursive, which will make the parser loop forever.

So, the following modified grammar is used with left-recursion completely eliminated:
(Aho, Sethi and Ullman, p72) using the technique on p47-48.

A->Aa | Ab | c

translates to:

A->cR
R->aR | bR | empty


prog -> expr ; EOLN prog
    | empty

expr -> term moreterms

moreterms -> + term moreterms
    | - term moreterms
    | empty

term -> factor morefactors

morefactors -> * factor morefactors
    | / factor morefactors
    | empty

factor -> ( expr )
    | CONST
    | VAR


Note 1: moreterms and morefactors are optimised inside term() and factor(),
rather than being separate functions.

Note 2: The compiler driver processes lines at a time, so line breaks inside
expressions are not allowed in this implementation.

Note 3: the '.' character in the comments represents where the predictive parser
thinks it should be at that point in time. This makes it possible to relate the
code back to the grammar.
"""


def expr():
    """Parse an expression"""

    # expr->.term moreterms
    term()

    # expr->term .moreterms
    while True:
        # moreterms->.+ term moreterms
        if lookahead == '+':
            match('+')
            # moreterms->+ .term moreterms
            term()
            emit('+')

        # moreterms->.- term moreterms
        elif lookahead == '-':
            match('-')
            # moreterms->- .term moreterms
            term()
            emit('-')

        # moreterms->.empty
        else:
            break


def term():
    """Parse a term"""

    # term->.factor morefactors
    factor()

    while True:
        # morefactors->.* factor morefactors
        if lookahead == '*':
            match('*')
            # morefactors->* .factor morefactors
            factor()
            emit('*')

        # morefactors->./ factor morefactors
        elif lookahead == '/':
            match('/')
            # morefactors->/ .factor morefactors
            factor()
            emit('/')

        # morefactors->.empty
        else:
            break


def factor():
    """Parse a factor"""

    # factor->.( expr )
    if lookahead == '(':
        match('(')
        # factor->( .expr )
        expr()
        # factor-> ( expr .)
        match(')')

    # factor->.CONST
    elif lookahead == CONST:
        emit(CONST, tokenval)
        match(CONST)

    # factor->.VAR
    elif lookahead == VAR:
        emit(VAR, tokenval)
        match(VAR)

    else:
        error("factor:expected factor, got:" + str(lookahead))


def match(token):
    """Match this token, or fail if it does not match"""

    global lookahead

    if lookahead == token:
        lookahead = lexer()
    else:
        error("match:expected " + str(token) + " got:" + str(lookahead))


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
    ##trace("poptop:" + str(top))
    if istmp(top):
        tmp = tmp_stack.pop()
        ##trace("top popped:" + str(top) + " tmp stack popped:" + str(tmp))
    return top


def pushtmp(tmp):
    """Push a tmp variable on the stack"""

    #Also remember how many times it has been used
    ##trace("pushtmp:" + str(tmp))
    usetmp(tmp)
    stack.append(maketmp(tmp))
    ##trace("stack:" + str(stack))


def pushconst(value):
    """push a constant onto the stack, work out it's name first"""

    #If this is a new constant, create a data region for it.
    #If this is an existing constant, just reuse the name.
    ##trace("pushconst:" + str(value))
    useconst(value)
    stack.append(makeconst(value))
    ##trace("stack:" + str(stack))


def pushvar(varname):
    """push a variable onto the stack, work out it's name first"""

    #If this is a new variable, create a data region for it.
    #If this is an existing variable, just reuse the name.
    ##trace("pushvar:" + str(varname))
    usevar(varname)
    stack.append(makevar(varname))
    ##trace("stack:" + str(stack))


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

    ##trace("usetmp:" + str(tmp))
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
    ##trace("unuse:" + str(tmp))
    if type(tmp) == str:
        if tmp.startswith("tmp"):
            tmp = int(tmp[3:])

    if tmp_used.has_key(tmp):
        tmp_used[tmp] -= 1
        if tmp_used[tmp] == 0:
            del tmp_used[tmp]
            ##trace("deleted:" + str(tmp))
            ##trace("tmp_used:" + str(tmp_used))


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

#----- TAC EMITTER ------------------------------------------------------------
#
# Generate TAC (three address code) based on the parse stack contents.
# TAC is really an instruction set for an ideal abstract machine.
# It is later translated into AC (accumulator code) and into LMC assembly
# instructions in the final emit stage.

outbuf      = []

def emit(token, tval=None):
    """Emit TAC (three address code) for this token"""

    global outbuf
    tac = None

    if token == CONST:
        pushconst(tval)

    elif token == VAR:
        pushvar(tval)

    elif token == '+':
        a = poptop()
        b = poptop()
        tmp = newtmp()
        # Note, a and b are rvalue uses of these items that need counting
        tac = ["ADD", str(a), str(b), maketmp(tmp)]
        pushtmp(tmp)
        if istmp(a): usetmp(a)
        if istmp(b): usetmp(b)

    elif token == '-':
        a = poptop()
        b = poptop()
        tmp = newtmp()
        # Note, a and b are rvalue uses of these items that need counting
        tac = ["SUB", str(b), str(a), maketmp(tmp)]
        pushtmp(tmp)
        if istmp(a): usetmp(a)
        if istmp(b): usetmp(b)

    elif token == '*':
        #LMC does not have a MUL instruction, but our simulator adds one.
        a = poptop()
        b = poptop()
        tmp = newtmp()
        # Note, a and b are rvalue uses of these items that need counting
        tac = ["MUL", str(b), str(a), maketmp(tmp)]
        pushtmp(tmp)
        if istmp(a): usetmp(a)
        if istmp(b): usetmp(b)

    elif token == '/':
        #LMC does not have a DIV instruction, but our simulator adds one.
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

# NOTE: this code could be optimised because operands are swappable with ADD
# but it might be better to do a more determined data flow optimisation pass
# rather than looking for certain patterns.
# alternatively we could use rule rewriting to list match templates and
# rules for rewriting them.

def peephole_redundant_store_load(instrs):
    """Run a peephole optimiser to remove 'STA name' followed by a 'LDA name'"""

    # Note this could be implemented as a rule in a rewrite engine instead.
    ##trace("on entry:" + str(instrs))
    this_i = 1
    while this_i < len(instrs):
        prev_operator, prev_operand = instrs[this_i-1]
        this_operator, this_operand = instrs[this_i]
        if prev_operator == "STA" and this_operator == "LDA" and this_operand == prev_operand:
            # delete prev and this, they are redundant
            ##trace("deleting:" + str(this_i-1) + " " + str(this_i))
            ##trace("  " + str(instrs[this_i-1]) + " " + str(instrs[this_i]))
            del instrs[this_i-1]
            del instrs[this_i-1]
            this_i = this_i - 1
            if istmp(prev_operand):
                unusetmp(prev_operand)
            if istmp(this_operand):
                unusetmp(this_operand)
        else:
            this_i += 1

    ##trace("on exit:" + str(instrs))


#----- FINAL CODE EMITTER -----------------------------------------------------

def generate(instrs, final):
    """Generate code for one expression"""

    # each subexpression is output at each step
    #TODO: If an assignment statement, don't output the result, squash this.
    #only output an expression if it is not assigned to anything.
    instrs.append(["LDA", final])
    instrs.append(["OUT",""])

    # Run an optimisation pass on this code region only
    peephole_redundant_store_load(instrs)

    # Output all code for this code region
    for i in instrs:
        opcode, operand = i
        print(opcode + " " + str(operand))


#----- PROG -------------------------------------------------------------------

def prog():
    """Parse a whole program (list of expressions)"""
    global inbuf, outbuf, pos, tmp_stack, lookahead

    # start->.prog
    while True:
        # READ ANOTHER LINE
        inbuf = readline()
        # prog->.empty
        if inbuf == EOF: break # no more lines left

        # PARSE AND GENERATE CODE FOR THE WHOLE LINE
        lookahead = lexer()
        while lookahead != EOLN:
            # PARSE ONE EXPRESSION
            outbuf = []
            # prog->.expr ; EOLN prog
            expr()
            # prog->expr .; EOLN prog
            match(';')
            final = stack.pop()

            generate(outbuf, final)

            # empty the tmp stack
            tmp_stack = []


#----- MAIN COMPILER DRIVER ---------------------------------------------------

def main():
    # start->.prog EOF
    prog()

    # MARK THE END OF THE COMPLETE PROGRAM
    print("HLT")


    # OUTPUT DATA TABLES AT END

    # Allocate space for constants
    ##trace(str(const_used))
    for i in range(len(const_used)):
        value = const_used[i]
        print(makeconst(value) + " DAT " + str(value))

    # Allocate space for temporaries
    ##trace(str(tmp_used))
    for t in tmp_used:
        print(maketmp(t) + " DAT")

    # Allocate space for variables
    ##trace(str(var_used))
    for i in range(len(var_used)):
        name = var_used[i]
        value = 0 # All vars are zero-init
        print(makevar(name) + " DAT " + str(value))


#----- MODULE ENTRY POINT -----------------------------------------------------

if __name__ == "__main__":
    ## import sys
	## IN_NAME = sys.argv[1] #TODO if -  or not present, use stdin
	## OUT_NAME = sys.argv[2] #TODO if - or not present, use stdout

    main()


# END


