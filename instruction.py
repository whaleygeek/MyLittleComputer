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
U      = 400 # Unknown/User
# 00..99 not used yet

# IO opcodes, probably useful for defining new I/O instructions
IO     = 900 # Various I/O including INP and OUT
IO_IN  = 01
IO_OUT = 02
# 00, 03..99 not used yet

# HLT instructions, probably useful for OS calls
# Note special case of 000 is HLT 00 = HLT.
# 01..99 not used yet

# Pseudo opcodes, used by assembler only, not by LMC architecture
# An out of range opcode is used to signify these.
PSEUDO = 1000
DAT    = 1000
#1001..1999 not used yet


# useful lookup table for string versions of operands

no_operands = [HLT, INP, OUT]

operators = {
	HLT: "HLT",  # this is really HLT 00
	ADD: "ADD",
	SUB: "SUB",
	STA: "STA",
	U:   "U",    # unknown/user extensions
	LDA: "LDA",
	BRA: "BRA",
	BRZ: "BRZ",
	BRP: "BRP",
	INP: "INP",  # this is really IO 1
	OUT: "OUT",  # this is really IO 2

	# EXTENSION
	IO:  "IO",

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

	elif operand < 0 or operand > 99:
		raise ValueError("Operand out of range:" + str(operand))

	return operator + operand


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

	operator = (instr/100)*100
	return operator
	

def getOperand(instr):
	"""Get the operand from an existing instruction"""
	
	return instr % 100


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
		result = result + " " + str(operand).zfill(3)

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
	# We also support numberic operators (000..999)
	try:
		operator = int(s)
		return operator
	except:
		pass

	s = s.upper()
	operator = reverseLookup(operators, s)
	return operator


# END

