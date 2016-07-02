# disassembler.py  03/11/2014  D.J.Whale
#
# Disassemble an LMC output file into an assembler file

import instruction


def processMemory(memory):
	"""Dump all instructions in a memory region"""

	for addr in range(0,len(memory)):
		instr = processInstr(memory[addr])
		print(str(addr) + ":" + instr)


def processInstr(instr):
	"""Disassemble a single line into it's decimal form"""

	decimal = int(instr)
	return instruction.toString(decimal)

	
def processFile(filename, source=None, startaddr=0):
	"""Disassemble a whole file, into it's decimal form"""
	
	if source == None:
		source = []
		
	f = open(filename, "rt")
	
	for line in f.readlines():
		line = line.strip()
		i = processInstr(line)
		source.append(i)
		
	f.close()
	return source


def writeFile(source, filename, startaddr=0):
	"""Write disassembly file"""
	
	f = open(filename, "wt")
	size = len(source)
	
	for addr in range(startaddr, startaddr+size):
		f.write(source[addr].zfill(3) + "\n")
	f.close()


def main():
	import sys
	IN_NAME  = sys.argv[1] #TODO: If - or not present, use stdin
	OUT_NAME = sys.argv[2] #TODO: if - or not present, use stdout
	mem = processFile(IN_NAME)
	writeFile(mem, OUT_NAME)


if __name__ == "__main__":
	main()


# END

