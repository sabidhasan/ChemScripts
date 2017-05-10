#Version 5,3 change notes: added comments, removed customized training, make atoms col string
#fixed bug with erroneous method supplied in subprocess

#####################
#    IMPORT LIBS    #
#####################
import com.dotmatics.vortex.mol2img.Mol2Img
import sys
import com.dotmatics.vortex.util.Util as Util
import subprocess

if Util.getPlatform() == Util.PlatformIsWindows:
  sys.path.append(vortex.getVortexFolder() + '\\modules\jythonconsole')
  sys.path.append(vortex.getVortexFolder() + '\\modules\jythonlib')
else:
  sys.path.append(vortex.getVortexFolder() + '/modules/jythonconsole')
  sys.path.append(vortex.getVortexFolder() + '/modules/jythonlib')

# Get path to current sdf
sdfFile = com.dotmatics.vortex.mol2img.Mol2Img.getFileForPropertyCalculation(vtable)

#####################
#  CALCULATE PROPS  #
#####################
#This version does not use logP training library
#So this should work on other users' computers
#USE THESE PARAMETERS TO GET TRAINED LOG D
# '-m', 'user', '--trainingid', 'finaltraininglogp'

p = subprocess.Popen(['C:\\Program Files\\ChemAxon\\MarvinBeans\\bin\\cxcalc.bat', 'pka', '-b', '1', '-a', '1', 'logp', '-t', 'logpmicro', 'logd', '-H', '7.4',sdfFile], stdout=subprocess.PIPE)
output = p.communicate()[0]

#####################
#    MAKE COLUMNS   #
#####################
lines = output.split('\n')
colName = lines[0].split('\t')
for c in colName:
  if "logD" in c:
    column = vtable.findColumnWithName("logD", 1, vortex.DOUBLE)
    colName[5] = "logD"
    #colName[5] is because fifth column is logD, as calculated from ChemAxon
  elif "atoms" in c:
    #Needs to be STRING  because atoms has "commas" in it
    column = vtable.findColumnWithName("atoms", 1, vortex.STRING)
  else:
    column = vtable.findColumnWithName(c, 1, vortex.DOUBLE)
vtable.fireTableStructureChanged()

#####################
#    WRITE OUTPUT   #
#####################
#we must use r+1, because first row of lines is actually
#column names. otherwise properties will be offset by 1
for r in range(0, vtable.getRealRowCount()):
	vals = lines[r+1].split('\t')
	for j in range(0, len(vals)):
		column = vtable.findColumnWithName(colName[j], 0)
		column.setValueFromString(r, vals[j])
vtable.fireTableStructureChanged()