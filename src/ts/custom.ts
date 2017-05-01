// Code as imported from original Python project.

//   TODO: rewrite in TypeScript
//   TODO: wire up I/O to platform
//   TODO: wire up an interactive REPL using 'interactive'
//   TODO: split back into separate modules
//   TODO: create a pxt-package with a visual wrapper
//   TODO: publish as pxt-package

// TODO: might want to add disassembler so we can build a REPL based monitor
// TODO: might want to add assembler so we can build a REPL based monitor
// TODO: might want to add symtab so we can build a simple variable-aware debugger


//----- DEBUG -----------------------------------------------------------------

//possibly in namespace debug?

function trace(msg: string): void {
    serial.writeLine(msg)
}

//TODO: need better error handling
function error(msg: string): void {
    serial.writeLine(msg)
}


//----- STREAMS ---------------------------------------------------------------

namespace streams {
    export interface InputStream {
        isEnd(): boolean;
        readLine(): string;
        readChar(): string;
        putBack(data: string): void;
    }

    export interface File {
        length(): number;
        getPos(): number;
        setPos(pos: number): void;
        reset(): void;
    }

    export class ReadOnlyFile
        implements InputStream, File {
        data: string
        pos: number
        eof: boolean

        constructor(data: string) {
            this.data = data // is this a reference or a copy?
            this.pos = 0 // start of file
            this.eof = false
        }

        length(): number {
            // get the filesize
            return this.data.length()
        }

        getPos(): number {
            // get the current file pos
            return this.pos
        }

        setPos(pos: number) {
            // set the current file pos
            if (pos < 0 || pos > this.data.length) {
                // raise error
            } else {
                this.pos = pos
            }
        }

        reset(): void {
            this.eof = false
            this.pos = 0
        }

        isEnd(): boolean {
            // work out if hit end of file or not
            return this.eof
        }

        readLine(): string {
            // read characters until EOLN or EOF
            // if already eof, raise an error?
            if (this.eof) {
                // raise error
                return ""
            } else {
                let line = ""
                let c = ""
                while (c != '\n' && !this.eof) {
                    c = this.readChar()
                    if (!this.eof) {
                        line += c
                    }
                }
                return line
            }
        }

        readChar(): string {
            // read a single char
            // if already EOF, raise an error
            // advance pointer by one, maintain eof flag
            // return string with single char in it
            if (this.pos < this.data.length) {
                let ch = this.data[this.pos]
                this.pos += 1
                return ch
            }
            this.eof = true
            return "" //TODO: read past eof
        }

        putBack(data: string): void {
            // putback 1 or more characters, useful for lookahead parsers
            // validate that what is being put back is correct
            // validate we are not putting back beyond start of string
            // if bad, raise an error
            // wind back pos by the length of this string
        }
    }

    class SerialInputStream implements InputStream {
        line: string
        lpos: number

        constructor() {
            this.line = ""
            this.lpos = 0
        }

        isEnd(): boolean {
            // Serial never generates EOF
            return false
        }

        readLine(): string { //blocking
            return serial.readLine()
        }

        readChar(): string { //blocking
            if (this.lpos >= this.line.length) {
                this.line = this.readLine()
                this.lpos = 0
            }
            let c = this.line[this.lpos]
            this.lpos += 1
            return c
        }

        putBack(data: string): void {
            //TODO: unimplemented
        }
    }
    export interface OutputStream {
        write(s: string): void;
        writeLine(s: string): void
    }
    export class ScreenOutputStream implements OutputStream {
        constructor() { }

        write(s: string) {
            basic.showString(s)
        }
        writeLine(s: string) {
            basic.showString(s)
            basic.pause(200)
            basic.clearScreen()
        }
    }
    export class SerialOutputStream implements OutputStream {
        constructor() { }

        write(s: string) {
            serial.writeString(s)
        }

        writeLine(s: string) {
            serial.writeLine(s)
        }
    }
    export class IOStream implements InputStream, OutputStream {
        inp: InputStream
        out: OutputStream

