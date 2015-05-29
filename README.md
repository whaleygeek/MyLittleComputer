# MyLittleComputer

This is a complete toolchain for a tiny computer architecture

This code is at ALPHA release status. It is released into the community in order to trigger feedback and
further innovation. 

This is a complete toolchain for a tiny computer architecture. The chosen architecture is completely
compatible with the Little Man Computer architecture (but supports a range of additional extensions
in the form of IO calls and OS calls). MLC (MyLittle Computer) is a re-arranged acronym of LMC
(LittleManComputer) to identify it's close resemblance but independence from it's inspirational parent.

The whole toolchain is written in Python.

The purpose of this toolchain is to provide a tiny but complete implementation, written in a style of Python
that is mostly understandable by children learning about the LMC architecture at school as part of their
GCSE studies. As such, very few features of the Python language are used, and features have been
selected based on a known subset used by children and school teachers.

Note: The Little Man Computer architecture stipulates a decimal representation (not a binary).


The toolchain consists of:

assembler.py - assemble source code into decimal files.

disassembler.py - disassemble decimal files into source files

simulator.py - simulate a decimal file on an LMC compliant architecture

interactive.py - run an interactive session with the simulator

compiler.py - compile simple high level source programs into assembly language source files

Hello World
====

Your first assembly program should be "hello world", which just outputs the number '1':
(Note that ^D here means press "CTRL D")

    cat > hello.mlc

    LDA one
    OUT
    HLT
    one DAT 1
    ^D

    python assembler.py hello.mlc hello.dec
   python simulator.py hello.dec

    out=001

Using the compiler
====

The compiler only supports simple arithmetic expressions in this version. It supports 
positive integer numbers, plus and minus, and brackets - nothing else!

    cat > math.e
    1+(3-2+(4+5))-3;
    ^D

    python compiler.py < math.e > math.mlc
    cat math.mlc

    LDA const3
    SUB const2
    STA tmp0
    LDA const5
    ADD const4
    ADD tmp0
    ADD const1
    SUB const3
    OUT 
    HLT
    const1 DAT 1
    const3 DAT 3
    const2 DAT 2
    const4 DAT 4
    const5 DAT 5
    tmp0 DAT

You can see from the generated program that it auto generates stored versions of any constants,
and also auto allocates temporary workspace variables for you.

    python assembler.py math.mlc math.dec
    python simulator.py math.dec

    out=008

If you put multiple lines, one expression per line terminated by a semicolon, it will display the
results of each expression one after the other.

This codebase is intentionally focused on impementing a few small features only, in the hope that the
resultant python programs are small enough that children can understand them, use them and modify them.

Feel free to fork this code, add more features to it, but let me know what you do with it!

Of course, I have lots of new additions to add to the compiler, but feel free to do some of these yourself!

    * multiply and divide
    * compiler intrinsics (mult, div, mod, shift)
    * variables
    * support for negative numbers
    * if statements
    * using HLT 1.. HLT 999 to implement OS calls
    * using IO 3..999 to implement file io, GPIO, network IO, and other neat things
    * loops
    * call and return stack
    * function calls
    * function return results
    * function parameters
    * global and local variables
    * a larger memory space for programs
    * better optimisations in the compiler
    * a command line debugger
    * a tiny IDE written in Python
    * a visual debugger with single step and breakpoints
    * an interface to Minecraft (of course!)

David Whale

@whaleygeek

29 May 2015




