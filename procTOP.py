# -*- coding: utf-8 -*-
"""
v0.0: Created on Sat Mar 17 17:44:39 2018
After create the bond, since the bond length sometimes is longer than usual, and gromacs cannot recognize.
After we transfer mol2 file to gro file, some bond/angle/dihedral coefficient may miss. This file helps
us to fill in those blank.

@author: HuangMing
"""

import pandas as pd

#Following are Gaff data
dictBond = {
        'C-N': '1, 0.14700, 268278.'
        }

dictAngle = { #TODO: keep update angle coefficient
        'N-C-N': '1, 110.380, 553.9616',
        'C-O-C': '1, 117.600, 522.1632',
        'C-C-N': '1, 110.380, 553.9616',
        'C-N-C': '1, 110.900, 535.5520',
        'N-C-C': '1, 110.380, 553.9616',
        'H-C-N': '1, 109.920, 413.3792',
        'C-N-H': '1, 109.920, 394.1328'
        }

dictDihedral = {
        
        }

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
def ProcessString(index, df, category='bond'):
    a = '1'             
    b = '0.14700'
    c = '268278.'
    for i in range(len(index)):
        tmp = df.iloc[index[i]].str.split()[0]
        if category == 'bond':
            str1 = "{:>8}{:>6}{:>4}{:>12}{:>13}{:>8}{:>7}{:>6}".format(tmp[0],tmp[1],a , b, c, tmp[2], tmp[3],tmp[4])
            print(str1)
            df.iloc[index[i]] = str1
        elif category == 'angle':
            tmp1 = tmp[-3:]
            tmp1 = ''.join(tmp1)
            if tmp1 in dictAngle:
                coeff = dictAngle[tmp1].split(',')
            str1 = "{:>6}{:>6}{:>6}{:>4}{:>12}{:>12}{:>6}{:>7}{:>7}{:>6}".format(tmp[0],tmp[1],tmp[2], coeff[0], coeff[1], coeff[2], tmp[3], tmp[-3], tmp[-2],tmp[-1])
            print(str1)
            df.iloc[index[i]] = str1
        else:
            print("Unknow data type")

def UpdateRow(index, df, category='bond'): #For now only bond section needs to be updated, or the coefficient is for bond
    if category == 'bond':
        ProcessString(index, df, 'bond')
    if category == 'angle':
        ProcessString(index, df, 'angle')
    return df

def DropRows(index, df): #For the empty dihedral, for now I just delete them
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
    finalDF = UpdateRow(anglesIndex, TOP, 'angle')
    return finalDF

def DihedralProc(df):
    dihIdx = CheckIndex(df, 'dihedral')
    index = list(range(dihIdx[0], dihIdx[1]))
    finalDF = DropRows(index, df)
    return finalDF

def ConstraintsProc(df):
    constrainStartIdx = CheckIndex(df, 'constraints')
    constrainEndIdx = CheckIndex(df, 'pairs')
    print('tst-1:', constrainStartIdx)
    print('tst-2:', constrainEndIdx)
    print('tst-3:', df.iloc[constrainStartIdx])
    print('tst-4:', df.iloc[constrainEndIdx])
    for i in range(constrainStartIdx[0], constrainEndIdx[0]):
        print('tst-5:', df.iloc[i])
        df = df.drop([i])
    return df    
    

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
DihedralProc = DihedralProc(angleProc)
finalProc = ConstraintsProc(DihedralProc)
ExportTOP('topol.top-bk', finalProc)
