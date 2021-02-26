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
#FIRST THE I-TYPE INSTR
    if(s[0:6]=='001000'):
        op = 'addi'
        print(f'op = {s[0:6]}, addi instruction.')
    elif(s[0:6]=='001100'):
        op = 'andi'
        print(f'op = {s[0:6]}, andi instruction.')
    elif(s[0:6]=='001101'):
        op = 'ori'
        print(f'op = {s[0:6]}, ori instruction.')
    elif(s[0:6]=='001110'):
        op = 'xori'
        print(f'op = {s[0:6]}, xori instruction.')
#THEN THE BRANCH/JUMP INSTR
    elif(s[0:6]=='000100'):
        op = 'beq'
        print(f'op = {s[0:6]}, beq instruction.')
    elif(s[0:6]=='000101'):
        op = 'bne'
        print(f'op = {s[0:6]}, bne instruction.')
    elif(s[0:6]=='000010'):
        op = 'j'
        print(f'op = {s[0:6]}, j instruction.')
#THEN THE LOAD/STORE INSTR
    elif(s[0:6]=='100011'):
        op = 'lw'
        print(f'op = {s[0:6]}, lw instruction.')
    elif(s[0:6]=='101011'):
        op = 'sw'
        print(f'op = {s[0:6]}, sw instruction.')
#FINALLY THE R-TYPE INSTR
    elif(s[0:6]=='000000'):
        if (s[26:]=='100000'):
            op = 'add'
        elif (s[26:]=='100010'):
            op = 'sub'
        elif (s[26:]=='100100'):
            op = 'and'
        elif (s[26:]=='100101'):
            op = 'or'
        elif (s[26:]=='100110'):
            op = 'xor'                            
        elif (s[26:]=='101010'):
            op = 'slt'
        elif (s[26:]=='000000'):
            op = 'sll'
        elif (s[26:]=='000010'):
            op = 'srl'
        elif (s[26:]=='000011'):
            op = 'sra'
        print(f'op = {s[0:6]}, {op} instruction.')
    else:
        print(f'op = {s[0:6]}, unknown instruction.\n')
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

