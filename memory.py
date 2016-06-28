# memory.py  21/08/2015  D.J.Whale
#
# Placeholder for an abstraction which models the memory of the computer.
# This abstraction will be required, so that we can implement sparse memory
# larger memories and other schemes later without breaking the real model.

#TODO first step is to move all memory[] accesses from all other python code
#into here, accessed via memory.* abstraction first.
#then later on, we can change the implementation independently of it's use.

#This also opens up the way for us to have a remote memory access interface
#into the simulator for pre-loading the memory with known patterns before the
#simulator runs, eg by passing a memory initialiser list on the command line
#where it sparsely loads specific addresses to specific values. Useful for
#bootloading images. Can then also do memory dump in the debugger and other
#useful things.