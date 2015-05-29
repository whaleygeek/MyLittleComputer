# interactive.py  03/11/2014  D.J.Whale
#
# A simple interactive shell

import instruction
import assembler
import disassembler
import parser
import simulator

def todec(n):
	return str(n).zfill(3)

simulator.memory = [0 for i in range(99)]
	
while not simulator.halt:
	line = raw_input("instruction? ")

	label, operator, operand, labelref = parser.parseLine(line)
	instr = instruction.build(operator, operand)

	simulator.memory[simulator.program_counter] = instr
	simulator.cycle()
	
	print("pc:"    + todec(simulator.program_counter)
	    + " a:"    + todec(simulator.accumulator)
	    + " z:"    + str(simulator.z_flag)
	    + " p:"    + str(simulator.p_flag)
	    + " halt:" + str(simulator.halt))
	    
# END
 
	
