# Turns hex into bin
def hextobin(c):
    num = int(c, base=16)
    b = bin(num)
    return (b[2:].zfill(4))

def 2scomp(val)
    

# parse an 8-digit string of hex into 32-bit binary string
def parse_hex8(s):
    b = ""
    for i in range(8):
        b += hextobin(s[i])
    if check == 'slow':
        if (b[0:6] == '000000'):
            print(
                f'{s[:-1]} -> {b[0:6]} {b[6:11]} {b[11:16]} {b[16:21]} {b[21:26]} {b[26:32]}'
            )
        else:
            print(f'{s[:-1]} -> {b[0:6]} {b[6:11]} {b[11:16]} {b[16:32]}')
    return b


# decides the type of instruction and prints assembly code
def instr_analysis(c):
    op_dict = {
        "001000": "addi",
        "001100": "andi",
        "001101": "ori",
        "001110": "xori",
        "000100": "beq",
        "000101": "bne",
        "000010": "j",
        "100011": "lw",
        "101011": "sw",
        "001111": "lui"
    }
    funct_dict = {
        "100000": "add",
        "100010": "sub",
        "100100": "and",
        "100101": "or",
        '100111': "nor",
        "100110": "xor",
        "101010": "slt",
        "000000": "sll",
        "000100": "sllv",
        "000010": "srl",
        "000011": "sra"
    }

    if (c[0:6] == '000000'):
        op = funct_dict[c[26:]]
        asm_dict[PC] = (f'{op} ${d}, ${s}, ${t}')
        if check == 'slow':
            print(f'{op} ${d}, ${s}, ${t}\n')
        

    elif (c[3:6] == '011'):
        op = op_dict[c[0:6]]
        asm_dict[PC] = (f'{op} ${t}, {hex(imm)}(${s})')
        if check == 'slow':
            print(f'{op} ${t}, {imm}(${s})\n')

    elif (c[0:6] == '000010'):
        op = op_dict[c[0:6]]
        asm_dict[PC] = (f'{op} {jimm}')
        if check == 'slow':
            print(f'{op} {jimm}')

    else:
        op = op_dict[c[0:6]]
        if (op == "lui"):
            asm_dict[PC] = (f'{op} ${t}, {imm}')
            if (check == 'slow'):
                print(f'{op} ${t}, {imm}\n')
        else:
            asm_dict[PC] = (f'{op} ${t}, ${s}, {imm}')
            if (check == 'slow'):
                print(f'{op} ${t}, ${s}, {imm}\n')
    return op


def do_addi():
    register[t] = register[s] + imm
    stats['ALU'] += 1


def do_andi():
    register[t] = register[s] & imm
    stats['ALU'] += 1


def do_ori():
    p = register[s]
    i = imm
    if (p<0) and (i<0):
        i += 0x10000
        p += 0x10000
    elif imm < 0:
        i += 0x10000
    elif register[s] < 0:
        p += 0x10000
    register[t] = p | i
    if register[t] > 0x7fffffff:
      register[t] -= 0x100000000
    stats['ALU'] += 1


def do_xori():
    register[t] = register[s] ^ imm
    stats['ALU'] += 1


def do_beq():
    global PC
    label_dict[str(PC + (imm*4) + 4)] = 'label'+ str(PC + (imm*4) + 4)
    if register[t] == register[s]:
        PC += (4 * imm)
    stats['Branch'] += 1


def do_bne():
    global PC
    label_dict[str(PC + (imm*4) + 4)] = 'label'+ str(PC + (imm*4) + 4)
    if register[t] == register[s]:
        return
    PC += (4 * imm)
    stats['Branch'] += 1


def do_j():
    global PC
    label_dict[str((jimm*4))] = 'label'+ str((jimm*4))
    PC = (4 * jimm) - 4
    stats['Jump'] += 1


def do_lw():
    register[t] = DM[imm + register[s]]
    stats['Memory'] += 1


def do_sw():
    DM[imm + register[s]] = register[t]
    stats['Memory'] += 1


def do_add():
    register[d] = register[s] + register[t]
    stats['ALU'] += 1


def do_sub():
    register[d] = register[s] - register[t]
    stats['ALU'] += 1


def do_and():
    register[d] = register[s] & register[t]
    stats['ALU'] += 1


def do_or():
    register[d] = register[s] | register[t]
    stats['ALU'] += 1


def do_nor():
    if register[s] < 0:
        rs = register[s] + 0x100000000
    else:
        rs = register[s]
    if register[t] < 0:
        rt = register[t] + 0x100000000
    else:
        rt = register[t]
    rd = rs | rt
    if rd > 0x7fffffff:
        register[d] = ~(rd - 0x100000000)
    else:
        register[d] = ~rd
    stats['ALU'] += 1


def do_xor():
    register[d] = register[s] ^ register[t]
    stats['ALU'] += 1


