
plainText = '01010101' 
keyString = '1011000111'

# Create Tuples of permutation numbers
Permutate10 = (3,5,2,7,4,10,1,9,8,6)
Permutate8 = (6,3,7,4,8,5,10,9)
ExpansionPermutation = (4,1,2,3,2,3,4,1)
InitialPermutation = (2,6,3,1,4,8,5,7)
FinalPermutation = (4, 1, 3, 5, 7, 2, 8, 6) #Inverse of IP
p4 = (2,4,3,1)

# S-Box Creation
sboxes0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
sboxes1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
sboxesModified = [[3,1,3,2],[3,2,1,0],[0,2,1,3],[1,0,3,2]]

def permutate(keyString, permutation):
    permutatedString = [] 
    for index in permutation:
        index = int(index)       
        permutatedString.append(keyString[index-1]) 
        permString = ''.join(map(str, permutatedString))
    return permString


def keyReturn(keyString):   
    length = len(keyString)
    midLength = int(length/2) 
    global keyL 
    keyL = keyString[:midLength] 
    global keyR
    keyR = keyString[midLength:] 
    return keyL, keyR


def keyShift(key, numberofShifts):
    bitString = str(key) 
    shiftedKey = str(bitString[numberofShifts:]) + str(bitString[:numberofShifts]) 
    return shiftedKey

def stringCombine(shiftedKeyL, shiftedKeyR):
    combinedLRKey = shiftedKeyL + shiftedKeyR
    return combinedLRKey

def permEP(IP, sk1orsk2):
    keyReturn(IP) 
    EpermR = permutate(keyR, ExpansionPermutation) 
    xored = int(EpermR, 2) ^ int(sk1orsk2, 2)
    xored = bin(xored); xored = str(xored); xored = xored[2:]
    keyReturn(xored)
    print("sk1orsk2:", sk1orsk2)


def sboxCreation(input0, input1):
    global s0
    s0 = []
    global s1
    s1 = []
    for s00 in input0:
        s00 = int(s00)
        s0.append(s00)
    for s01 in input1:
        s01 = str(s01)
        s1.append(s01)
    s0 = ''.join(map(str, s0))#Join the elements of the list into one string
    s1 = ''.join(map(str, s1))#Join the elements of the list into one string

    while len(s0) < 4:
        s0 = str(0) + s0 #pad leading 0 
    while len(s1) < 4:
        s1 = str(0) + s1 #pad leading 0 
    print("s0:", s0)
    print("s1:", s1)

#SBox Manipulations, takes in the output of sbox creation 
def sbox(s0, s1):
    #Row0
    a = (str(s0[0])); a = int(a)
    b = (str(s0[3])); b = int(b)
    sbox0Row = sboxesModified[a][b]
    ab = str(a) + str(b)
    ab = int(ab, 2)

    #Col0
    c = str(s0[1]);  c= int(c)
    d = str(s0[2]); d = int(d)
    sbox0Col = sboxesModified[c][d]
    cd = str(c) + str(d)
    cd = int(cd,2)

    sboxRow = sboxesModified[ab][cd]
    sboxRow = bin(sboxRow)
    sboxRow = str(sboxRow[2:])

    #Row1
    e = (str(s1[0])); e = int(e)
    f = (str(s1[3])); f = int(f)
    sbox1Row = sboxes1[e][f]
    ef = str(e) + str(f)
    ef = int(ef, 2)

    #Col1
    g = str(s1[1]); g = int(g)
    h = str(s1[2]); h = int(h)
    sbox1Col = sboxes1[g][h]
    gh = str(g) + str(h)
    gh = int(gh, 2)

    sboxRow1 = sboxes1[ef][gh]
    sboxRow1 = bin(sboxRow1)
    sboxRow1 = str(sboxRow1[2:])
    global sbox0
    sbox0 = stringCombine(sboxRow, sboxRow1)
    while len(sbox0) < 4:
        sbox0 = str(0) + sbox0 #pad leading 0 
    print("sbox", sbox0)


def keys(keyString, numberofShifts):
    global sk1 
    p10 = permutate(keyString, Permutate10) 
    keyReturn(p10) 
    ShiftkL = keyShift(keyL, numberofShifts) 
    ShiftkR = keyShift(keyR, numberofShifts) 
    combStr = stringCombine(ShiftkL, ShiftkR) 
    sk1 = permutate(combStr, Permutate8) 
    print("sk1:", sk1)

    global sk2 
    Shiftk2L = keyShift(ShiftkL, numberofShifts+1) 
    Shiftk2R = keyShift(ShiftkR, numberofShifts+1) 
    combStr2 = stringCombine(Shiftk2L, Shiftk2R)  
    sk2 = permutate(combStr2, Permutate8) 
    print("sk2:", sk2)
    return sk1, sk2

def fk1(IPorSwap, sk1orsk2):
    permEP(IP, sk1orsk2)
    sboxCreation(keyL, keyR) 
    sbox(s0, s1) 
    print("If round 1, sk will be sk1. If round 2, sk will be sk2")
    print("sk1orsk2 :", sk1orsk2)
    perm4 = permutate(sbox0, p4)

    
    xoredp4 = int(keyL, 2) ^ int(perm4, 2)
    xoredp4 = bin(xoredp4); xoredp4 = str(xoredp4); xoredp4 = xoredp4[2:]
    while len(xoredp4) < 4:
        xoredp4 = str(0) + xoredp4  
    print("xoredp4:", xoredp4)
    keyReturn(xoredp4)
    keyReturn(IP)
    print("keyR:", keyR)
    global fk1Out
    fk1Out = stringCombine(xoredp4,keyR)
    keyReturn(fk1Out)
    global swap
    swap = stringCombine(keyR,keyL)

    print("fk1Out:", fk1Out)
    print("Swap:", swap)
    print('')
    print('')
    return swap



keys(keyString, 1)

IP = permutate(plainText, InitialPermutation)
print("Initial Permutation:", IP)
print("")
print("-----------------------------------")
print("Function fk using subkey 1")
print("")
fk1(IP, sk1)
print("-----------------------------------")


print("Second Round of fk function using subkey2")
print("")
fk1(swap, sk2)
print("------------------------------------")


cipher = permutate(swap, FinalPermutation)
print("Cipher Text:", cipher)
print('')


print("------------------------------------")
print("Decryption")
print("")
fk1(cipher, swap)
fk1(fk1Out, keyString)
