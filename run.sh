MON="DGEBA"
CRO="PACM"
SYS="system"
BOND="sys-bond"
INI="init"
DES="mol2-test"
FF="oplsaa.ff"
IN="/mnt/disk2/IncludeFiles"
PYTHON="ReadMol2"

SIZE="20" #Have test for 200 monomers, needs 120A
NUM1="4" #Monomer/Crosslinker number
NUM2="2"

cd ..
rm -rf $DES/$NUM1$MON-$NUM2$CRO
mkdir $DES/$NUM1$MON-$NUM2$CRO
cd $DES/$NUM1$MON-$NUM2$CRO

cp $IN/packmol.inp .
cp $IN/$MON.mol2 .
cp $IN/$CRO.mol2 .

#If start from a mol2 file, this step helps to convert

obabel -i mol2 -o pdb -fi $MON.mol2 -O $MON.pdb
obabel -i mol2 -o pdb -fi $CRO.mol2 -O $CRO.pdb

sed -i "s/MMM/${MON}/g" packmol.inp
sed -i "s/CCC/${CRO}/g" packmol.inp
sed -i "s/FFF/${SYS}/g" packmol.inp
sed -i "s/SIZE/${SIZE}/g" packmol.inp
sed -i "s/NUM1/${NUM1}/g" packmol.inp
sed -i "s/NUM2/${NUM2}/g" packmol.inp
packmol < packmol.inp

obabel -i pdb -o mol2 -fi $SYS.pdb -O $SYS.mol2 -d

#######
#Need to add bond creation bash here
cp $IN/$PYTHON/*py .
cp $IN/$PYTHON/input.txt .
sed -i "s/III/${SYS}.mol2/g" input.txt
sed -i "s/OOO/${BOND}.mol2/g" input.txt

python3 Main.py
#######

obabel -i mol2 -o mol2 -fi $BOND.mol2 -O $INI.mol2 -h
echo "" >> $INI.mol2 #add a blank line at the end of the file
$SOFT/topolbuild1_3/src/topolbuild -dir $DATA/../ -ff gaff -n $INI
rm *py

mkdir gmx
mv $INI.gro gmx
mv $INI.top gmx
mv posre$INI.itp gmx
cd gmx

sed "s/\#include\ \"ff${INI}/\#include\ \"${FF}\/forcefield/g" $INI.top > topol.top
sed -i "s/\#include\ \"spc/\#include\ \"$FF\/spc/g" topol.top
sed -i "s/\#include\ \"ions/\#include\ \"$FF\/ions/g" topol.top

cp $IN/$PYTHON/*.py .
python3 procTOP.py
mv topol.top topol.top~
mv topol.top-bk topol.top
rm *py

cp $IN/em.mdp .
cp $IN/nvt.mdp .

#editconf -f $INI.gro -o box.gro -box $SIZE $SIZE $SIZE
editconf -f $INI.gro -o box.gro -box 5 5 5
grompp -f em.mdp -c box.gro -o min -maxwarn 10
mpirun -np 1 mdrun_mpi -deffnm min -ntomp 1 -v
grompp -f nvt.mdp -c min.gro -o nvt -maxwarn 10
mpirun -np 1 mdrun_mpi -deffnm nvt -ntomp 1 -v

mkdir sim_result
mv min.gro sim_result
mv nvt.gro sim_result
mv nvt.trr sim_result
cp topol.top sim_result
cd sim_result
cp $IN/$PYTHON/*.py .
python3 readGRO.py
rm *py
