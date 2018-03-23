# ReadMol2
Generate the polymer crosslinking network starts from a mol2 file to a gro file

# version 0.1
Prerequirement software packages:
1. Gromacs 
2. Topoltools
3. openBabel

Has been implement following usage:
1. Import all information from a MOL2 file
    1) Atoms information
        - atoms index
        - atoms name
        - atoms coordinate
        - atoms sub-ID
        - atoms sub-Name
        - atoms chain number
        - atoms charge
    2) Bonds information
        - bonds index
        - bonds atoms
        - bonds type (mainly separate into 2, for single bond, type '1', for aromatic ring, type 'ar')

2. Convert MOL2 to GROMACS readable file (.gro & .top)
    - using topoltool do this

3. After minization, convert .gro & .top back to MOL2 file

