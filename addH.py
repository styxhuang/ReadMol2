# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 21:36:16 2018

@author: HuangMing
"""

import pandas as pd
import readMOL2 as MOL
import AtomClass as Atom
import BondClass as Bond

def ExportMol2(atomsNum, bondsNum, atomList, bondList):
    name = "system.pdb"
    outputName = 'aH-stp1.mol2'
    content = [' {:} {:} {:} {:} {:}'.format(atomsNum, bondsNum, 0, 0, 0), 'SMALL', 'GASTEIGER']
    MOL.ExportMOL2(name, outputName, content, atomList, bondList)

#########################################################################
atomList = []
bondList = []

arList = []   
mol2Name = "dH-aH.mol2"
f = open(mol2Name)
content = f.readlines()
ORI = pd.read_csv(mol2Name, sep="\n", header=None)
start_atom_idx = content.index("@<TRIPOS>ATOM\n")
start_bond_idx = content.index("@<TRIPOS>BOND\n")

atomsDataframe = ORI.iloc[start_atom_idx:start_bond_idx-1][0].str.split()
bondsDataframe = ORI.iloc[start_bond_idx:][0].str.split()

for i in range(len(atomsDataframe)):
    a = Atom.AtomsInfo()
    atom = atomsDataframe.iloc[i]             
    for ii in range(len(atom)): #loop each atom's info
        MOL.InfoInput(ii, a, atom)            
    atomList.append(a)

for i in range(len(bondsDataframe)):
    b = Bond.BondsInfo()
    bond = bondsDataframe.iloc[i]
    for ii in range(len(bond)):
        MOL.BondInfoInput(ii, b, bond)
    bondList.append(b)

for i in range (len(atomList)):
    if atomList[i].getAtomType() == "C.ar":
        #print("tst-1", atomList[i].getAtomType())
        #print("tst-2", atomList[i].getIndex())
        arList.append(atomList[i].getIndex())

for i in range(len(bondList)):
    atoms = bondList[i].getAtom()
    if any(i in atoms for i in arList):
        bondList[i].setBondType('ar')
        print('tst-1',bondList[i].getIndex())

atomsNum = len(atomList)
bondsNum = len(bondList)
ExportMol2(atomsNum, bondsNum, atomList, bondList)
#print("tst-3:", arList)