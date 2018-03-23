# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 14:34:14 2018

@author: HuangMing
"""

import pandas as pd
import AtomClass as Atom
import BondClass as Bond
import readMOL2 as MOL2
import os
def CheckIndex(df, keyword):
    index = df.index[df[0].str.contains(keyword) == True].tolist()
    return index

def ChkAtomType(atomName, atomType):
    if atomName == 'C':
        if atomType == 'opls_145' or atomType == "opls_166":
            return 'C.ar'
        else:
            return 'C.3'
    elif atomName == 'N':
        return 'N.3'
    elif atomName == 'O':
        return 'O.3'
    elif atomName == 'H':
        return 'H'

def RemoveRows(df, keyword):
    tmp = df[df[0].str.contains(keyword) == False].reset_index(drop=True)
    tmp = tmp.iloc[:len(df)-1].reset_index(drop=True)
    return tmp

def InitData(GRO, TOP):
   
    atomStartIdx = CheckIndex(TOP, 'atoms')
    atomEndIdx = CheckIndex(TOP, '; total molecule charge')
    
    bondStartIdx = CheckIndex(TOP, 'bonds')
    bondEndIdx = CheckIndex(TOP, 'constraints')
    
    atomsTop = TOP.iloc[atomStartIdx[0]+2:atomEndIdx[0]]
    atomsGro = GRO.iloc[2:].iloc[:-1]
    
    bondsTop = TOP.iloc[bondStartIdx[0]+2:bondEndIdx[0]].reset_index(drop=True)
#Remove the hydrogen needs to update the atom index in the bond session, may be complexed    
#    atomsTopNoH = RemoveRows(atomsTop, " H ")
#    atomsGroNoH = RemoveRows(GRO.iloc[2:], "H ").iloc[:-1]
 
    return atomsGro, atomsTop, bondsTop

def AtomInfoInput(groData, topData):
    atoms = []
    arIndex = []
    for i in range(len(groData)):
        oriGRO = groData.iloc[i].str.split().tolist()[0] #from pandas datafrom to list
        oriTOP = topData.iloc[i].str.split().tolist()[0]
        
        #From gro file input
        atom = Atom.AtomsInfo()
        atom.setIndex(oriGRO[2])
        atom.setAtomName(oriGRO[1])
        atom.setPos([oriGRO[3],oriGRO[4],oriGRO[5]])
        atom.setSubName(oriGRO[0])
        
        #From top file input
        atomType = ChkAtomType(oriGRO[1], oriTOP[1])
        atom.setAtomType(atomType)
        atom.setSubID(oriTOP[2])
        atom.setCharge(oriTOP[6])        
        if atomType == 'C.ar':
            arIndex.append(atom.getIndex())
        atoms.append(atom)

    for i in range(len(atoms)):
        atoms[i].outputData()
        
    return atoms, arIndex

def BondInfoInput(topData, arIndex):
    bonds=[]
    print("tst-", arIndex)
    for i in range(len(topData)):
        oriTOP = topData.iloc[i].str.split().tolist()[0]
        bond = Bond.BondsInfo()
        bond.setIndex(i+1)
        bond.setAtom(oriTOP[0], oriTOP[1])
        atomTmp = [oriTOP[0], oriTOP[1]] 
        if any(i in atomTmp for i in arIndex):
            #print("right!")
            bond.setBondType("ar")
        else:
            bond.setBondType(oriTOP[2])
        bonds.append(bond)
    return bonds

def ExportMol2(TOP, atomsNum, bondsNum, atoms, bondList):
    atomList = atoms[0]
    name = TOP.iloc[-1][0].split()[0]
    outputName = 'stp_1.mol2'
    content = [' {:} {:} {:} {:} {:}'.format(atomsNum, bondsNum, 0, 0, 0), 'SMALL', 'GASTEIGER']
    MOL2.ExportMOL2(name, outputName, content, atomList, bondList)
    
###############################################################################
groName = "min.gro"
topName = "topol.top"

GRO = pd.read_csv(groName, sep="\n", header=None)
TOP = pd.read_csv(topName, sep="\n", header=None)

a = InitData(GRO, TOP)
atoms = AtomInfoInput(a[0],a[1])
bonds = BondInfoInput(a[2], atoms[1])
atomsNum = len(atoms[0])
bondsNum = len(bonds)
ExportMol2(TOP, atomsNum, bondsNum, atoms, bonds)
    
