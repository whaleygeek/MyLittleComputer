# extarch.py  10/07/2016  D.J.Whale
#
# Extended architecture features
# The b_reg and a b_flag is added.
# This makes it easier to implement two-operand MUL and DIV instructions
# even with the limited space in the instruction set format.

#TODO: Add copious comments about this decorator system,
#it is not something that beginner python programs will be familiar with.

import instruction

b_flag = False
b_reg  = 0

def bmux(old_execute):

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


# END
