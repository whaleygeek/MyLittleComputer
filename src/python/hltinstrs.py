# hltinstrs.py  10/07/2016  D.J.Whale
#
# Extra HLT instructions for the instruction set simulator
# These are good for implementing OS calls

# You can use mnemonic forms instead of HLT 01 HLT 02 etc if you want,
# but look at extinstrs.py to see how to runtime register new
# mneumonics in the instruction table from here, in a way that does
# not pollute the instruction.py with unnecessary optional detail.

# HLT 00 (HLT) is handled in simulator.py and never delegated here.

# 000 is HLT but 001..099 are undefined. So, by modelling 0xx as a HLT
# and making HLT mean HLT 00, we can add HLT 01..HLT 99.
# Halts are useful for adding OS calls, for example, and might take
# a value in the accumulator to parameterise them, or the value in
# the accumulator might be a memory address that stores a block of
# parameters.

def execHLTInstr(operand, acc):
	"""Execute any halt instructions here (instruction.T_XX)"""

	print("executed HLT %d" % str(operand))
	# DEFINE USER HLT INSTRUCTIONS HERE

	return acc


# END
