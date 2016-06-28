# simulator.py  0311/2014  D.J.Whale
#
# Simulate an LMC program.

import instruction
import loader
import io
import sys


BUS_MAX           = 999 # largest value the internal buses can use
PC_MAX            = BUS_MAX
STDIN_REDIRECTED  = not sys.stdin.isatty()
STDOUT_REDIRECTED = not sys.stdout.isatty()

program_counter   = 0
accumulator       = 0
z_flag            = False # zero
p_flag            = False # positive
halt              = False
memory            = {}


def trace(msg):
	print(str(msg))


def run(mem, startaddr = 0):
	"""Run a program to completion"""
	
	global program_counter, memory
	program_counter = startaddr
	memory = mem
	
	while not halt:
		#TODO check LMC spec, does 999+1 wrap to 000?
		if program_counter < 0 or program_counter > 999:
			raise ValueError("out of range program counter:" 
			  + str(program_counter))
		cycle()


def cycle():
	"""Run a single cycle of the LMC machine"""

	global program_counter
	
	# FETCH
	instr = fetch()
	#trace("fetch: pc:" + str(program_counter) + " instr:" + str(instr))
	program_counter = truncate(program_counter+1)
	
	# DECODE
	operator, operand = decode(instr)
	
	# EXECUTE
	execute(operator, operand)


def fetch():
	"""Fetch a single instruction from memory at the program counter pos"""

	instr = memory[program_counter]
	return instr
	
	
def decode(instr):
	"""Decode a single instruction"""
	
	operator = instruction.getOperator(instr)
	operand = instruction.getOperand(instr)
	return operator, operand
	

def truncate(v):
	"""Truncate a value to the bus-width of the machine"""

	return v % (BUS_MAX+1)


def execute(operator, operand):
	"""Execute a single instruction"""

	global program_counter, accumulator, z_flag, p_flag, memory, halt
	
	if   operator == instruction.HLT: # 0xx
		execHaltInstr(operand)

	elif operator == instruction.ADD: # 1xx
		accumulator += memory[operand]
		accumulator = truncate(accumulator)
		update_flags(accumulator)
		
	elif operator == instruction.SUB: # 2xx
		accumulator -= memory[operand]
		accumulator = truncate(accumulator)
		update_flags(accumulator)
		
	elif operator == instruction.STA: # 3xx
		memory[operand] = accumulator
		#trace("m[" + str(operand) + "]=" + str(accumulator))
		update_flags(accumulator)

	elif operator == instruction.U: # 4xx
		execUserInstr(operand)
		
	elif operator == instruction.LDA: # 5xx
		accumulator = memory[operand]
		#trace("a=m[" + str(operand) + "]")
		update_flags(accumulator)
		
	elif operator == instruction.BRA: # 6xx
		program_counter = operand
		#??update_flags(operand)
		
	elif operator == instruction.BRZ: # 7xx
		if z_flag:
			program_counter = operand
			#??update_flags(operand)
			
	elif operator == instruction.BRP: # 8xx
		if p_flag:
			program_counter = operand
			#??update_flags(operand)

	elif operator == instruction.IO: # 9xx
		if operand == instruction.IO_IN: # 901
			if not STDIN_REDIRECTED:
				sys.stdout.write("in? ")
			value = io.read()
			#TODO should we cope with negative numbers here and complement appropriately?
			#TODO: Should honour buswidth here depending on decimal/binary/hexadecimal io mode
			if value < 0 or value > 999:
				raise ValueError("Out of range value:" + str(value))
			accumulator = truncate(value)
			update_flags(accumulator)

		elif operand == instruction.IO_OUT: # 902
			if not STDOUT_REDIRECTED:
				sys.stdout.write("out=")
			io.write(accumulator)
			update_flags(accumulator)

		else: # user defined 9xx instructions
			execIOInstr(operand)

	else: # all might now be covered above??
		raise ValueError("Unknown operator:" + str(operator))

		
