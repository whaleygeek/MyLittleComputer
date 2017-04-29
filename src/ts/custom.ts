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

function trace(msg:string):void {
    serial.writeLine(msg)
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
    // HLT = 000
    // ADD = 100
    // SUB = 200
    // STA = 300
    // # 400 not defined by LMC architecture
    // LDA = 500
    // BRA = 600
    // BRZ = 700
    // BRP = 800
    // INP = 901
    // OUT = 902
    //
    // # Pseudo opcodes, used by assembler only, not by LMC architecture
    // # An out of range opcode is used to signify these.
    // PSEUDO = 1000
    // DAT    = 1000
    // #1001..1999 not used yet
    //
    //
    // # useful lookup table for string versions of operands
    // no_operands = [INP, OUT, HLT]
    //
    // operators = {
    // 	HLT: "HLT",  # this is really HLT 00
    // 	ADD: "ADD",
    // 	SUB: "SUB",
    // 	STA: "STA",
    // 	LDA: "LDA",
    // 	BRA: "BRA",
    // 	BRZ: "BRZ",
    // 	BRP: "BRP",
    // 	INP: "INP",  # this is really IO 1
    // 	OUT: "OUT",  # this is really IO 2
    // 	# PSEUDO
    // 	DAT: "DAT" # PSEUDO instruction, for convenience
    // }

    function register_mnemonic(name:string, code:number, has_operations:boolean=false):void {
        // def registerMnemonic(name, code, hasOperands=false):
        // 	"""Register a new Mnemonic in the instruction tables"""
        //
        // 	# Define the constant (e.g. instruction.XXX)
        // 	me = sys.modules[__name__]
        // 	setattr(me, name, code)
        //
        // 	# Add the name into the table (e.g. XXX: "XXX"
        // 	operators[code] = name
        //
        // 	# If appropriate, flag that it has no operands
        // 	if not hasOperands:
        // 		global no_operands
        // 		no_operands += [code]
    }

    //function reverse_lookup(mymap:list, value:number):string {
        // def reverseLookup(mymap, value):
        // 	"""Lookup a value in a map, and get it's key"""
        //
        // 	value_idx = mymap.values().index(value)
        // 	key = mymap.keys()[value_idx]
        // 	return key
        //return "" //TODO
    //}

    function build(operator:number, operation:number=0):number {
        // def build(operator, operand=null):
        // 	"""Build an instruction"""
        //
        // 	#trace("build:" + str(operator) + " " + str(operand))
        //
        // 	if operator == null and operand == null:
        // 		return 0
        //
        // 	if type(operator) != number:
        // 		raise ValueError("non number operator:" + str(operator))
        //
        // 	if operand == null:
        // 		operand = 0
        //
        // 	elif operand < 0 or operand > 99: # TODO change to 0..255 to allow binary/hex machines
        // 		raise ValueError("Operand out of range:" + str(operand))
        //
        // 	return operator + operand # TODO might have to store differently to allow bytes
        // 	# but beware, when we get it's value on a decimal machine, it must return correct value
        return 0 //TODO
    }

    function set_operator(instr:number, operator:number):number {
        // def setOperator(instr, operator):
        // 	"""Set the operator in an existing instruction"""
        //
        // 	operand = getOperand(instr)
        // 	return build(operator, operand)
        return 0 //TODO
    }

    function set_operand(instr:number, operand:number):number {
        // def setOperand(instr, operand):
        // 	"""Set the operand in an existing instruction"""
        //
        // 	operator = getOperator(instr)
        // 	return build(operator, operand)
        return 0 //TODO
    }

    function get_operator(instr:number):number {
        // def getOperator(instr):
        // 	"""Get the operator from an existing instruction"""
        //
        // 	operator = (instr/100)*100 # change for binary machine, but beware of breaking number output
        // 	return operator
        return 0 //TODO
    }

    function get_operand(instr:number):number {
        // def getOperand(instr):
        // 	"""Get the operand from an existing instruction"""
        //
        // 	return instr % 100 # change for binary machine, but beware of breaking number output
        return 0 //TODO
    }

    function has_operand(instr:number):boolean {
        // def has_operand(instr):
        // 	"""Check if this instruction has an operand or not"""
        // 	# Note the special handling for INP OUT HLT (and IO n, HLT n)
        //
        // 	try:
        // 		no_operands.index(instr)
        // 	except:
        // 		return true
        // 	return false
        return false //TODO
    }

    function get_operator_string(instr:number):string {
        // def getOperatorString(instr):
        // 	"""Turn a numeric operator inside an instr into a string"""
        //
        // 	if operators.has_key(instr):
        // 		return operators[instr]
        //
        // 	instr = getOperator(instr)
        // 	if operators.has_key(instr):
        // 		return operators[instr]
        //
        // 	else:
        // 		raise ValueError("Unknown operator:" + str(instr))
        return "" // TODO
    }

    function to_string(instr:number):string {
        // def toString(instr):
        // 	"""Get a string representation of any instruction"""
        //
        // 	result = getOperatorString(instr)
        // 	if has_operand(instr):
        // 		operand = getOperand(instr)
        // 		result = result + " " + str(operand).zfill(2) ## might need to change for binary machine
        // 	return result
        return "" //TODO
    }

    function is_operator(s:string):boolean {
        // def isOperator(s):
        // 	"""Is this string an operator or not?"""
        // 	try:
        // 		reverseLookup(operators, s)
        // 		return true
        // 	except:
        // 		return false
        return false //TODO
    }

    function operator_from_string(s:string):number {
        // def operatorFromString(s):
        // 	"""Turn a string into a numberic operator"""
        // 	# We also support numberic operators (000..999) # change this for binary machine
        // 	try:
        // 		operator = number(s)
        // 		return operator
        // 	except:
        // 		pass
        //
        // 	s = s.upper()
        // 	operator = reverseLookup(operators, s)
        // 	return operator
        return 0 //TODO
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
    //
    // DECIMAL     = 10
    // BINARY      = 2
    // HEXADECIMAL = 16
    //
    // thebase = DECIMAL

    function configure(base:number):void {
        // def configure(base):
        //     global thebase
        //     thebase = base
    }

    function read(base:number=null, width:number=null, file:string=null): void {
        // def read(base=null, width=null, file=null):
        //     if base == null:
        //         base = thebase
        //
        //     if base == DECIMAL:
        //         return decimal.read(width=width, file=file)
        //     elif base == BINARY:
        //         return binary.read(width=width, file=file)
        //     elif base == HEXADECIMAL:
        //         return hexadecimal.read(width=width, file=file)
        //     else:
        //         raise ValueError("Unsupported base:" + str(base))
    }

    function write(number:number, base:number=null, width:number=null, file:string=null):void {
        // def write(number, base=null, width=null, file=null):
        //     if base == null:
        //         base = thebase
        //
        //     if base == DECIMAL:
        //         decimal.write(number, width=width, file=file)
        //     elif base == BINARY:
        //         binary.write(number, width=width, file=file)
        //     elif base == HEXADECIMAL:
        //         hexadecimal.write(number, width=width, file=file)
        //     else:
        //         raise ValueError("Unsupported base:" + str(base))
    }

    function writeln(number:number, base:number=null, width:number=null, file:string=null):void {
        //
        // #def writeln(number, base=null, width= null, file=file):
        // #    write(number, base=base, width=width, file=file)
        // #    if file == null:
    }
}


//----- DECIMAL ---------------------------------------------------------------

namespace mlc_decimal {

    // # Read and write decimal 3 digit unsigned numbers
    // # with zero padding
    //
    let DEFAULT_WIDTH = 3

    function read(width:number=DEFAULT_WIDTH, file:string=null):number {
        // def read(width=null, file=null):
        //     #trace("read")
        //     """return a decimal number in range 000-999"""
        //     # default width is 3 characters, but you can ask for wider
        //
        //     if width == null:
        //         width = DEFAULT_WIDTH
        //
        //     if file == null: # stdin, strip blank lines
        //         #trace("stdin")
        //         while true:
        //             try:
        //                 try:
        //                     line = raw_input()
        //                 except:
        //                     line = input()
        //             except EOFError:
        //                 #trace(" EOF")
        //                 return null # EOF
        //
        //             line = line.strip() # strip wrapping spaces and newline char
        //             if len(line) != 0:
        //                 instr = number(line)
        //                 #trace(" instr:" + str(instr))
        //                 return instr
        //
        //     else: # from file, strip blank lines
        //         #trace("file")
        //         #raise RuntimeError("HERE")
        //         while true:
        //             line = file.readline()
        //             if line == "":
        //                 #trace(" EOF")
        //                 return null # EOF
        //             line = line.strip() # strip wrapping spaces and newline char
        //             if len(line) != 0:
        //                 instr = number(line)
        //                 #trace(" instr:" + str(instr))
        //                 return instr
        return 0 //TODO
    }

    function write(number:number, width:number=null, file:string=null):void {
        // def write(number, width=null, file=null):
        //     #trace("write: %s %s %s %s" %( str(number) , str(type(number)), str(width), str(type(width))))
        //     """write a decimal number 000-999 zero padded"""
        //
        //     if width == null:
        //         width = DEFAULT_WIDTH
        //
        //     if file == null: # stdout
        //         trace(str(number).zfill(width))
        //     else: # to file
        //         file.write(str(number).zfill(width) + "\n")
    }
}


//----- BINARY ----------------------------------------------------------------

namespace mlc_binary {

    // # Read and write binary data as bytes (8 bit) and words (16 bits)
    //
    let DEFAULT_WIDTH = 8

    function read(width:number=DEFAULT_WIDTH, file:string=null):number {
    // def read(width=DEFAULT_WIDTH, file=null):
    //     """Read a binary number and return as range 0-255 or 0-65535"""
    //     if file == null:
    //         v = raw_input()
    //     else:
    //         v = file.readline()
    //     return number(v, 2)
        return 0 //TODO
    }

    function write(number:number, width:number=DEFAULT_WIDTH, file:string=null):void {
        // def write(number, width=DEFAULT_WIDTH, file=null):
        //     """Write a binary number"""
        //     f = "{0:0%db}" % width
        //     v = f.format(number)
        //     if file == null:
        //         trace(v)
        //     else:
        //         file.write(v)
        //         file.write('\n')
    }
}


//----- HEXADECIMAL -----------------------------------------------------------

namespace mlc_hexadecimal {

    // # Read and write hexadecimal 8 bit (2 char) or 16 bit (4 char) unsigned numbers
    // # with zero padding
    //
    let DEFAULT_WIDTH=4

    function read(file:string=null):number {
        // def read(file=null):
        //     if file == null:
        //         v = raw_input()
        //     else:
        //         v = file.readline()
        //     return number(v, 16)
        return 0 //TODO
    }

    function write(number:number, width:number=DEFAULT_WIDTH, file:string=null):void {
        // def write(number, width=DEFAULT_WIDTH, file=null):
        //     format = "%%0%dX" % width
        //     v = format % number
        //     if file == null:
        //         trace(v)
        //     else:
        //         file.write(v)
        //         file.write('\n')
    }
}


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

    function exec_HLT_instr(operand:number, acc:number):number {
        //
        // def execHLTInstr(operand, acc):
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

    function exec_IO_instr(operand:number, acc:number):number {
        //
        // def execIOInstr(operand, acc):
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
    // instruction.registerMnemonic("EXT", 400, false)
    // instruction.registerMnemonic("USB", 401, false)
    // instruction.registerMnemonic("MUL", 402, false)
    // instruction.registerMnemonic("DIV", 403, false)

    function exec_extended_instr(operand:number, acc:number):number {
        // def execExtendedInstr(operand, acc):
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

    //function bmux(old_execute:lambda):lambda {
        // def bmux(old_execute):
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

    //function hlt_isntrs(old_execute:lambda):lambda {
        // def hlt_instrs(old_execute):
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

    //function io_instrs(old_execute:lambda):lambda {
        // def io_instrs(old_execute):
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

    //function ext_instrs(old_execute:lambda):lambda {
        // def ext_instrs(old_execute):
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

    //function run(mem:number_array, start_addr:number=0):void {
        // def run(mem, startaddr = 0):
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
    //}

    //function cycle():void {
        // def cycle():
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
    //}

    //function fetch():void {
        // def fetch():
        // 	"""Fetch a single instruction from memory at the program counter pos"""
        //
        // 	instr = memory[program_counter]
        // 	return instr
    //}

    //function decode(instr:number):number {
        // def decode(instr):
        // 	"""Decode a single instruction"""
        //
        // 	operator = instruction.getOperator(instr)
        // 	operand = instruction.getOperand(instr)
        //
        // 	return operator, operand
        //return 0 //TODO
    //}

    //function truncate(value:number):number {
        // def truncate(v):
        // 	"""Truncate a value to the bus-width of the machine"""
        //
        // 	return v % (BUS_MAX+1)
        //return 0 //TODO
    //}

    // # Extended architecture features (comment out if you don't want them)
    // @extarch.bmux        # Add b_reg multiplexed with accumulator
    // @extarch.hlt_instrs  # add user specified HLT instructions
    // @extarch.io_instrs   # add user specified IO instructions
    // @extarch.ext_instrs  # add user specified EXT instructions
    //function execute(operator:number, operand:number, acc:number):number {
        // def execute(operator, operand, acc):
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
        //return 0 //TODO
    //}

    //function update_flags(value:number):void {
        // def update_flags(v):
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
    //}
}


//----- PARSER ----------------------------------------------------------------

namespace mlc_parser {

    // # Parse an input program file

    //function label_from_string(s:string):number {
        // def labelFromString(s):
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
        //return null //TODO
    //}

    //function parse_line(line:string):list_of_stuff   {
        // def parseLine(line):
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

    //function load(filename:string, memory:number_array, start_addr:number=0):void {
        // def load(filename, memory, startaddr=0):
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
    //}

    //function show_mem(memory:number_array, start:number=0, end:number=null):void {
        // def showmem(memory, start=0, end=null):
        //     """Show a range of a memory region"""
        //
        //     trace("MEMORY:")
        //     if end == null:
        //         end = len(memory)
        //     for addr in range(start, end):
        //         trace(str(addr) + " " + str(memory[addr]))
    //}
}


//----- SHELL -----------------------------------------------------------------

namespace mlc_shell {
    // # interactive shell

    // simulator.memory = [0 for i in range(99)]

    //function to_dec(n:number):string {
        // def todec(n):
        // 	return str(n).zfill(3)
        //return "" //TODO
    //}

    //function main():void {
        // def main():
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
    //}
}


//----- BOOT ------------------------------------------------------------------

namespace mlc_boot {
    //# boot a runnable system

    //function main():void {
        // def main():
        // 	FILENAME = sys.argv[1]
        // 	m = {}
        // 	loader.load(FILENAME, m)
        // 	run(m)
    //}
}

