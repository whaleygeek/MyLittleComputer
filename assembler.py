# assembler.py  03/11/2014  D.J.Whale
#
# Read a file and assemble it into a numeric representation

import parser
import instruction
import symtab
import io

# Set to True if you want addresses prefixed into the output file
PREFIX_ADDR = False

def trace(msg):
	print(str(msg))


def parse(filename, memory=None, startaddr=0):
	"""parse a whole file, storing each instruction in memory"""
	
	addr = startaddr
	f = open(filename, "rt")
	if memory == None:
		memory = {}

	for line in f.readlines():
		line = line.strip()
		label, operator, operand, labelref = parser.parseLine(line)
		#trace("parse:" + line + "=" + str((label, operator, operand, labelref)))
		if line == "" or (label == None and operator == None):
			# must be a comment
			continue # go round to next line

		instr = instruction.build(operator, operand)
		#trace("  created:" + str(instr))


		# dump any collected labels
		if label != None:
			symtab.define(label, addr)

		if labelref != None:
			addrref = symtab.use(labelref, addr)
			if addrref != None:
				# address of label already known, so fixup instruction operand now
				#trace("info: Fixing label reference:" + labelref + " to:" + str(addrref))
				instr = instruction.setOperand(instr, addrref)

		# Store in memory
		memory[addr] = instr

		# Move to next memory location
		addr += 1
		
	f.close()
	return memory
	
	
def write(memory, filename):
	"""write the contents of memory to the file"""
	
	f = open(filename, "wt")
	size = len(memory)
	startaddr = min(memory)

	for addr in range(startaddr, startaddr+size):
		#if PREFIX_ADDR:
		#	io.write(addr, file=f)
		io.write(memory[addr], file=f)
	f.close()
  

def main():
	import sys
	IN_NAME = sys.argv[1]
	OUT_NAME = sys.argv[2]

	m = parse(IN_NAME)
	symtab.fixup(m)

	##symtab.dumpLabels()
	##symtab.dumpFixups()

	##loader.showmem(m)

	##disassembler.disassemble(m)

	write(m, OUT_NAME)


if __name__ == "__main__":
	#TODO#### get encoder settings from command line args use io.configure()
	main()


# END

