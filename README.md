# MyLittleComputer

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
in io.py, although I haven't done much tested of the BINARY and HEXADECIMAL modes yet so they
might not completely work.


The toolchain consists of:

assembler.py - assemble source code into decimal files.

disassembler.py - disassemble decimal files into source files

simulator.py - simulate a decimal file on an LMC compliant architecture

interactive.py - run an interactive session with the simulator

compiler.py - compile simple high level source programs into assembly language source files


The following instructions assume a Unix/Linux OS (Raspberry Pi, Ubuntu Linux, Mac OSX)

If you are on windows, create the files inside notepad first, and use the Command Prompt
to run the commands.


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
The test cases hand-build a simple repeated-addition multiply routine. 
The latest version also supports multiply and divide, and the MUL and DIV instructions
have been added as extension instructions to the simulator.

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
because there is no constant addressing mode in LMC/MLC. Also, the compiler auto-allocates temporary workspace
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

There is a single test suite. Unfortunately this is only written to run on Unix/Linux at the moment,
but you should be able to work out how to write a similar script for Windows using batch files if you
want to. The test_suite is mainly there so that I can run the tests when I make a change, to make sure
that nothing else has been broken.

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
to a execExtendedInstr(), so you can decode 400..499 and allocate any processing to these. I always
had a view that some of these would be used for intrinsic functions to extend the machine,
such as a MULT, DIV, REM for fast multiply and divide, shift and rotate instructions,
sign extension instructions, and other useful instructions. These can be used
to allow the core machine (which is beautifully simple) to be made more powerful. This could
be done by making these jump to linked library routines that are written in LMC code,
or to just call user provided Python code. I have already implemented MUL and DIV, and also
a USB instruction (use b register) that allows the second operand for MUL and DIV to be set.


Learning Opportunities
====

1. Look in the simulator.py file at function cycle() and you will see an explicit
fetch/decode/execute cycle. This is called in a loop from run() and each part of the
cycle is split into appropriate functions fetch() decode() and execute() just under this function.

2. This codebase is intentionally focused on implementing a few small features only, in the hope that the
resultant python programs are small enough that children can understand them, use them and modify them.

Feel free to fork this code, add more features to it, but let me know what you do with it!


Current work
====

I have just implemented some extended instructions that allow multiply and divide to work.
This works in the compiler as well (the grammar has been extended to allow them with the correct
precedence). To do this cleanly, I also added a USB instruction and a B register. USB modifies
the next instruction so that the source/target register address is b_reg rather than accumulator.
The MUL and DIV instructions don't have enough space inside their instruction to store an address
of a second operand (unlike all other LMC instructions), so the B register is used for the 
second operand.

A lot of work has just been done to move all optional extensions into separate modules.
This is so that the core simulator assembler and disassembler are as true to the original
LMC architecture as possible. I have not documented the extension mechanism yet (but will do 
soon), as this means that the MUL and DIV features can be turned on and off, and also that
students can extend the architecture and the instruction set in a clean way themselves
if they want to add new features.

I am looking at possibility of writing a librarian and a linker, so that the multiply and divide
routines could be written by children, and then put into a library and linked into the code.
This would actually be better than using extended instructions, as the multiply routine is
part of the standard syllabus to implement. It would also make the explanation of what the role
and operation of a librarian and a linker are much easier, by example (again, this is something
that is covered on the syllabus)

I want to make the command line parameter passing format consistent across all tools
(some use redirection, some use command line parameters, at the moment)


New ideas
====

Of course, I have lots of new additions to add to the compiler, but feel free to do some of these yourself!

* variables
* support for negative numbers
* if statements
* using HLT 01..HLT 99 to implement OS calls (TRAPS)
* using IO 3 .. IO99 to implement other hardware, such as: file io, GPIO, network IO, and other neat things
* loops
* call and return stack (single level, and multi level with a stack pointer)
* function calls
* function return results
* function parameters
* global and local variables
* lifetime and scope
* a larger memory space for programs
* better optimisations in the compiler
* a command line debugger
* a tiny IDE written in Python
* a visual debugger with single step and breakpoints
* an interface to Minecraft (of course!)
* a way to switch between bases seamlessly so that a binary machine can be used too

David Whale

@whaleygeek

2nd July 2016





