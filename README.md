# MyLittleComputer

This is a complete toolchain for a tiny computer architecture

This is a complete toolchain for a tiny computer architecture. The chosen architecture is completely
compatible with the Little Man Computer architecture, as (mostly defined) here:

https://en.wikipedia.org/wiki/Little_man_computer
 
I have called this variant MLC (MyLittleComputer) as a re-arranged acronym of LMC
(LittleManComputer) to identify it's close resemblance but independence from it's inspirational parent.
 
The whole toolchain is written in Python.

The purpose of this toolchain is to provide a tiny but complete implementation, written in a style of Python
that is mostly understandable by children learning about the LMC architecture at school as part of their
GCSE studies. As such, very few features of the Python language are used, and features have been
selected based on a known subset used by children and school teachers.

Note: The Little Man Computer architecture stipulates a decimal representation (not a binary).
This is contrary to how modern CPU's are designed (they are binary machines). However, there
is (untested) experimental support for BINARY and HEXADECIMAL i/o modes, that can be configured
in io.py.


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

```
    cat > hello.mlc
    
    LDA one
    OUT
    HLT
    one DAT 1
    ^D
    
    python assembler.py hello.mlc hello.dec
    python simulator.py hello.dec
    
    out=001
```

Using the compiler
====

The compiler only supports simple arithmetic expressions in this version. It supports 
positive integer numbers, plus and minus, and brackets - nothing else!
The test cases hand-build a simple repeated-addition multiply routine. There are
hooks in the compiler grammar for a MULT and DIV instruction, but they are not implemented
yet.

```
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
```

You can see from the generated program that the compiler auto generates stored versions of any constants,
because there is no constant addressing mode in MLC. Also, the compiler auto-allocates temporary workspace
variables for you, and manages their lifetime, reusing them where possible.

```
    python assembler.py math.mlc math.dec
    python simulator.py math.dec
    
    out=008
```

If you put multiple lines, one expression per line terminated by a semicolon, it will display the
results of each expression one after the other.

Interactive mode
====

You can run interactive mode with interactive.py and type in assembly instructions one line at a time.
After you press return, it will show the processor state, then either ask for user input (if you use INP)
or ask for another instruction. ^D to finish (CTRL-D)

Test scripts
====

There are two very small test scripts, test_LMC and test_COMPILER that test out the toolchain from end to
end, by assembling, disasembling, compiling and simulating a simple routine. If you capture the output
files from these test scripts before changing the python code, make the change, then re-run the tests
and diff the resultant files, you will know if you have broken anything. They do not constitute an
exhaustive test harness.

Extending the machine
====

Unlike the original LMC, there are hook points in the simulator for extending the unused
instruction codes. Inside the simulator.py execute() function you will find each simulated
instruction. 

There are 3 places that you can extend the instruction set:

901 and 902 are INP and OUT respectively, so 900 and 903..999 are unused instructions.
If you include these instructions in your .dec file, they will be sent to execIOInstr() for
processing. The idea here is you could wire up new instructions to control GPIO pins on a Raspberry Pi,
or even to display characters on a SenseHat or other display device.

The original LMC specifies 000 as HLT, but does not specify what 001..099 are used for, and
are therefore undefined instructions. In the simulator.py execute() function all 0xx instructions
are routed to the execHaltInstr() function. Only 000 is handled (which halts the machine). 001..099
can be added by the user inside execHaltInstr() to perform anything. I always had a view that these
instructions could be used for non-IO based OS calls or runtime library calls, such as getting a random
number, reading the date and time, delaying for a fixed period, etc.

The original LMC does not specify any operation for 4xx instructions. The code routes these
to a execUserInstr(), so you can decode 400..499 and allocate any processing to these. I always
had a view that some of these would be used for intrinsic functions to extend the machine,
such as a MULT, DIV, REM for fast multiply and divide, shift and rotate instructions,
sign extension instructions, and other useful instructions. Intrinsics in this way can be used
to allow the core machine (which is beautifully simple) to be made more powerful. This could
be done by making these intrinsics jump to linked library routines that are written in LMC code,
or to just call user provided Python code.


Learning Opportunities
====

1. Look in the simulator.py file at function cycle() and you will see an explicit
fetch/decode/execute cycle. This is called in a loop from run() and each part of the
cycle is split into appropriate functions fetch() decode() and execute() just under this function.

2. This codebase is intentionally focused on implementing a few small features only, in the hope that the
resultant python programs are small enough that children can understand them, use them and modify them.

Feel free to fork this code, add more features to it, but let me know what you do with it!


New ideas
====

Of course, I have lots of new additions to add to the compiler, but feel free to do some of these yourself!

* multiply and divide
* compiler intrinsics (mult, div, rem, mod, shift)
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

28th June 2016




