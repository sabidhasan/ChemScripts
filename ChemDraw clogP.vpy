#Version 0.2	Jan 10, 2017
#changed version for ChemScript 16
#####################
#    IMPORT LIBS    #
#####################
#TO--DO : add commenting for everything

import sys
import com.dotmatics.vortex.mol2img.Mol2Img
import com.dotmatics.vortex.util.Util as Util
import subprocess
import time
from os.path import *
import os

#variable for writing file
write_out = ""
home_folder = os.path.expanduser("~")

#####################
# EXPORT STRUCTURES #
#####################
column = vtable.findColumnWithName("CD clogP", 1, vortex.DOUBLE)
#To--DO add check for empty file
for r in range(0, vtable.getRealRowCount()):
  mol = vtable.molFileManager.getMolFileAtRow(r)
  smiles_key = vortex.getMolProperty(mol, 'smiles')
  #TO--DO : If isempty(smiles_key): smileskey = "N/A error", so that the python file for 
  #calcuylations doesnt crap out and stop reading midway through, also go to python file and
  #if theres something that has "N/A error" then clogP should not be calcualted!!
  write_out = write_out + smiles_key + "\n"
#create file
fl = open(os.path.join(home_folder, "structures.txt"), 'w')
fl.write(write_out)
fl.close()

######################
#    CALCULATIONS    #
######################
#run the calculator
#Check for python installation TO--DO
#Attempt to make relative path for testfile TO--DO
p = subprocess.Popen(['C:\\Python32\\python.exe', 'C:\\Users\\ahasan\\vortex\\scripts\\clogPcalc.py'], stdout=subprocess.PIPE)
output = p.communicate()[0]
#this will create a file that has clogP values one by one
#wait based on length of file - this can be fudged more, but it seems reasonabel...
wait_time = 3 + int(vtable.getRealRowCount() / 333)
time.sleep(wait_time)

#open the newlyt create file 
fl = open(os.path.join(home_folder, "structureslogp.txt"))

#read the things back in
for r in range(0, vtable.getRealRowCount()):
  clogp = fl.readline()
  column.setValueFromString(r, clogp)
fl.close()
#deelte the files
os.remove(os.path.join(home_folder, "structureslogp.txt"))
os.remove(os.path.join(home_folder, "structures.txt"))

vtable.fireTableStructureChanged()