        constructor(inp: InputStream, out: OutputStream) {
            this.inp = inp
            this.out = out
        }
        isEnd(): boolean {
            return this.inp.isEnd()
        }
        readLine(): string {
            return this.inp.readLine()
        }
        readChar(): string {
            return this.inp.readChar()
        }
        putBack(data: string): void {
            this.inp.putBack(data)
        }
        write(s: string) {
            this.out.write(s)
        }
        writeLine(s: string) {
            this.out.writeLine(s)
        }
    }

}


//----- MAP -------------------------------------------------------------------

//beware, null==0
//so if value==0, value==null??

//note, bug in generics is being fixed at moment, so can't use this yet

class Map<K, V> {

    keys: K[]
    values: V[]

    constructor() {
    }

    push(key: K, value: V) {
        this.keys.push(key)
        this.values.push(value)
    }

    search_array(a: Object[], item: Object): number {
        for (let i = 0; i < a.length; i++) {
            if (a[i] == item) {
                return i
            }
        }
        return -1 // NOT FOUND
    }

    value_for(key: K): V {
        let i = this.search_array(this.keys, key)
        if (i == -1) {
            return null
        }
        return this.values[i]
    }

    key_for(value: V): K {
        let i = this.search_array(this.values, value)
        if (i == -1) {
            return null
        }
        return this.keys[i]
    }

    set(key: K, value: V): void {
        let i = this.search_array(this.keys, key)
        if (i == -1) {
            this.keys.push(key)
            this.values.push(value)
        } else {
            this.values[i] = value
        }
    }

    has_key(key: K): boolean {
        return this.search_array(this.keys, key) != -1
    }

    has_value(value: V): boolean {
        return this.search_array(this.values, value) != -1
    }
}


//----- INSTRUCTION -----------------------------------------------------------

namespace mlc_instruction {

    // # Encode/Decode an instruction
    // #
    // # An instruction is a positive whole number 000-999
    // # xyy where:
    // # x is 0..9, the operator
    // # yy is 00..99, the operand
    //
    // # decimal opcodes of all standard LMC instructions
    enum Operand {
        HLT = 000,
        ADD = 100,
        SUB = 200,
        STA = 300,
        // # 400 not defined by LMC architecture
        LDA = 500,
        BRA = 600,
        BRZ = 700,
        BRP = 800,
        INP = 901,
        OUT = 902,

        // # Pseudo opcodes, used by assembler only, not by LMC architecture
        // # An out of range opcode is used to signify these.
        PSEUDO = 1000,
        DAT = 1000
        // #1001..1999 not used yet
    }

    // bug in pxt prevents this working. Fix going into beta Tuesday 2nd May.
    // find a workaround until then, and ignore the extension mechanism for now.
    //let operands: Map<number, string> = new Map<number, string>()

    //operands.push(Operand.HLT, "HLT")
    //        Operand.HLT, "HLT",
    //        Operand.ADD, "ADD",
    //        Operand.SUB, "SUB",
    //        Operand.STA, "STA",
    //        Operand.LDA, "LDA",
    //        Operand.BRA, "BRA",
    //        Operand.BRZ, "BRZ",
    //        Operand.BRP, "BRP",
    //        Operand.INP, "INP",
    //        Operand.OUT, "OUT"
    //    ])

    let operands_n: number[] = [
        Operand.HLT,
        Operand.ADD,
        Operand.SUB,
        Operand.STA,
        Operand.LDA,
        Operand.BRA,
        Operand.BRZ,
        Operand.BRP,
        Operand.INP,
        Operand.OUT
    ]

    let operands_s: string[] = [
        "HLT",
        "ADD",
        "SUB",
        "STA",
        "LDA",
        "BRA",
        "BRZ",
        "BRP",
        "INP",
        "OUT"
    ]

    let no_operands: number[] = [
        Operand.INP,
        Operand.OUT,
        Operand.HLT
    ]

