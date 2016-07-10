# extinstrs.py  10/07/2016  D.J.Whale
#
# Wxtended instructions that are added to the instuction set simulator

import extarch # for b_flag and b_reg
import instruction

# TODO: runtime registration of these 3 instrutions into the instruction.py tables
# will need to be done here, so that instruction.py is not polluted with non standard
# features.

# 5xx instructions are not defined, so these are USER instructions,
# The whole range from 500 to 599 are free for user use. U + 00
# to U + 99 can be used to add specific instruction extensions,
# such as bitwise operators and other useful facilities that would
# not normally be done with OS calls.

def execExtendedInstr(operand, acc):
	"""Execute any user instructions here (instruction.X_xx)"""

	if   operand == instruction.getOperand(instruction.USB): # Use Breg in next instruction
		extarch.b_flag = True # next instr will use B instead of A

	elif operand == instruction.getOperand(instruction.MUL): # multiply
		acc = extarch.b_reg * acc

	elif operand == instruction.getOperand(instruction.DIV): # divide
		##trace("acc %d breg %d" % (acc, b_reg))
		acc = extarch.b_reg / acc

	else:
		raise ValueError("Unknown EXT instr:" + str(operand))

	return acc

# END
