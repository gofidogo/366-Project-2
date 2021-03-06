# Turns hex into bin
def hextobin(c):
    num = int(c, base=16)
    b = bin(num)
    return (b[2:].zfill(4))

# parse an 8-digit string of hex into 32-bit binary string
def parse_hex8(s):
    b = ""
    for i in range(8):
        b += hextobin(s[i])
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
        "101011": "sw"
    }
    funct_dict = {
        "100000": "add",
        "100010": "sub",
        "100100": "and",
        "100101": "or",
        "100110": "xor",
        "101010": "slt",
        "000000": "sll",
        "000010": "srl",
        "000011": "sra"
    }

    if (c[0:6] == '000000'):
        op = funct_dict[c[26:]]
        print(f'{op} ${d}, ${s}, ${t}\n')
    elif (c[4:6] == '11'):
        op = op_dict[c[0:6]]
        print(f'{op} ${t}, {imm}(${s})\n')
    elif (c[0:6] == '000010'):
        op = op_dict[c[0:6]]
        print(f'{op}')
    else:
        op = op_dict[c[0:6]]
        print(f'{op} ${t}, {s}, {imm}\n')
    return op

def do_addi():
    register[t] = register[s] + imm
def do_andi():
    register[t] = register[s] & imm
def do_ori():
    register[t] = register[s] | imm
def do_xori():
    register[t] = register[s] ^ imm
def do_beq():
    global PC
    if register[t] == register[s]:
      PC += (4*imm)
def do_bne():
    global PC
    if register[t] != register[s]:
      PC += (4*imm)
def do_j():
    global PC
    PC = (4*jimm)
def do_lw():
    register[t] = DM[imm + register[s]]
def do_sw():
    DM[imm + register[s]] = register[t]
def do_add():
    register[d] = register [s] + register[t]
def do_sub():
    register[d] = register [s] - register[t]
def do_and():
    register[d] = register [s] & register[t]
def do_or():
    register[d] = register [s] | register[t]
def do_xor():
    register[d] = register [s] ^ register[t]
def do_slt():
    register[d] = register [s] < register[t]
def do_sll():
    register[t] = register[s] << a
def do_srl():
    register[t] = register[s] >> a


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
  "addi":do_addi,
  "andi":do_andi,
  "ori":do_ori,
  "xori":do_xori,
  "beq":do_beq,
  "bne":do_bne,
  "j":do_j,
  "lw":do_lw,
  "sw":do_sw,
  "add":do_add,
  "sub":do_sub,
  "and":do_and,
  "or":do_or,
  "xor":do_xor,
  "slt":do_slt,
  "sll":do_sll,
  "srl":do_srl
  }


f = open('mc.txt')
lines = f.readlines()
f.close()

#Instrucion and label dictionaries for robustness
instr_dict = {}
label_dict = {}
PC = 0
for ln in lines:
    instr_dict[PC] = ln[0:8]  # do not include \n in the end of an
    PC += 4

print('\nNow reading lines from mc.txt:\n')
PC = 0
while PC <= list(instr_dict.keys())[-1]:
    instr = instr_dict[PC]
    mc = parse_hex8(instr)
    s = int(mc[6:11],2)      # First defines any possible information
    t = int(mc[11:16],2)
    d = int(mc[16:21],2)
    a = int(mc[21:26],2)
    imm = int(mc[16:],2)
    if (imm > 0x7fff):
      imm -= 0x10000
    jimm = int(mc[11:],2)
    operation = instr_analysis(mc)  # Defines operation based on instr_analysis
    call[operation]()       # Calls and executes correct instr. with dispatch table
    PC += 4


# Shows every register
print('Registers')
for i in range(len(register)):
  print(f'{i} : {register[i]}')

# Shows changed data memory
print('Data Memory')
for i in (DM):
  if DM[i] != 0:
    print(f'DM[{hex(i)}] = {DM[i]}')