    function numberToString(op: number): string {
        //return this.operands.value_for(op)

        for (let i = 0; i < operands_n.length; i++) {
            if (operands_n[i] == op) {
                return operands_s[i]
            }
        }
        error("Operator number not found")
        return ""
    }

    function stringToNumber(op: string): number {
        //return this.operands.key_of(op)
        for (let i = 0; i < operands_s.length; i++) {
            if (operands_s[i] == op) {
                return operands_n[i]
            }
        }
        error("Operator string not found")
        return 0 //TODO: Unknown
    }

    function registerMnemonic(name: string, code: number, hasOperands: boolean = false): void {
        // 	"""Register a new Mnemonic in the instruction tables"""
        // 	# Define the constant (e.g. instruction.XXX)
        // 	me = sys.modules[__name__]
        // 	setattr(me, name, code)

        // 	# Add the name into the table (e.g. XXX: "XXX"
        //this.operands.add(code, name)
        this.operands_n.push(code)
        this.operands_s.push(name)

        // 	# If appropriate, flag that it has no operands
        if (!hasOperands) {
            this.no_operands.append(code)
        }
    }


    function build(operator: number, operand: number = 0): number {
        // 	"""Build an instruction"""
        // 	#trace("build:" + str(operator) + " " + str(operand))

        if (operand < 0 || operand > 99) {
            error("Operand out of range 0..99")
        }

        // 	return operator + operand # TODO might have to store differently to allow bytes
        // 	# but beware, when we get it's value on a decimal machine, it must return correct value
        return operator + operand
    }

    function setOperator(instr: number, operator: number): number {
        // 	"""Set the operator in an existing instruction"""
        let operand = this.getOperand(instr)
        return this.build(operator, operand)
    }

    function setOperand(instr: number, operand: number): number {
        // 	"""Set the operand in an existing instruction"""
        let operator = this.getOperator(instr)
        return this.build(operator, operand)
    }

    function getOperator(instr: number): number {
        // 	"""Get the operator from an existing instruction"""
        return (instr / 100) * 100 //TODO: change for binary machine, but beware of breaking number outut
    }

    function getOperand(instr: number): number {
        // 	"""Get the operand from an existing instruction"""
        return instr % 100 //TODO: change for binary machine, but beware of breaking number output
    }

    function hasOperand(instr: number): boolean {
        // 	"""Check if this instruction has an operand or not"""
        // 	# Note the special handling for INP OUT HLT (and IO n, HLT n)
        return !this.no_operands.has_key(instr & 100)
    }

    function getOperatorString(instr: number): string {
        // 	"""Turn a numeric operator inside an instr into a string"""

        if (this.operators.has_hey(instr)) {
            return this.operators.value_for(instr)
        }

        instr = this.getOperator(instr)
        if (this.operators.has_key(instr)) {
            return this.operators.value_for(instr)
        } else {
            error("Unknown operator")
            return ""
        }
    }

    function toString(instr: number): string {
        // 	"""Get a string representation of any instruction"""

        let result = this.getOperatorString(instr)
        if (this.hasOperand(instr)) {
            let operand = this.getOperand(instr)
            result = result + " " + operand.toString() //TODO change for binary machine
            //TODO: need Typescript equivalent of zfill(2)
        }
        return result
    }

    function isOperator(s: string): boolean {
        // 	"""Is this string an operator or not?"""
        return this.operators.has_value(s)
    }
}


//----- IO --------------------------------------------------------------------

namespace mlc_io {

    // # Handle the input/output streams to a running program.
    // # This decides how to read and write data to and from a running program,
    // # or to and from a stored program file.
    // #
    // # Depending on the configuration, it can use decimal, binary or hexadecimal
    // # of any width in characters/bytes. You can also set a default base and width
    // # that will be used if not supplied.

    let DECIMAL = 10
    let BINARY = 2
    let HEXADECIMAL = 16

    let theBase = DECIMAL
    let theInpStream: streams.InputStream = null
    let theOutStream: streams.OutputStream = null

    export function setDefaults(base: number, inp: streams.InputStream = null, out: streams.OutputStream = null): void {
        theBase = base
        theInpStream = inp
        theOutStream = out
    }

