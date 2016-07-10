# ioinstrs.py  10/07/2016  D.J.Whale
#
# Add extra IO instructions to the instruction set simulator

# Might not be needed, unless you need mnemonic support in addition to
# generic form IO 01 IO 02 etc

#TODO: Also, runtime registration of these 3 instrutions into the instruction.py tables
# will need to be done here, so that instruction.py is not polluted with non standard
# features. But only if the instructions need mnemonic names other than IO 03 etc

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
	# DEFINE NEW IO INSTRUCTIONS HERE


# END
