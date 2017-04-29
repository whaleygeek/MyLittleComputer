# ioinstrs.py  10/07/2016  D.J.Whale
#
# Add extra IO instructions to the instruction set simulator

import instruction

# Runtime registration of generic form
# you can add specific mnemonic names here if you want,
# see the example in extinstrs.py to see how to do it in a way that
# does not pollute instruction.py with optional features.

instruction.registerMnemonic("IO", 900, False)


# INP and OUT are already handled in simulator.py, and never delegated here.

# 901=INP and 902=OUT, but 900 and 903..999 are not used.
# These undefined instructions are therefore useful to use to define
# other types of IO, such as GPO for general purpose output, GPI for
# general purpose input, AIN for analog input, and other I/O
# related things that would not warrant a HLT for an OS call.
# they could be done as User instrutions (U) but it's handy to group
# all the I/O together into a set of instructions.


def execIOInstr(operand, acc):
	"""Execute any user IO instructions here (instruction.IO_xx)"""

	print("exec IO instr %d" % str(operand))
	# DEFINE NEW IO INSTRUCTIONS HERE
	return acc


# END
