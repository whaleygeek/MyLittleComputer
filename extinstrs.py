# extinstrs.py  10/07/2016  D.J.Whale
#
# Wxtended instructions that are added to the instuction set simulator

import extarch # for b_flag and b_reg
import instruction

# Runtime registration of new mnemonics in the instruction table
# This ensures that the assembler and disassembler can use the instructions
# with their proper mnemonic names, but by runtime registering them int
# does not pollute instruction.py with extended functionality

# Define numeric values
instruction.EXT    = 400 # Extension instruction
instruction.USB    = 401 # use B register
instruction.MUL    = 402 # multiply A and B
instruction.DIV    = 403 # divide A and B
## 00, 05..99 not used yet

instruction.no_operands += [instruction.EXT, instruction.USB, instruction.MUL, instruction.DIV]

# Define string values
instruction.operators[instruction.EXT] = "EXT"
instruction.operators[instruction.USB] = "USB"
instruction.operators[instruction.MUL] = "MUL"
instruction.operators[instruction.DIV] = "DIV"


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