    function format10(n: number, width = 3, zeroPad = true, signed = false): string {
        // if zero padding, work out how many zeros to add first
        let result = ""
        let neg: boolean = n < 0
        n = Math.abs(n) // strip any sign
        let err: boolean = false

        if (!signed && neg) {
            err = true
        }

        // SIGN
        if (neg) {
            result = "-"
        }

        let value = n.toString()

        // ZEROPAD
        if (zeroPad) {
            let len = value.length + result.length
            if (len < width) {
                let numz = width - len
                for (; numz > 0; numz--) {
                    result += "0"
                }
            }
        }
        // VALUE
        result += n.toString()

        // LENGTH CHECK
        if (result.length > width) {
            err = true
        }

        // ERROR HANDLING
        if (err) {
            result = ""
            for (let i = 0; i < width; i++) {
                result += '*'
            }
        }
        return result
    }

    function parse10(s: string): number {
        return parseInt(s)
    }

    export function read(base: number = null, width: number = 3, stream: streams.InputStream = null, interactive: streams.OutputStream = null): number {
        if (base == null) {
            base = theBase
        }
        if (base != DECIMAL) {
            //error we only support decimal at moment
            return 0
        }
        if (stream == null) {
            stream = theInpStream
        }
        if (interactive == null) {
            interactive = theOutStream
        }
        if (interactive != null) {
            interactive.write("inp" + base.toString() + "> ")
        }
        //TODO might change this later to support any delimiter, e.g. [comma/newline]
        //stream.readUntil(charset:string)
        //i.e. let s = stream.readUntil("\n, ")
        let s = stream.readLine()
        return parse10(s)
    }

    export function write(n: number, base: number = null, width: number = 3, stream: streams.OutputStream = null): void {
        if (base == null) {
            base = theBase
        }
        if (stream == null) {
            stream = theOutStream
        }
        if (base != DECIMAL) {
            // error
            return
        }
        let s = format10(n)
        stream.write(s)
    }

    export function writeLine(n: number, base: number = null, width: number = null, stream: streams.OutputStream = null): void {
        write(n, base, width, stream)
        stream.writeLine("")
    }
}


//=============================================================================
//TODO: Not got past this line yet in the porting

//TODO: Not sure yet, but might put all extensions, and the extension wrappers
//in a simple mlc_extensions namespace

//----- HLTINSTRS -------------------------------------------------------------

namespace mlc_hlt_instrs {

    // # Extra HLT instructions for the instruction set simulator
    // # These are good for implementing OS calls
    //
    // # You can use mnemonic forms instead of HLT 01 HLT 02 etc if you want,
    // # but look at extinstrs.py to see how to runtime register new
    // # mneumonics in the instruction table from here, in a way that does
    // # not pollute the instruction.py with unnecessary optional detail.
    //
    // # HLT 00 (HLT) is handled in simulator.py and never delegated here.
    //
    // # 000 is HLT but 001..099 are undefined. So, by modelling 0xx as a HLT
    // # and making HLT mean HLT 00, we can add HLT 01..HLT 99.
    // # Halts are useful for adding OS calls, for example, and might take
    // # a value in the accumulator to parameterise them, or the value in
    // # the accumulator might be a memory address that stores a block of
    // # parameters.

    function execHLTInstr(operand: number, acc: number): number {
        // 	"""Execute any halt instructions here (instruction.T_XX)"""
        //
        // 	trace("executed HLT %d" % str(operand))
        // 	# DEFINE USER HLT INSTRUCTIONS HERE
        //
        // 	return acc
        return 0 //TODO
    }
}


//----- IOINSTRS --------------------------------------------------------------

namespace mlc_io_instrs {

