# simulator.py  03/11/2014  D.J.Whale
#
# Simulate an LMC program.

import instruction
import loader
import io
import sys

# Extension mechanism
import hltinstrs
import ioinstrs
import extarch
import extinstrs


BUS_MAX           = 999 # largest value the internal buses can use
PC_MAX            = BUS_MAX
STDIN_REDIRECTED  = not sys.stdin.isatty()
STDOUT_REDIRECTED = not sys.stdout.isatty()

program_counter   = 0
accumulator       = 0
z_flag            = False # zero
p_flag            = False # positive
halt_flag         = False
memory            = {}


def trace(msg):
	print(str(msg))


def run(mem, startaddr = 0):
	"""Run a program to completion"""
	
	global program_counter, memory
	program_counter = startaddr
	memory = mem
	
	while not halt_flag:
		#TODO check LMC spec, does 999+1 wrap to 000?
		if program_counter < 0 or program_counter > 999:
			raise ValueError("out of range program counter:" 
			  + str(program_counter))
		cycle()


def cycle():
	"""Run a single cycle of the LMC machine"""

	global program_counter, accumulator
	
	# FETCH
	instr = fetch()
	##trace("fetch: pc:" + str(program_counter) + " instr:" + str(instr))
	program_counter = truncate(program_counter+1)
	
	# DECODE
	operator, operand = decode(instr)

	# EXECUTE
	accumulator = execute(operator, operand, accumulator)


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


@extarch.bmux
def execute(operator, operand, acc):
	"""Execute a single instruction, and return new desired accumulator result"""

	global program_counter, z_flag, p_flag, memory, halt_flag

	if   operator == instruction.HLT: # 0xx
		if operand == 0: # HLT 00 is actually HLT
			halt_flag = True
		#TODO: Could do this optional extension with extarch.hlt
		else:
			hltinstrs.execHLTInstr(operand) # EXTENSIONS

	elif operator == instruction.ADD: # 1xx
		acc += memory[operand]
		acc = truncate(acc)
		update_flags(acc)
		
	elif operator == instruction.SUB: # 2xx
		acc -= memory[operand]
		acc = truncate(acc)
		update_flags(acc)
		
	elif operator == instruction.STA: # 3xx
		memory[operand] = acc
		##trace("m[" + str(operand) + "]=" + str(acc))
		update_flags(acc)

	#TODO: could do this optional extension with extarch.ext
	elif operator == instruction.EXT: # 4xx
		acc = extinstrs.execExtendedInstr(operand, acc) # EXTENSION
		update_flags(acc)

	elif operator == instruction.LDA: # 5xx
		acc = memory[operand]
		##trace("a=m[" + str(operand) + "]")
		update_flags(acc)
		
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
		if operand == instruction.getOperand(instruction.INP): # 901
			if not STDIN_REDIRECTED:
				sys.stdout.write("in? ")
			value = io.read()
			#TODO: should we cope with negative numbers here and complement appropriately?
			#TODO: Should honour buswidth here depending on decimal/binary/hexadecimal io mode
			if value < 0 or value > 999:
				raise ValueError("Out of range value:" + str(value))
			acc = truncate(value)
			update_flags(acc)

		elif operand == instruction.getOperand(instruction.OUT): # 902
			if not STDOUT_REDIRECTED:
				sys.stdout.write("out=")
			io.write(acc)
			update_flags(acc)

		#TODO: Could do this optional extension with extarch.io
		else: # user defined 9xx instructions
			ioinstrs.execIOInstr(operand) # EXTENSIONS

	else: # all might now be covered above??
		raise ValueError("Unknown operator:" + str(operator))

	return acc

		
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


# MAIN PROGRAM ----------------------------------------------------------------

def main():
	FILENAME = sys.argv[1]
	m = {}
	loader.load(FILENAME, m)
	run(m)


if __name__ == "__main__":
	#TODO: get encoder decoder settings from args io.configure()
	#so that we can use BINARY and HEXADECIMAL modes too.
	main()


# END


