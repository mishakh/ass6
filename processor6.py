#Assignment 5 ARM Processor
# import processor6_c as arm       #import classes/functions
from steps import *


#instatiate pipeline registers
decode_in = arm.pipeReg()
execute_in = arm.pipeReg()
writeback_in = arm.pipeReg()
memory_in = arm.pipeReg()

# ###RUN TIME
while PC<len(instrucMem):
        
        fetch_out = fetch()
        decode_out = decode(decode_in)
        execute_out = execute(execute_in)
        memory_out = memory(memory_in)
        writeback_out = writeback(writeback_in)

        # this block of code ensures that the processor doesn't repeat the same instruction
        if writeback_out.PC > PC:
                PC = writeback_out.PC
        else:   #
                PC += 1

        decode_in = fetch_out
        execute_in = decode_out
        memory_in = execute_out
        writeback_in = memory_out



        print('Registers:\n',(reg.X))
        print("PC: "+str(PC))
        print('-----------------------\n')
print('END OF FILE')