    // # Add extra IO instructions to the instruction set simulator
    // //
    // # Runtime registration of generic form
    // # you can add specific mnemonic names here if you want,
    // # see the example in extinstrs.py to see how to do it in a way that
    // # does not pollute instruction.py with optional features.
    // //
    // instruction.registerMnemonic("IO", 900, false)
    // //
    //
    // # INP and OUT are already handled in simulator.py, and never delegated here.
    // //
    // # 901=INP and 902=OUT, but 900 and 903..999 are not used.
    // # These undefined instructions are therefore useful to use to define
    // # other types of IO, such as GPO for general purpose output, GPI for
    // # general purpose input, AIN for analog input, and other I/O
    // # related things that would not warrant a HLT for an OS call.
    // # they could be done as User instrutions (U) but it's handy to group
    // # all the I/O together into a set of instructions.

    function execIOInstr(operand: number, acc: number): number {
        // 	"""Execute any user IO instructions here (instruction.IO_xx)"""
        // //
        // 	trace("exec IO instr %d" % str(operand))
        // 	# DEFINE NEW IO INSTRUCTIONS HERE
        // 	return acc
        return 0 //TODO
    }
}


//----- EXTINSTRS -------------------------------------------------------------

namespace mlc_ext_instrs {

    // # Extended instructions that are added to the instuction set simulator
    //
    // # Runtime registration of new mnemonics in the instruction table
    // # This ensures that the assembler and disassembler can use the instructions
    // # with their proper mnemonic names, but by runtime registering them int
    // # does not pollute instruction.py with extended functionality
    //
    //TODO: beware, there is Python metamagic here that registers instruction constants.
    //will have to 'avoid' that in TypeScript.
    //EXT is a collection of extended instructions, the specific instance of which is
    //in the operand
    // instruction.registerMnemonic("EXT", 400, false)
    // instruction.registerMnemonic("USB", 401, false)
    // instruction.registerMnemonic("MUL", 402, false)
    // instruction.registerMnemonic("DIV", 403, false)

    function execExtendedInstr(operand: number, acc: number): number {
        // 	"""Execute any user instructions here (instruction.X_xx)"""
        //
        // 	if   operand == instruction.getOperand(instruction.USB): # Use Breg in next instruction
        // 		extarch.b_flag = true # next instr will use B instead of A
        //
        // 	elif operand == instruction.getOperand(instruction.MUL): # multiply
        // 		acc = extarch.b_reg * acc
        //
        // 	elif operand == instruction.getOperand(instruction.DIV): # divide
        // 		##trace("acc %d breg %d" % (acc, b_reg))
        // 		acc = extarch.b_reg / acc
        //
        // 	else:
        // 		raise ValueError("Unknown EXT instr:" + str(operand))
        //
        // 	return acc
        return 0 //TODO
    }
}


//----- EXTARCH ---------------------------------------------------------------

//NOTE: We have a solution for the lambdas now, in the notes.txt file
//so this is ready to be rewritten in TypeScript.
//we can use lambas to define function decorators for runtime chaining functions.

namespace mlc_ext_arch {

    // # Extended architecture features
    // # The b_reg and a b_flag is added.
    // # This makes it easier to implement two-operand MUL and DIV instructions
    // # even with the limited space in the instruction set format.
    //
    // #TODO: Add copious comments about this decorator system,
    // #it is not something that beginner python programs will be familiar with.
    //
    //
    // b_flag = false
    // b_reg  = 0

    //function bmux(oldExecute:lambda):lambda {
    //     """Add the b_reg architectural feature in as a multiplexor around execute()"""
    //     def new_execute(operator, operand, acc):
    //         global b_flag, b_reg
    //         # If b_flag is set, read and write the B rather than the A
    //         if b_flag:
    //             acc = b_reg
    //
    //         # EXECUTE
    //         acc = old_execute(operator, operand, acc)
    //
    //         # WRITE BACK
    //         instr = instruction.build(operator, operand)
    //         if b_flag and instr != instruction.USB:
    //             b_reg = acc
    //             b_flag = false
    //
    //         return acc
    //
    //     return new_execute # the patched (decorated) execute function with b_flag functionality
    //return null //TODO
    //}

