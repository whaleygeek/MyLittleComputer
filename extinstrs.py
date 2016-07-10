# extinstrs.py  10/07/2016  D.J.Whale
#
# Wxtended instructions that are added to the instuction set simulator

import extarch # for b_flag and b_reg
import instruction

# Runtime registration of new mnemonics in the instruction table
# This ensures that the assembler and disassembler can use the instructions
# with their proper mnemonic names, but by runtime registering them int
# does not pollute instruction.py with extended functionality

instruction.registerMnemonic("EXT", 400, False)
instruction.registerMnemonic("USB", 401, False)
instruction.registerMnemonic("MUL", 402, False)
instruction.registerMnemonic("DIV", 403, False)


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
