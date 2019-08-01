import processor6_c as arm


# ### INITIAL
# load Instruction Memory
f = open("assignment5.txt", 'r')
instrucMem = f.readlines()
PC = 0
reg = arm.Registers()     #create register object with Registers and Data Memory
reg.dataMem[0]=10
reg.dataMem[1]=13       #load in data memory array values


def fetch():
    temp = arm.pipeReg()
    temp.npc = PC + 1
    temp.intruction_Reg = arm.InstructionReg(instrucMem[PC])

    return temp


def decode(temp):
    temp.inReg
    temp.controlU = arm.Control()  # creates control unit for this instruction (with all flags set low)
    temp.controlU.insRead(temp.inReg.opcode)  # Set control bit values

    reg.readRegs(temp.inReg.Rn, temp.inReg.Rm)  # read in values from Rn and Rm registers
    return temp


def execute(temp):
    if (temp.controlU.branch == 1):
        temp.ALU = arm.ALU(reg.X[temp.inReg.Rd], temp.inReg.Imm, temp.controlU.ALUop1, temp.controlU.ALUop2)
        # creates ALU operation for B type instructions
    elif (temp.controlU.ALUSrc == 1):
        temp.ALU = arm.ALU(reg.readData1, temp.inReg.Imm, temp.controlU.ALUop1, temp.controlU.ALUop2)
        # creates ALU operation for I type and D type instructions
    elif (temp.controlU.ALUSrc == 0):
        temp.ALU = arm.ALU(reg.readData1, reg.readData2, temp.controlU.ALUop1, temp.controlU.ALUop2)

        # creates ALU operation for R type instructions
    temp.ALU.ALUcontrol(temp.ALU.ALU_op, temp.inReg.opcode)
    # read in ALU op and set the appropriate ALU operation
    temp.ALU.exec(temp.ALU.ALU_c)  # perform ALU operation, place result in ALU.output
    return temp


def writeback(temp):
    if ((temp.controlU.memToReg == 0) and (temp.controlU.branch == 0)):
        reg.regWrite(temp.inReg.Rd, temp.ALU.output)  # write back for R type instructions
        temp.PC = temp.NPC

    return temp


def memory(temp):
    if (temp.controlU.memToReg == 1):
        if (temp.controlU.memRead == 1):  # LOAD
            reg.regWrite(temp.inReg.Rd,
                         reg.dataMem[temp.ALU.output])  # load data memory value to Rd
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