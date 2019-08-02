#Assignment 5 ARM Processor
import processor6_c as arm       #import classes/functions






def fetch(PC):
    temp = arm.pipeReg()
    temp.npc = PC + 1
    temp.inReg = arm.InstructionReg(instrucMem[PC])
    return temp
def decode(temp):

    if arm.pipeReg == temp.__class__:
        temp.controlU = arm.Control()  # creates control unit for this instruction (with all flags set low)
        temp.controlU.insRead(temp.inReg.opcode)  # Set control bit values

        reg.readRegs(temp.inReg.Rn, temp.inReg.Rm)  # read in values from Rn and Rm registers
        temp.readData1 = reg.readData1
        temp.readData2 = reg.readData2
    return temp



def execute(temp):

    if temp.__class__ == arm.pipeReg:

        if (temp.controlU.branch == 1):

            temp.ALU = arm.ALU(reg.X[temp.inReg.Rd], temp.inReg.Imm, temp.controlU.ALUop1, temp.controlU.ALUop2)
            # creates ALU operation for B type instructions
        elif (temp.controlU.ALUSrc == 1):
            temp.ALU = arm.ALU(temp.readData1, temp.inReg.Imm, temp.controlU.ALUop1, temp.controlU.ALUop2)
            # creates ALU operation for I type and D type instructions
        elif (temp.controlU.ALUSrc == 0):
            temp.ALU = arm.ALU(temp.readData1, temp.readData2, temp.controlU.ALUop1, temp.controlU.ALUop2)

            # creates ALU operation for R type instructions
        temp.ALU.ALUcontrol(temp.ALU.ALU_op, temp.inReg.opcode)
        # read in ALU op and set the appropriate ALU operation
        temp.ALU.exec(temp.ALU.ALU_c)  # perform ALU operation, place result in ALU.output
    return temp


def writeback(temp):
    if temp.__class__ == arm.pipeReg:
        if ((temp.controlU.memToReg == 0) and (temp.controlU.branch == 0)):
            reg.regWrite(temp.inReg.Rd, temp.ALU.output)  # write back for R type instructions
            temp.PC = temp.NPC

    return temp


def memory(temp):
    if temp.__class__ == arm.pipeReg:
        if (temp.controlU.memToReg == 1):
            if (temp.controlU.memRead == 1):  # LOAD
                print( temp.ALU.output)
                reg.regWrite(temp.inReg.Rd, reg.dataMem[temp.ALU.output])  # load data memory value to Rd
                print('Data Memory:\n', reg.dataMem)
            elif (temp.controlU.memWrite == 1):  # STORE
                reg.dataMem[temp.ALU.output] = reg.X[temp.inReg.Rd]  # load Rd value to calculated Data Memory Address
                print('Data Memory:\n', reg.dataMem)

            temp.PC = temp.NPC  # go to next sequential instrution

        elif (temp.controlU.branch == 1):  # Check for branch opcode
            if (temp.controlU.uncond == 1):  # B instruction
                temp.PC = temp.PC + temp.inReg.Imm  # PC <- PC+addr
                print("PC: " + str(temp.PC))
                print('-----------------------\n')

            elif (temp.ALU.zero == 1):  # if R[Rd]==0
                temp.PC = temp.PC + temp.inReg.Imm  # PC <- PC+addr
                print('Registers:\n', (reg.X))
                print("PC: " + str(temp.PC))
                print('-----------------------\n')

            else:
                print('Registers:\n', (reg.X))
                print("PC: " + str(temp.PC))  # if CBZ result is false, continue sequentially
                temp.PC = temp.NPC
    return temp

def runtime(instrucMem):
    # ###RUN TIME
    #instatiate pipeline registers
    decode_in = 0
    execute_in = 0
    writeback_in = 0
    memory_in = 0
    PC = 0
    cycle_count = 0
    instruction_count = 0

    while PC<len(instrucMem)+5:
        print('cycle: '+str(cycle_count))
        
        # STOP READING FOR INSTRUCTIONS IF THERE AREN'T ANY LEFT
        if PC < len(instrucMem):
            fetch_out = fetch(PC)
            instruction_count += 1
        
        decode_out = decode(decode_in)
        execute_out = execute(execute_in)
        memory_out = memory(memory_in)
        writeback_out = writeback(writeback_in)

        # this block of code ensures that the processor doesn't repeat the same instruction
        if writeback_out.__class__()== arm.pipeReg:
                if writeback_out.PC > PC:
                        PC = writeback_out.PC
                else:   #
                        PC += 1
        else:
                PC += 1


        decode_in = fetch_out
        execute_in = decode_out
        memory_in = execute_out
        writeback_in = memory_out



        cycle_count += 1
        print('Registers:\n',(reg.X))
        print("PC: "+str(PC))
        print('-----------------------\n')
    print('END OF FILE')

    print("CPI = CYCLES / INSTRUCTIONS:")
    print(cycle_count)
    print(instruction_count)
    print(cycle_count/instruction_count)
#############################
# ### INITIAL
# load Instruction Memory
reg = arm.Registers()     #create register object with Registers and Data Memory
reg.dataMem[0]=10
reg.dataMem[1]=13       #load in data memory array values

#Example 5
f = open("example5.txt", 'r')
instrucMem = f.readlines()
reg.X[1]=3
reg.X[2]=17
reg.X[11]=9
reg.X[19]=42
runtime(instrucMem)

#Example 7
reg.clearReg()
f = open("example7.txt", 'r')
instrucMem = f.readlines()
reg.X[1]=3
reg.X[2]=17
reg.X[11]=9
reg.X[19]=42
runtime(instrucMem)

#Example 8
reg.clearReg()
f = open("example8.txt", 'r')
instrucMem = f.readlines()
reg.X[1]=3
reg.X[2]=17
reg.X[11]=9
reg.X[19]=42
runtime(instrucMem)