def update_flags(v):
	"""Update the z and p flags"""
	
	global z_flag, p_flag
	
	if v == 0:
		z_flag = True
	else:
		z_flag = False
		
	
	#TODO check if LMC specifies how this is represented
	# negative is just a representation, so 000-999 are all positive,
	# but split into two halves. Not that easy to do two's complement,
	# so it should really be 10's complement??
	# 000-499 positive
	# 500-999 negative i.e. 999 is -1
	# so if >= 500, negative, value = 1000 = value
	# does the assembler allow entry of negative numbers, and code them
	# into the appropriate complemented form?
	
	if v < 500: #TODO: This will be dependent on buswidth
		p_flag = True
	else:
		p_flag = False


# USER DEFINED INSTRUCTIONS ---------------------------------------------------
#
# This is a place that users can add their own instructions, while still
# being backwards compatible with the standard architecture.

# 000 is HLT but 001..099 are undefined. So, by modelling 0xx as a HLT
# and making HLT mean HLT 00, we can add HLT 01..HLT 99.
# Halts are useful for adding OS calls, for example, and might take
# a value in the accumulator to parameterise them, or the value in
# the accumulator might be a memory address that stores a block of
# parameters.

def execHaltInstr(operand):
	"""Execute any halt instructions here (instruction.T_XX)"""

	global halt
	# Note that instruction.HLT is HLT 00 (000)
	if operand == 0:
		halt = True
	else:
		raise ValueError("Unknown HLT instr:" + str(operand))
		# DEFINE USER HLT INSTRUCTIONS HERE


# 5xx instructions are not defined, so these are USER instructions,
# The whole range from 500 to 599 are free for user use. U + 00
# to U + 99 can be used to add specific instruction extensions,
# such as bitwise operators and other useful facilities that would
# not normally be done with OS calls.


def execUserInstr(operand):
	"""Execute any user instructions here (instruction.U_xx)"""

	global accumulator

	# Note, not possible to define user instructions that have other operands
	# due to their being insufficient space in the instruction format.
	# e.g. LDA 10 MULT 20 won't work
	# unless you say the 20 is a small constant, and the higher bits
	# represent the opcode and the lower bits the operand. This gets
	# messy with decimal as the range is 00-99 which is not a fixed number of bits.

	# So, it is better to reserve these instructions to either jump to specific
	# routines, or to work on nominated memory locations.
	# MULT for example could multiply the MULTIPLIER and the MULTIPLICAND
	# stored in separate named parameter registers. Or one of the operands could
	# be in accumulator, another in a named location.

	#TODO: Unless we pass forward the symbol table from the compiler
	#we won't know the address of the muldiv_reg
	
	if   operand == 01: # U 01  MUL
		##muldiv_reg_addr = symtab.get("muldiv_reg")
		##muldiv_reg = memory[muldiv_reg_addr]
		##accumulator = accumulator * muldiv_reg
		##update_flags(accumulator)
		raise RuntimeError("MUL not yet completely written")

	elif operand == 02: # U 02  DIV
		raise RuntimeError("DIV not yet completely written")
		# lookup muldiv_reg in symtab
		# acc = acc / muldiv_reg
		# update_flags(acc)
	else:
		raise ValueError("Unknown U instr:" + str(operand))


# 901=INP and 902=OUT, but 900 and 903..999 are not used.
# These undefined instructions are therefore useful to use to define
# other types of IO, such as GPO for general purpose output, GPI for
# general purpose input, AIN for analog input, and other I/O
# related things that would not warrant a HLT for an OS call.
# they could be done as User instrutions (U) but it's handy to group
# all the I/O together into a set of instructions.

def execIOInstr(operand):
	"""Execute any user IO instructions here (instruction.IO_xx)"""

	raise ValueError("Unknown IO instr:" + str(operand))
	# DEFINE IO INSTRUCTIONS HERE


# MAIN PROGRAM ----------------------------------------------------------------

def main():
	FILENAME = sys.argv[1]
	m = {}
	loader.load(FILENAME, m)
	run(m)


if __name__ == "__main__":
	#TODO#### get encoder decoder settings from args io.configure()
	main()


# END


