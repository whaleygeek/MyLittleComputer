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
#
# For TODO list, see end of this file.


import sys

def trace(msg):
    pass #print("# " + str(msg))


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

# SCANNER STATE

CONST       = 256
inbuf       = None
lookahead   = None
lineno      = 0
pos         = 0


def tokname(t):
    """Get the name of this token number"""

    if t == CONST:
        return "CONST"
    else:
        return t


def get():
    """Get the next character in the input stream"""

    global pos
    if pos >= len(inbuf):
        return None
    ch = inbuf[pos]
    pos += 1
    return ch


def unget(ch):
    """Put this character back in the input stream"""

    global pos, lookahead
    pos -= 1
    lookahead = ch


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
            return CONST
        else:
            tokenval = None
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

//term -> term * factor
//    | term / factor
//    | factor


//factor -> ( expr )
//    | CONST

term -> ( expr )
    | CONST

"""
def expr():
    """Parse an expression"""

    term()
    while True:
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


#def term():
#    factor()
#    while True:
#        if lookahead == '*':
#            match('*')
#            factor()
#            emit('*')
#
#        elif lookahead == '/':
#            match('/')
#            factor()
#            emit('/')
#        else:
#            break

def term():
    """Parse a term"""

    if lookahead == '(':
        match('(')
        expr()
        match(')')
    elif lookahead == CONST:
        emit(CONST, tokenval)
        match(CONST)
    else:
        error("expected term, got:" + str(lookahead))


#def factor():
#    if lookahead == '(':
#        match('(')
#        expr()
#        match(')')
#    elif lookahead == CONST:
#        emit(CONST, tokenval)
#        match(CONST)
#    else:
#        error("expected factor, got:" + str(lookahead))


def match(t):
    """Match this token"""

    global lookahead

    if lookahead == t:
        lookahead = lexer()
    else:
        error("expected " + str(t) + " got:" + str(lookahead))


#----- EMITTER ----------------------------------------------------------------
#
# Generate code based on the parse tree.

# STATE

const_used  = []
tmp_stack   = []
used_tmp    = {}
stack       = []
outbuf      = []


def maketmp(name):
    """Make a tmp variable name"""

    return "tmp" + str(name)


def makeconst(name):
    """Make a constant name"""

    return "const" + str(name)


def pushconst(value):
    """push a constant onto the stack, work out it's name first"""

    #If this is a new constant, create a data region for it.
    #If this is an existing constant, just reuse the name.
    trace("pushconst:" + str(value))
    useconst(value)
    stack.append(makeconst(value))
    trace("stack:" + str(stack))


def pushtmp(tmp):
    """Push a tmp variable on the stack"""

    #Also remember how many times it has been used
    trace("pushtmp:" + str(tmp))
    usetmp(tmp)
    stack.append(maketmp(tmp))
    trace("stack:" + str(stack))


def istmp(name):
    """Is this a name of a tmp variable?"""

    return name.startswith("tmp")


def isconst(name):
    """Is this the name of a const?"""

    return name.startswith("const")


def newtmp():
    """Get a usable tmp variable number"""

    tmp = len(tmp_stack)
    tmp_stack.append(tmp)
    return tmp


def useconst(value):
    # Is this a known constant value?

    try:
        const_used.index(value)
    except ValueError:
        const_used.append(value)


def usetmp(tmp):
    """Mark this tmp variable as used"""

    trace("#usetmp:" + str(tmp))
    if type(tmp) == str:
        if tmp.startswith("tmp"):
          tmp = int(tmp[3:])

    if not used_tmp.has_key(tmp):
        used_tmp[tmp] = 1
    else:
        used_tmp[tmp] += 1


def unusetmp(tmp):
    """Remove a use of a temporary variable number"""

    #e.g. when the optimiser rewrites or deletes an instruction

    global used_tmp
    trace("#unuse:" + str(tmp))
    if type(tmp) == str:
        if tmp.startswith("tmp"):
            tmp = int(tmp[3:])

    if used_tmp.has_key(tmp):
        used_tmp[tmp] -= 1
        if used_tmp[tmp] == 0:
            del used_tmp[tmp]
            trace("#deleted:" + str(tmp))
            trace("#used_tmp:" + str(used_tmp))


def poptop():
    """Pop the top item off of the parse stack"""

    top = stack.pop()
    trace("poptop:" + str(top))
    if istmp(top):
        tmp = tmp_stack.pop()
        trace("top popped:" + str(top) + " tmp stack popped:" + str(tmp))
    return top


