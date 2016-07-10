# instruction.py  03/11/2014  D.J.Whale  
#
# Encode/Decode an instruction
#
# An instruction is a positive whole number 000-999
# xyy where:
# x is 0..9, the operator
# yy is 00..99, the operand

# decimal opcodes of all standard LMC instructions
HLT = 000
ADD = 100
SUB = 200
STA = 300
# 400 not defined by LMC architecture
LDA = 500
BRA = 600
BRZ = 700
BRP = 800
INP = 901
OUT = 902


# Opcodes that will be used to extend the machine architecture
# in a compatible way without breaking existing programs

# User Extension opcodes
# Probably useful for defining new custom instructions
EXT    = 400 # Extension instruction
USB    = 401 # use B register
MUL    = 402 # multiply A and B
DIV    = 403 # divide A and B
REM    = 404 # divide A and B and keep remainder
# 00, 05..99 not used yet

# IO opcodes, probably useful for defining new I/O instructions
IO     = 900 # Various I/O including INP and OUT
IO_IN  = 01
IO_OUT = 02
# 00, 03..99 not used yet

# HLT instructions, probably useful for OS calls
# Note special case of 000 is TRAP 00 = HLT.
# T00..T99 are traps
# 01..99 not used yet
HLT = 000

# Pseudo opcodes, used by assembler only, not by LMC architecture
# An out of range opcode is used to signify these.
PSEUDO = 1000
DAT    = 1000
#1001..1999 not used yet


# useful lookup table for string versions of operands

no_operands = [INP, OUT, EXT, IO, USB, MUL, DIV, HLT]

operators = {
	ADD: "ADD",
	SUB: "SUB",
	STA: "STA",
	LDA: "LDA",
	BRA: "BRA",
	BRZ: "BRZ",
	BRP: "BRP",

	EXT: "EXT",    # user extensions #will collide with X00 extension
    USB: "USB",
	MUL: "MUL",
	DIV: "DIV",

	# HARDWARE I/O
	IO:  "IO", # will collide with H00
	INP: "INP",  # this is really H 1
	OUT: "OUT",  # this is really H 2

	# Halts
	HLT: "HLT",  # this is really HLT 00

	# PSEUDO
	DAT: "DAT"
}


def trace(msg):
	print(str(msg))


def reverseLookup(mymap, value):
	"""Lookup a value in a map, and get it's key"""

	value_idx = mymap.values().index(value)
	key = mymap.keys()[value_idx]
	return key



def build(operator, operand=None):
	"""Build an instruction"""

	#trace("build:" + str(operator) + " " + str(operand))

	if operator == None and operand == None:
		return 0

	if type(operator) != int:
		raise ValueError("non int operator:" + str(operator))

	if operand == None:
		operand = 0

	elif operand < 0 or operand > 99: # TODO change to 0..255 to allow binary/hex machines
		raise ValueError("Operand out of range:" + str(operand))

	return operator + operand # TODO might have to store differently to allow bytes
	# but beware, when we get it's value on a decimal machine, it must return correct value


def setOperator(instr, operator):
	"""Set the operator in an existing instruction"""

	operand = getOperand(instr)
	return build(operator, operand)


def setOperand(instr, operand):
	"""Set the operand in an existing instruction"""
	
	operator = getOperator(instr)
	return build(operator, operand)


def getOperator(instr):
	"""Get the operator from an existing instruction"""

	operator = (instr/100)*100 # change for binary machine, but beware of breaking number output
	return operator
	

def getOperand(instr):
	"""Get the operand from an existing instruction"""
	
	return instr % 100 # change for binary machine, but beware of breaking number output


def has_operand(instr):
	"""Check if this instruction has an operand or not"""
	# Note the special handling for INP OUT HLT (and IO n, HLT n)

	try:
		no_operands.index(instr)
	except:
		return True
	return False


def getOperatorString(instr):
	"""Turn a numeric operator inside an instr into a string"""

	if operators.has_key(instr):
		return operators[instr]

	instr = getOperator(instr)
	if operators.has_key(instr):
		return operators[instr]

	else:
		raise ValueError("Unknown operator:" + str(instr))


def toString(instr):
	"""Get a string representation of any instruction"""

	result = getOperatorString(instr)
	if has_operand(instr):
		operand = getOperand(instr)
		result = result + " " + str(operand).zfill(2) ## might need to change for binary machine
	return result


def isOperator(s):
	"""Is this string an operator or not?"""
	try:
		reverseLookup(operators, s)
		return True
	except:
		return False


def operatorFromString(s):
	"""Turn a string into a numberic operator"""
	# We also support numberic operators (000..999) # change this for binary machine
	try:
		operator = int(s)
		return operator
	except:
		pass

	s = s.upper()
	operator = reverseLookup(operators, s)
	return operator


# END