    //function HLTInstrs(oldExecute:lambda):lambda {
    //     """Insert new HLT instructions into instruction simulation"""
    //     def new_execute(operator, operand, acc):
    //         if   operator == instruction.HLT: # 0xx
    //             if operand != 0: # HLT 00 is actually HLT
    //                 return hltinstrs.execHLTInstr(operand, acc)
    //         return old_execute(operator, operand, acc)
    //
    //     return new_execute
    //return null //TODO
    //}

    //function IOInstrs(oldExecute:lambda):lambda {
    //     """Insert new IO instructions into instruction simulation"""
    //     def new_execute(operator, operand, acc):
    //         if   operator == instruction.IO:
    //             instr = instruction.build(operator, operand)
    //             if instr != instruction.INP and instr != instruction.OUT:
    //                 return ioinstrs.execIOInstr(operand, acc)
    //         return old_execute(operator, operand, acc)
    //
    //     return new_execute
    ///return null //TODO
    //}

    //function EXTInstrs(oldExecute:lambda):lambda {
    //     """Insert new EXT instructions into instruction simulation"""
    //     def new_execute(operator, operand, acc):
    //         if   operator == instruction.EXT:
    //             return extinstrs.execExtendedInstr(operand, acc)
    //         return old_execute(operator, operand, acc)
    //
    //     return new_execute
    //return null //TODO
    //}
}


//=============================================================================


//----- SIMULATOR -------------------------------------------------------------

namespace mlc_simulator {

    // # Simulate a loaded program
    //
    // BUS_MAX           = 999 # largest value the internal buses can use
    // PC_MAX            = BUS_MAX
    // STDIN_REDIRECTED  = not sys.stdin.isatty()
    // STDOUT_REDIRECTED = not sys.stdout.isatty()
    //
    // program_counter   = 0
    // accumulator       = 0
    // z_flag            = false # zero
    // p_flag            = false # positive
    // halt_flag         = false
    // memory            = {}

    function run(mem: number[], startAddr: number = 0): void {
        // 	"""Run a program to completion"""
        //
        // 	global program_counter, memory
        // 	program_counter = startaddr
        // 	memory = mem
        //
        // 	while not halt_flag:
        // 		#TODO check LMC spec, does 999+1 wrap to 000?
        // 		if program_counter < 0 or program_counter > 999:
        // 			raise ValueError("out of range program counter:"
        // 			  + str(program_counter))
        // 		cycle()
    }

    function cycle(): void {
        // 	"""Run a single cycle of the LMC machine"""
        //
        // 	global program_counter, accumulator
        //
        // 	# FETCH
        // 	instr = fetch()
        // 	##trace("fetch: pc:" + str(program_counter) + " instr:" + str(instr))
        // 	program_counter = truncate(program_counter+1)
        //
        // 	# DECODE
        // 	operator, operand = decode(instr)
        //
        // 	# EXECUTE
        // 	accumulator = execute(operator, operand, accumulator)
    }

    function fetch(): number {
        // 	"""Fetch a single instruction from memory at the program counter pos"""
        //
        // 	instr = memory[program_counter]
        // 	return instr
        return 0 //TODO
    }

    function decode(instr: number): number {
        // 	"""Decode a single instruction"""
        //
        // 	operator = instruction.getOperator(instr)
        // 	operand = instruction.getOperand(instr)
        //
        // 	return operator, operand
        return 0 //TODO
    }

    function truncate(value: number): number {
        // 	"""Truncate a value to the bus-width of the machine"""
        //
        // 	return v % (BUS_MAX+1)
        return 0 //TODO
    }

