# extarch.py  10/07/2016  D.J.Whale
#
# Extended architecture features
# The b_reg and a b_flag is added.
# This makes it easier to implement two-operand MUL and DIV instructions
# even with the limited space in the instruction set format.

#TODO: Add copious comments about this decorator system,
#it is not something that beginner python programs will be familiar with.

import instruction
import hltinstrs
import ioinstrs
import extinstrs

b_flag = False
b_reg  = 0

def bmux(old_execute):
    """Add the b_reg architectural feature in as a multiplexor around execute()"""
    def new_execute(operator, operand, acc):
        global b_flag, b_reg
        # If b_flag is set, read and write the B rather than the A
        if b_flag:
            acc = b_reg

        # EXECUTE
        acc = old_execute(operator, operand, acc)

        # WRITE BACK
        instr = instruction.build(operator, operand)
        if b_flag and instr != instruction.USB:
            b_reg = acc
            b_flag = False

        return acc

    return new_execute # the patched (decorated) execute function with b_flag functionality


def hlt_instrs(old_execute):
    """Insert new HLT instructions into instruction simulation"""
    def new_execute(operator, operand, acc):
        if   operator == instruction.HLT: # 0xx
            if operand != 0: # HLT 00 is actually HLT
                return hltinstrs.execHLTInstr(operand, acc)
        return old_execute(operator, operand, acc)

    return new_execute


def io_instrs(old_execute):
    """Insert new IO instructions into instruction simulation"""
    def new_execute(operator, operand, acc):
        if   operator == instruction.IO:
            instr = instruction.build(operator, operand)
            if instr != instruction.INP and instr != instruction.OUT:
                return ioinstrs.execIOInstr(operand, acc)
        return old_execute(operator, operand, acc)

    return new_execute


def ext_instrs(old_execute):
    """Insert new EXT instructions into instruction simulation"""
    def new_execute(operator, operand, acc):
        if   operator == instruction.EXT:
            return extinstrs.execExtendedInstr(operand, acc)
        return old_execute(operator, operand, acc)

    return new_execute


# END
