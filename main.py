# char of hex digit -> a string of 4 binary bits.
def hextobin(c):
    num = int(c, base=16)
    b = bin(num)
#    print(f'c is {c}, num is {num}, b[2:].zfill(4) is {b[2:].zfill(4)}')
    return(b[2:].zfill(4))

# parse an 8-digit string of hex into 32-bit binary string 
def parse_hex8(s):
    b = ""
    for i in range(8):
        b += hextobin(s[i])
    if(b[0:6]=='000000'):
        print(f'{s[:-1]} -> {b[0:6]} {b[6:11]} {b[11:16]} {b[16:21]} {b[21:26]} {b[26:32]}')
    else:
        print(f'{s[:-1]} -> {b[0:6]} {b[6:11]} {b[11:16]} {b[16:32]}')
    return b

def instr_analysis(s):
    # decide if this is an addi instruction
    op_dict = {
    "001000":"addi",
    "001100":"andi",
    "001101":"ori",
    "001110":"xori",
    "000100":"beq",
    "000101":"bne",
    "000010":"j",
    "100011":"lw",
    "101011":"sw"
    }
    funct_dict = {
    "100000":"add",
    "100010":"sub",
    "100100":"and",
    "100101":"or",
    "100110":"xor",
    "101010":"slt",
    "000000":"sll",
    "000010":"srl",
    "000011":"sra"
    }

    if(s[0:6]=='000000'):
        op = funct_dict[s[26:]]
        print(f'funct = {s[26:]}, {funct_dict[s[26:]]} instruction.')
    else:
        op = op_dict[s[0:6]]
        print(f'op = {s[0:6]}, {op_dict[s[0:6]]} instruction.\n')
    return op

def user_input():
    h = input("give me an instruction in 8-digit hex: \n")
    mc = parse_hex8(h)
    return mc
    
def read_file():
    f = open('mc.txt')
    print('\nNow reading lines from mc.txt:\n')
    for line in f:
        mc = parse_hex8(line)
        op = instr_analysis(mc)
        full_instr(op,mc)
    f.close()

def full_instr(operation,b):
    imm = int(b[16:32],2)
    if (imm > 32767):         #simple 2s complement checker
        imm = imm - 65536
    if(operation == 'lw' or operation == 'sw'):
        print(f'{operation} ${int(b[11:16],2)}, {imm}(${int(b[6:11],2)})\n\n')
    elif(b[0:6]=='000000'):
        print(f'{operation} ${int(b[16:21],2)}, ${int(b[6:11],2)}, ${int(b[11:16],2)}\n\n')
    else:
        print(f'{operation} ${int(b[11:16],2)}, ${int(b[6:11],2)}, {imm}\n\n')

read_file()

