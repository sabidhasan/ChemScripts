from sys import *
from ChemScript16 import *
import os
from os.path import *

home_folder = os.path.expanduser("~")

dd = open(os.path.join(home_folder , 'structures.txt'))
dd2 = open(os.path.join(home_folder, 'structureslogp.txt'), 'w')

#TO--DO : use diff method for reading files, so it doesnt end midway if theres an empty line
liness = dd.readlines()

for i in range(0, len(liness)):
  #print(liness[i])
  m = StructureData.LoadData(liness[i], 'smiles')
  dd2.write(str(m.PartitionCoefficient)+"\n")
#m.ChemicalName gets canoncial name from chemdraw
dd.close()
dd2.close()