    // # Extended architecture features (comment out if you don't want them)
    // @extarch.bmux        # Add b_reg multiplexed with accumulator
    // @extarch.hlt_instrs  # add user specified HLT instructions
    // @extarch.io_instrs   # add user specified IO instructions
    // @extarch.ext_instrs  # add user specified EXT instructions
    function execute(operator: number, operand: number, acc: number): number {
        // 	"""Execute a single instruction, and return new desired accumulator result"""
        //
        // 	global program_counter, z_flag, p_flag, memory, halt_flag
        //
        // 	if   operator == instruction.HLT: # 0xx
        // 		if operand == 0: # HLT 00 is actually HLT
        // 			halt_flag = true
        //
        // 	elif operator == instruction.ADD: # 1xx
        // 		acc += memory[operand]
        // 		acc = truncate(acc)
        //
        // 	elif operator == instruction.SUB: # 2xx
        // 		acc -= memory[operand]
        // 		acc = truncate(acc)
        //
        // 	elif operator == instruction.STA: # 3xx
        // 		memory[operand] = acc
        // 		##trace("m[" + str(operand) + "]=" + str(acc))
        //
        // 	elif operator == instruction.LDA: # 5xx
        // 		acc = memory[operand]
        // 		##trace("a=m[" + str(operand) + "]")
        //
        // 	elif operator == instruction.BRA: # 6xx
        // 		program_counter = operand
        //
        // 	elif operator == instruction.BRZ: # 7xx
        // 		if z_flag:
        // 			program_counter = operand
        //
        // 	elif operator == instruction.BRP: # 8xx
        // 		if p_flag:
        // 			program_counter = operand
        //
        // 	elif operator == instruction.IO: # 9xx
        // 		if operand == instruction.getOperand(instruction.INP): # 901
        // 			if not STDIN_REDIRECTED:
        // 				sys.stdout.write("in? ")
        // 			value = io.read()
        // 			#TODO: should we cope with negative numbers here and complement appropriately?
        // 			#TODO: Should honour buswidth here depending on decimal/binary/hexadecimal io mode
        // 			if value < 0 or value > 999:
        // 				raise ValueError("Out of range value:" + str(value))
        // 			acc = truncate(value)
        //
        // 		elif operand == instruction.getOperand(instruction.OUT): # 902
        // 			if not STDOUT_REDIRECTED:
        // 				sys.stdout.write("out=")
        // 			io.write(acc)
        //
        // 	else: # unhandled operator
        // 		raise ValueError("Unknown operator:" + str(operator))
        //
        // 	update_flags(acc)
        // 	return acc
        return 0 //TODO
    }

    function updateFlags(value: number): void {
        // 	"""Update the z and p flags"""
        //
        // 	global z_flag, p_flag
        //
        // 	if v == 0:
        // 		z_flag = true
        // 	else:
        // 		z_flag = false
        // 	#TODO check if LMC specifies how this is represented
        // 	# negative is just a representation, so 000-999 are all positive,
        // 	# but split into two halves. Not that easy to do two's complement,
        // 	# so it should really be 10's complement??
        // 	# 000-499 positive
        // 	# 500-999 negative i.e. 999 is -1
        // 	# so if >= 500, negative, value = 1000 = value
        // 	# does the assembler allow entry of negative numbers, and code them
        // 	# into the appropriate complemented form?
        //
        // 	if v < 500: #TODO: This will be dependent on buswidth
        // 		p_flag = true
        // 	else:
        // 		p_flag = false
    }
}


//----- PARSER ----------------------------------------------------------------

namespace mlc_parser {
    // # Parse an input program file

    function labelFromString(s: string): number {
        // 	"""Work out if this operand is a label or not"""
        //
        // 	# Is it numeric?
        // 	try:
        // 		operand = number(s)
        // 		return operand, null # just a normal number
        // 	except:
        // 		pass
        //
        // 	# Must be a label
        // 	return null, s # A labelref
        return null //TODO
    }

