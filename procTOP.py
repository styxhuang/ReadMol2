# -*- coding: utf-8 -*-
"""
v0.0: Created on Sat Mar 17 17:44:39 2018
After create the bond, since the bond length sometimes is longer than usual, and gromacs cannot recognize.
After we transfer mol2 file to gro file, some bond/angle/dihedral coefficient may miss. This file helps
us to fill in those blank.

@author: HuangMing
"""

import pandas as pd

def CheckIndex(df, keyword):
    index = df.index[df[0].str.contains(keyword) == True].tolist()
    return index

def ChkAnglePair(anglesIndex, TOP):
    string = TOP.iloc[anglesIndex].str.split()[0]
    pairs = [string[-3], string[-2], string[-1]]
    return pairs

def ChkErRow(df):
    index = []
    criNum = df.iloc[0][0].count(' ')
    
    for i in range(len(df)):
        spaceNum = df.iloc[i][0].count(' ')
        if spaceNum > criNum + 7:
            index.append(df.iloc[i]['index'])
    return index

def UpdateRow(index, df): #For now only bond section needs to be updated, or the coefficient is for bond
    a = '1'             
    b = '0.14480'
    c = '319658.'
    for i in range(len(index)):
        tmp = df.iloc[index[i]].str.split()[0]
        print(tmp)
        str1 = "{:>8}{:>6}{:>4}{:>12}{:>13}{:>8}{:>7}{:>6}".format(tmp[0],tmp[1],a , b, c, tmp[2], tmp[3],tmp[4])
        print(str1)
        df.iloc[index[i]] = str1
    return df

def DropRows(index, df): #For the empty angle and dihedral, for now I just delete them
    tmp = df
    for i in range(len(index)):
        tmp = tmp.drop([index[i]])
    return tmp
def BondProc(TOP):
    bondStartIdx = CheckIndex(TOP, 'bonds')
    bondEndIdx = CheckIndex(TOP, 'constraints')
    
    bondsTOP = TOP.iloc[bondStartIdx[0]+2: bondEndIdx[0]].reset_index()
    bondIdx = ChkErRow(bondsTOP)
    
    df = UpdateRow(bondIdx, TOP)
    
    return df

def AngleProc(TOP):
    angleStartIdx = CheckIndex(TOP, 'angles')
    angleEndIdx = CheckIndex(TOP, 'dihedrals')
    
    anglesTOP = TOP.iloc[angleStartIdx[0]+2:angleEndIdx[0]].reset_index()
    anglesIndex = ChkErRow(anglesTOP)
    finalDF = DropRows(anglesIndex, TOP)
#    pairs = []
#    for i in range(len(anglesIndex)):
#        pairs.append(ChkAnglePair(anglesIndex[i], TOP))
#        TOP.drop([anglesIndex[i]])
    return finalDF

def DihedralProc(df):
    dihIdx = CheckIndex(df, 'dihedral')
    index = list(range(dihIdx[0], dihIdx[1]))
    finalDF = DropRows(index, df)
    return finalDF

def ExportTOP(filename, df):
    f = open(filename, 'w')
    for i in range(len(df)):
        line = df.iloc[i][0] + '\n'
        if '[ atoms ]' in line:
            line = '\n' + line
        f.write(line)
    f.close()
    
topName = "topol.top"
TOP = pd.read_csv(topName, sep="\n", header=None)
a = TOP
BondProc = BondProc(TOP)
angleProc = AngleProc(BondProc)
finalProc = DihedralProc(angleProc)
ExportTOP('topol.top-bk', finalProc)
