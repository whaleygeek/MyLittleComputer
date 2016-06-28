# symtab.py  23/04/2015  D.J.Whale
#
# A symbol table to keep track of labels and their values and usage addresses

import instruction

defines = {} # label->addr
fixups  = {} # addr->labelref


def trace(msg):
    print(str(msg))


def is_defined(label):
    return label in defines


def define(label, addr):
    """Define a new label"""

    #trace("define:" + str(label) + "=" + str(addr))
    if defines.has_key(label):
        raise ValueError("Label already defined:" + label + "=" + str(defines[label]))
    defines[label] = addr


def use(label, refaddr):
    """Use (refer to) a label"""

    if not defines.has_key(label):
        #trace("use:" + str(label) + " at:" + str(refaddr))
        fixlater(refaddr, label)
        addrref = None
    else:
        addrref = defines[label]
        #trace("use:" + str(label) + " at:" + str(refaddr) + " fixup:" + str(addrref))
        # already known, so get it's value

    return addrref


def get(label):
    """Get the value associated with a label"""

    if not defines.has_key(label):
        raise ValueError("Unknown label:" + str(label))
    return defines[label]


def fixlater(refaddr, label):
    """Defer the fixup of a reference to a label at this address, til later"""

    fixups[refaddr] = label


def fixup(memory):
    """Fixup all addresses"""

    # Find all usages that did not previously have a define
    for refaddr in fixups:
        label = fixups[refaddr]
        realaddr = defines[label]

        #trace("fixup refaddr:" + str(refaddr) + " for label:" + label + " to:" + str(realaddr))

        instr1 = memory[refaddr]
        instr2 = instruction.setOperand(instr1, realaddr)

        #instr1_str = instruction.toString(instr1)
        #instr2_str = instruction.toString(instr2)
        #trace("fixup: old:" + str(instr1_str) + " new:" + str(instr2_str))
        memory[refaddr] = instr2


def dumpLabels():
    """Dump the whole symbol table to stdout"""

    print("LABELS:")
    for label in defines:
        print("  " + label + ":" + str(defines[label]))


def dumpFixups():
    """Dump all fixups in the symbol table to stdout"""

    print("FIXUPS:")
    for refaddr in fixups:
        print("  " + str(refaddr) + ":" + fixups[refaddr])


# END