    //function parseLine(line:string):string[] {
    // 	"""parse a line into an instruction"""
    //
    // 	# Ignore lines that are comments
    // 	line = line.strip()
    // 	if line.startswith('#'):
    // 		return null, null, null, null # whole-line comment
    //
    // 	# Strip off end of line comment
    // 	try:
    // 		commentpos = line.index('#')
    // 		line = line[:commentpos]
    // 		line = line.strip()
    // 	except:
    // 		pass
    //
    // 	# Ignore lines with no instruction on them
    // 	parts    = line.split(" ")
    // 	if len(parts) == 0: # empty line
    // 		return null
    //
    // 	# Split line into [label] [operator] [operand]
    // 	label    = null
    // 	operator = null
    // 	operand  = null
    // 	labelref = null
    //
    // 	if len(parts) == 1: # (label) or (operator)
    // 		if instruction.isOperator(parts[0]): # (operator)
    // 			operator = instruction.operatorFromString(parts[0])
    // 		else: # (label) (operator)
    // 			label    = parts[0]
    //
    // 	elif len(parts) == 2: # (label operator) or (operator operand)
    // 		if instruction.isOperator(parts[0]): # (operator operand)
    // 			operator          = instruction.operatorFromString(parts[0])
    // 			operand, labelref = labelFromString(parts[1])
    //
    // 		else: # (label operator)
    // 			label    = parts[0]
    // 			operator = instruction.operatorFromString(parts[1])
    //
    // 	elif len(parts) == 3: # (label operator operand)
    // 		label             = parts[0]
    // 		operator          = instruction.operatorFromString(parts[1])
    // 		operand, labelref = labelFromString(parts[2])
    //
    // 	# DAT or instruction?
    // 	if operator == instruction.DAT:
    // 		operator = operand
    // 		operand  = null
    //
    // 	return label, operator, operand, labelref
    //return null //TODO
    //}
}


//----- LOADER ----------------------------------------------------------------

namespace mlc_loader {
    // # Load numeric data into memory
    // # Useful for loading a 'binary' file into the simulator

    function load(filename: string, memory: number[], startAddr: number = 0): void {
        //     """Load from a file into memory"""
        //
        //     f = open(filename, "rt")
        //     addr = startaddr
        //
        //     while true:
        //         instr = io.read(file=f)
        //         if instr != null:
        //             memory[addr] = instr
        //             addr += 1
        //         else:
        //             break
        //
        //     f.close()
    }

    function showMem(memory: number[], startAddr: number = 0, endAddr: number = null): void {
        // def showmem(memory, start=0, end=null):
        //     """Show a range of a memory region"""
        //
        //     trace("MEMORY:")
        //     if end == null:
        //         end = len(memory)
        //     for addr in range(start, end):
        //         trace(str(addr) + " " + str(memory[addr]))
    }
}


//----- MEMDUMP ---------------------------------------------------------------
//TODO: A tool used at the shell that allows memory to be dumped in hex, binary, dec
//across a range
//Note: This needs to be prototyped in Python first


//----- MEMEDIT ---------------------------------------------------------------
//TODO: a tool used at the shell that allows memory to be edited
//Note: This needs to be prototyped in Python first


//----- SHELL -----------------------------------------------------------------

namespace mlc_shell {
    // # interactive shell

    // simulator.memory = [0 for i in range(99)]

    function toDec(n: number): string {
        // 	return str(n).zfill(3)
        return "" //TODO
    }

    function main(): void {
        // 	while not simulator.halt_flag:
        // 		line = raw_input("instruction? ")
        //
        // 		label, operator, operand, labelref = parser.parseLine(line)
        // 		instr = instruction.build(operator, operand)
        // 		trace("instr:" + instruction.toString(instr))
        //
        // 		simulator.memory[simulator.program_counter] = instr
        // 		simulator.cycle()
        //
        // 		#TODO: Somehow adding b_reg functionality needs to add b display here too?
        // 		trace("  pc:"    + todec(simulator.program_counter)
        // 			+ " a:"    + todec(simulator.accumulator)
        // 			+ " z:"    + str(simulator.z_flag)
        // 			+ " p:"    + str(simulator.p_flag)
        // 			+ " halt:" + str(simulator.halt_flag))
    }
}


//----- BOOT ------------------------------------------------------------------

namespace mlc_boot {
    //# boot a runnable system

    function main(): void {
        // 	FILENAME = sys.argv[1]
        // 	m = {}
        // 	loader.load(FILENAME, m)
        // 	run(m)
    }
}

