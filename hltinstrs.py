# hltinstrs.py  10/07/2016  D.J.Whale
#
# Extra HLT instructions for the instruction set simulator
# These are good for implementing OS calls

# Might not be needed, unless you need mnemonic support in addition to
# generic form HLT 01 HLT 02 etc

# TODO: runtime registration of these instructions into the instruction.py tables
# will need to be done here, so that instruction.py is not polluted with non standard
# features. (but only if they have names, if they are just HLT 01.. HLT 99 then
# the instruction.py won't need changing)



# 000 is HLT but 001..099 are undefined. So, by modelling 0xx as a HLT
# and making HLT mean HLT 00, we can add HLT 01..HLT 99.
# Halts are useful for adding OS calls, for example, and might take
# a value in the accumulator to parameterise them, or the value in
# the accumulator might be a memory address that stores a block of
# parameters.

def execHLTInstr(operand):
	"""Execute any halt instructions here (instruction.T_XX)"""

	raise ValueError("Unknown HLT instr:" + str(operand))
	# DEFINE USER HLT INSTRUCTIONS HERE


# END