def emit(t, tval=None):
    """Emit code for this token"""

    global outbuf
    if t == CONST:
        pushconst(tval)

    elif t == '+':
        a = poptop()
        b = poptop()
        tmp = newtmp()
        # Note, a and b are rvalue uses of these items that need counting
        tac = ["ADD", str(a), str(b), maketmp(tmp)]
        pushtmp(tmp)
        if istmp(a): usetmp(a)
        if istmp(b): usetmp(b)
        ac = tac_to_ac(tac)
        for c in ac:
            outbuf.append(c)
        #outbuf.append(tac)

    elif t == '-':
        a = poptop()
        b = poptop()
        tmp = newtmp()
        # Note, a and b are rvalue uses of these items that need counting
        tac = ["SUB", str(b), str(a), maketmp(tmp)]
        pushtmp(tmp)
        if istmp(a): usetmp(a)
        if istmp(b): usetmp(b)
        ac = tac_to_ac(tac)
        for c in ac:
            outbuf.append(c)
        #outbuf.append(tac)


#----- TAC TRANSFORMER --------------------------------------------------------------
#
# Transforms TAC (three address code) into the machine architecture (accumulator code)

def tac_to_ac(tac):
    """Translate three-address-code to accumulator-code"""
    
    # This creates instructions that are compatible with the target architecture
    # which is accumulator based and single operand based.

    # Note this could be written as a rule in a rule rewrite engine
    # Note this is where we could synthesise lots of things, including
    # inlining shifts and multiply routines from pseudo TAC instructions

    # ADD const0,const1->tmp0 becomes
    #   LDA const0
    #   ADD const1
    #   STA tmp0
    #
    # SUB const0, const1->tmp0 becomes
    #   LDA const0
    #   SUB const1
    #   STA tmp0

    operator, op1, op2, res = tac
    if operator == "ADD":
        ac = [
            ["LDA", op1],
            ["ADD", op2],
            ["STA", res]
        ]
    elif operator == "SUB":
        ac = [
            ["LDA", op1],
            ["SUB", op2],
            ["STA", res]
        ]
    return ac


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

if __name__ == "__main__":
    while True:
        try:
            inbuf = raw_input("") # if not isatty don't send prompt, else send prompt (see ark-iotic)
            pos = 0
        except EOFError:
            break

        lookahead = lexer()
        while lookahead != None:
            outbuf = []
            expr()
            match(';')
            stack.pop()

            # each subexpression is output at each step
            outbuf.append(["LDA", "tmp0"])
            outbuf.append(["OUT",""])

            # Run an optimisation pass on this code region only
            peephole_redundant_store_load(outbuf)

            # Output all code for this code region
            for i in outbuf:
                opcode, operand = i
                print(opcode + " " + str(operand))

            # empty the tmp stack
            tmp_stack = []

    # Mark the end of the complete program
    print("HLT")


    # Allocate space for constants
    for i in range(len(const_used)):
        value = const_used[i]
        print(makeconst(value) + " DAT " + str(value))

    # Allocate space for variables
    trace("#" + str(used_tmp))
    for t in used_tmp:
        print(maketmp(t) + " DAT")




#================================================================================


# Planned features:
#   expression parsing
#   named variables (integer only)
#   functions and procedures
#   function return results
#   function and procedure parameters
#   call and return (simulated stack?)

# TODO put a limit on range of integer numbers (0..999)
# TODO consider negative numbers?

# add variables to grammar

# add in() function to grammar
# this is our first compiler intrinsic. in() generates IN

# Add inlining support for mult and div (no runtime machine stack yet)
# - these are also compiler intrinsics

# Add set statement to grammar (split OUT and expr into sepr statements

# Add print statement to grammar (compiler intrinsic that generates OUT)

# add if statements

# add trap instructions (trap0 is stop trap1..999 are os calls)

# add loops

# Add a runtime machine stack (call and return, single level at this state)
# - can we do an indirect branch??? Only by self modifying code?
# - move mult/div to a library routine that is called
# - store library routines in a library and link it in
# - can then use library version of mult and div to save code space

# Add multi level software stack with call and return
# - user procedures, global variables
# - add parameters
# - add return results
# - add in scope (global/local)
# - add in a display? (for nested scopes)
# - add local variables

