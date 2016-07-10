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

def main():
	while not simulator.halt_flag:
		line = raw_input("instruction? ")

		label, operator, operand, labelref = parser.parseLine(line)
		instr = instruction.build(operator, operand)
		print("instr:" + instruction.toString(instr))

		simulator.memory[simulator.program_counter] = instr
		simulator.cycle()

		#TODO: Somehow adding b_reg functionality needs to add b display here too?
		print("  pc:"    + todec(simulator.program_counter)
			+ " a:"    + todec(simulator.accumulator)
		    ## + " b:"    + todec(99)
			+ " z:"    + str(simulator.z_flag)
			+ " p:"    + str(simulator.p_flag)
			+ " halt:" + str(simulator.halt_flag))


if __name__ == "__main__":
	main()


# END
 
	