def do_slt():
    register[d] = int(register[s] < register[t])
    stats['Other'] += 1


def do_sll():
    if (register[t] < 0):
        n = register[t] + 0x100000000
    else:
        n = register[t]
    p = bin(n)[2:].zfill(32)
    for i in range(a):
        p = p[1:] + '0'
    p = int(p, 2)
    if p > 0x7fffffff:
        p -= 0x100000000
    register[d] = p
    stats['ALU'] += 1


def do_sllv():
    if (register[t] < 0):
        n = register[t] + 0x100000000
    else:
        n = register[t]
    p = bin(n)[2:].zfill(32)
    for i in range(register[s]):
        p = p[1:] + '0'
    p = int(p, 2)
    if p > 0x7fffffff:
        p -= 0x100000000
    register[d] = p
    stats['ALU'] += 1


def do_srl():
    i = register[t]
    if (i < 0):
        i += 0x100000000
    h = bin(i)[2:].zfill(32)
    for n in range(a):
        h = '0' + h[:-1]
    h = int(h, 2)
    if h > 0x7fffffff:
        h -= 0x100000000
    register[d] = h
    stats['ALU'] += 1


def do_sra():
    i = register[t]
    if (i < 0):
        i += 0x100000000
        h = bin(i)[2:].rjust(32, '1')
        for n in range(a):
            h = '1' + h[:-1]
    else:
        h = bin(i)[2:].zfill(32)
        for n in range(a):
            h = '0' + h[:-1]
    h = int(h, 2)
    if h > 0x7fffffff:
        h -= 0x100000000
    register[d] = h
    stats['ALU'] += 1


def do_lui():
    register[t] = int((mc[16:] + '0000000000000000'), 2)
    stats['ALU'] += 1


def check_registers():
    print('Registers')
    for i in range(len(register)):
        print(f'{i} : {register[i]}')


def check_memory():
    print('Data Memory')
    for i in (DM):
        if DM[i] != 0:
            print(f'DM[{hex(i)}] = {DM[i]}')


def check_stats():
    print('Instruction Statistics')
    for i in (stats):
        print(f'{i} Instructions : {stats[i]}')

def check_labels():
    print('Instruction Statistics')
    for i in (label_dict):
        print(f'{i} = {label_dict[i]}')


# Generates 32 registers
register = []
for i in range(32):
    register.append(0)

# Generates simulated data memory i.e. DM[0x2000],DM[0x2004], etc.
DM = {}
DM_index = 0x2000
while DM_index < 0x3000:
    DM[DM_index] = 0
    DM_index += 4

# dispatch table for each instruction
call = {
    "addi": do_addi,
    "andi": do_andi,
    "ori": do_ori,
    "xori": do_xori,
    "beq": do_beq,
    "bne": do_bne,
    "j": do_j,
    "lw": do_lw,
    "sw": do_sw,
    "add": do_add,
    "sub": do_sub,
    "and": do_and,
    "or": do_or,
    "nor": do_nor,
    "xor": do_xor,
    "slt": do_slt,
    "sll": do_sll,
    "srl": do_srl,
    "sra": do_sra,
    "lui": do_lui,
    "sllv": do_sllv
}

f = open('mc.txt')
lines = f.readlines()
f.close()

#Instrucion and label dictionaries for robustness
instr_dict = {}
label_dict = {}
asm_dict = {}
stats = {'ALU': 0, 'Jump': 0, 'Branch': 0, 'Memory': 0, 'Other': 0}

PC = 0
for ln in lines:
    instr_dict[PC] = ln[0:8]  # do not include \n in the end of an
    PC += 4

check = input(
    "Project 3: Type 'fast' for nonstop mode or 'slow' for step-by-step mode:\n"
)

print('\nNow reading lines from mc.txt:\n')
PC = 0

while PC <= list(instr_dict.keys())[-1]:
    instr = instr_dict[PC]
    mc = parse_hex8(instr)
    s = int(mc[6:11], 2)  # First defines any possible information
    t = int(mc[11:16], 2)
    d = int(mc[16:21], 2)
    a = int(mc[21:26], 2)
    imm = int(mc[16:], 2)
    if (imm > 0x7fff):
        imm -= 0x10000
    jimm = int(mc[11:], 2)
    operation = instr_analysis(mc)  # Defines operation based on instr_analysis
    call[operation]()  # Calls and executes correct instr. with dispatch table
    PC += 4
    if check == 'slow':
        print('PC = ', PC)
        check_registers()
        input('Press enter to continue....\n\n\n')

# Shows every register
check_registers()

# Shows changed data memory
check_memory()

# Shows intructioin statistics
check_stats()

f = open('asm_engine.txt', 'a')
for i in range(0,len(asm_dict)*4,4):
  if str(i) in label_dict:
      f.write(str(label_dict[str(i)])+':\n')
  f.write(str(asm_dict[i])+'\n')
f.close()
