# parser.py  03/11/2014  D.J.Whale
#
# Parse an input program file

import instruction

def labelFromString(s):
	"""Work out if this operand is a label or not"""

	# Is it numeric?
	try:
		operand = int(s)
		return operand, None # just a normal number
	except:
		pass

	# Must be a label
	return None, s # A labelref


def parseLine(line):
	"""parse a line into an instruction"""

	# Ignore lines that are comments
	line = line.strip()
	if line.startswith('#'):
		return None, None, None, None # whole-line comment

	# Strip off end of line comment
	try:
		commentpos = line.index('#')
		line = line[:commentpos]
		line = line.strip()
	except:
		pass

	# Ignore lines with no instruction on them
	parts    = line.split(" ")
	if len(parts) == 0: # empty line
		return None

	# Split line into [label] [operator] [operand]
	label    = None
	operator = None
	operand  = None
	labelref = None

	if len(parts) == 1: # (label) or (operator)
		if instruction.isOperator(parts[0]): # (operator)
			operator = instruction.operatorFromString(parts[0])
		else: # (label) (operator)
			label    = parts[0]

	elif len(parts) == 2: # (label operator) or (operator operand)
		if instruction.isOperator(parts[0]): # (operator operand)
			operator          = instruction.operatorFromString(parts[0])
			operand, labelref = labelFromString(parts[1])

		else: # (label operator)
			label    = parts[0]
			operator = instruction.operatorFromString(parts[1])

	elif len(parts) == 3: # (label operator operand)
		label             = parts[0]
		operator          = instruction.operatorFromString(parts[1])
		operand, labelref = labelFromString(parts[2])

	# DAT or instruction?
	if operator == instruction.DAT:
		operator = operand
		operand  = None

	return label, operator, operand, labelref

# END

