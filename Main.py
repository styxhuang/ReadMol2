# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 18:43:40 2018

@author: HuangMing
"""

import readMOL2
import argparse

####################################################################  
if __name__ == "__main__":
#    filename = "system.mol2"
#    outputName = "tst_2.mol2"
    option = ['filename', 'outputName', 'monomer length', 'crosslinking length', 
          'monomer reactive atom index', 'crosslinker reactive atom index', 'cutoff', 
          'bonds generate each round']
    f = open('input.txt')
    for line in f:
        if option[0] in line:
            a = line.split("=")
            filename = a[1].strip('\n')
            print("filename: ", filename)
        elif option[1] in line:
            a = line.split("=")
            outputName = a[1].strip('\n')
            print("outname: ", outputName)
        elif option[2] in line:
            a = line.split("= ")
            monLen = int(a[1])
            print("monLen: ", monLen)
        elif option[3] in line:
            a = line.split("=")
            crosLen = int(a[1])
            print("crosLen: ", crosLen)
        elif option[4] in line:
            str1 = line.split("= ")[1].strip('\n').split()
            a = [int(str1[0]), int(str1[1])]
            print(a)
            monR = a
            print("monR: ", monR)
        elif option[5] in line:
            a = line.split("= ")[1].strip('\n').split()
            print(a)
            crosR = a
            print("crosR: ", crosR)
        elif option[6] in line:
            a = line.split("=")
            cutoff = float(a[1])
            print("cutoff: ", cutoff)
        elif option[7] in line:
            a = line.split("=")
            bondsNum = int(a[1])
            print("bondsNum: ", bondsNum)
    f.close()
#########################################
#   Inert for future implementation of option inuput
#    parser = argparse.ArgumentParser()
#    parser.add_argument("-b", help="Largest generated bonds number", type=int)
#    args = parser.parse_args()
#    bondTotal = args.bonds
#########################################
    readMOL2.main(filename, outputName, monLen, crosLen, monR, crosR, cutoff, bondsNum)