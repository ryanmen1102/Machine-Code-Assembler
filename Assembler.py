# File: Assembler.py
# Author: Ryan Mendoza
# Date: 4/7/2020
# Section: 511
# E-mail: ryanmen1102@tamu.edu
# Description:
# Assembler for .asm to .hack

import sys

if len(sys.argv) != 2:
    print("Please enter a file name")
    sys.exit()

with open(sys.argv[1], "r") as inFile:
    with open(sys.argv[1][:-4] + ".hack", "w") as outFile:

        comp = {"0":"0101010", "1":"0111111", 
                "-1":"0111010", "D":"0001100", 
                "A":"0110000", "M":"1110000", 
                "!D":"0001101", "!A":"0110001", 
                "!M":"1110001", "-D":"0001111", 
                "-A":"0110011", "-M":"1110011", 
                "D+1":"0011111", "A+1":"0110111", 
                "M+1":"1110111", "D-1":"0001110", 
                "A-1":"0110010", "M-1":"1110010", 
                "D+A":"0000010", "D+M":"1000010", 
                "D-A":"0010011", "D-M":"1010011", 
                "A-D":"0000111", "M-D":"1000111", 
                "D&A":"0000000", "D&M":"1000000", 
                "D|A":"0010101", "D|M":"1010101"}
                
        dest = {"M":"001", "D":"010", 
                "MD":"011", "A":"100",
                "AM":"101", "AD":"110",              
                "AMD":"111"}
                
        jump = {"JGT":"001", "JEQ":"010", 
                "JGE":"011", "JLT":"100",
                "JNE":"101", "JLE":"110",              
                "JMP":"111"}
                
        symb = {"SP":0, "LCL":1, 
                "ARG":2, "THIS":3,
                "THAT":4, "R0":0,
                "R1":1, "R2":2,
                "R3":3, "R4":4,
                "R5":5, "R6":6,
                "R7":7, "R8":8,
                "R9":9, "R10":10,
                "R11":11, "R12":12,
                "R13":13, "R14":14,
                "R15":15, "SCREEN":16384,
                "KBD":24576}
        
        address = 0
        for line in inFile:
        
            line = line.replace(" ", "")
            line = line.strip()
            for i in range(len(line)):
                if (line[i] == "/"):
                    line = line[:i]
                    break
                    
            if (line[:2] == "//"):
                continue
            elif (line == ""):
                continue
            elif (line[0] == "("):
                symb.update({line[1:-1]:address})
                continue
                
            address += 1
        
        inFile.seek(0)
        address = 16
        for line in inFile:
        
            line = line.replace(" ", "")
            line = line.strip()
            for i in range(len(line)):
                if (line[i] == "/"):
                    line = line[:i]
                    break
            
            if (line[:2] == "//"):
                continue
            elif (line == "" or line[0] == "("):
                continue
            elif (line[0] == "@"):
                if (line[1:].isdigit()):
                    outFile.write("0" + bin(int(line[1:]))[2:].zfill(15) + "\n")
                else:
                    try:
                        outFile.write("0" + bin(symb[line[1:]])[2:].zfill(15) + "\n")
                    except:
                        symb.update({line[1:]:address})
                        address += 1
                        outFile.write("0" + bin(symb[line[1:]])[2:].zfill(15) + "\n")
            else:
                destCheck = False
                destLoc = 0
                jumpCheck = False
                jumpLoc = 0
                
                for i in range(len(line)):
                    if (line[i] == '='):
                        destCheck = True
                        destLoc = i
                    elif (line[i] == ';'):
                        jumpCheck = True
                        jumpLoc = i
                    
                if (destCheck and jumpCheck):
                    outFile.write("111" + comp[line[destLoc+1:jumpLoc]] + dest[line[:destLoc]] + jump[line[jumpLoc+1:]] + "\n")
                elif jumpCheck:
                    outFile.write("111" + comp[line[:jumpLoc]] + "000" + jump[line[jumpLoc+1:]] + "\n")
                elif destCheck:
                    outFile.write("111" + comp[line[destLoc+1:]] + dest[line[:destLoc]] + "000" + "\n")
                else:
                    outFile.write("111" + comp[line] + "000000" + "\n")