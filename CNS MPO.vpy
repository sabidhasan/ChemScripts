import com.dotmatics.vortex.mol2img.Mol2Img
import sys
import com.dotmatics.vortex.util.Util as Util

sys.path.append(vortex.getVortexFolder() + '\\modules\jythonconsole')
sys.path.append(vortex.getVortexFolder() + '\\modules\jythonlib')

import subprocess

# Get the path to the currently open sdf file
sdfFile = com.dotmatics.vortex.mol2img.Mol2Img.getFileForPropertyCalculation(vtable)

#Properties needed for MPO score calculation
#clogP    clogD   TPSA    MW      HBD     pKa

# Run cxcalc on the file
p = subprocess.Popen(['C:\\Program Files\\ChemAxon\\MarvinBeans\\bin\\cxcalc.bat', 'logp', '-t', 'logpmicro', 'logd', '-H', '7.4', 'polarsurfacearea', 'mass', 'pka','-b', '1',sdfFile], stdout=subprocess.PIPE)
output = p.communicate()[0]

#Calculate HBD from Vortex, becuase we dont have Licence for Marvin
hbd = [float(i) for i in vortex.getMolProperty(vtable.getStructureTexts(), 'HBD')]
colhbd = vtable.findColumnWithName('HBD', 1, vortex.DOUBLE)
colhbd.setDoubles(hbd)

# Create new columns in table if needed
lines = output.split('\n')
colName = lines[0].split('\t')
for c in colName:
  if "logD" in c:
    column = vtable.findColumnWithName("logD", 1, vortex.DOUBLE)
    colName[2] = "logD"
  elif "Polar" in c:
    column = vtable.findColumnWithName("TPSA", 1, vortex.DOUBLE)
    colName[3] = "TPSA"
  elif "logP" in c:
    column = vtable.findColumnWithName("logP", 1, vortex.DOUBLE)
    colName[1] = "logP"
  else:
    column = vtable.findColumnWithName(c, 1, vortex.DOUBLE)
colhbd = vtable.findColumnWithName('HBD', 1, vortex.DOUBLE)
  
# Parse the output
rows = lines[1:len(lines)]
for r in range(0, vtable.getRealRowCount()):
	vals = rows[r].split('\t')
	for j in range(0, len(vals)):
		column = vtable.findColumnWithName(colName[j], 0)
		column.setValueFromString(r, vals[j])

#calculate T scores
CNSMPO = vtable.findColumnWithName("CNS MPO Score", 1, vortex.DOUBLE)

logpt = vtable.findColumnWithName("logP T0", 1, vortex.DOUBLE)
logpcol = vtable.findColumnWithName("logP", 0)

logdt = vtable.findColumnWithName("logD T0", 1, vortex.DOUBLE)
logdcol = vtable.findColumnWithName("logD", 0)

masst = vtable.findColumnWithName("MW T0", 1, vortex.DOUBLE)
masscol = vtable.findColumnWithName("Mass", 0)

hbdt = vtable.findColumnWithName("HBD T0", 1, vortex.DOUBLE)
hbdcol = vtable.findColumnWithName("HBD", 0)

pkat = vtable.findColumnWithName("Basic pKa T0", 1, vortex.DOUBLE)
pkacol = vtable.findColumnWithName("bpKa1", 0)

tpsat = vtable.findColumnWithName("TPSA T0", 1, vortex.DOUBLE)
tpsacol = vtable.findColumnWithName("TPSA", 0)

for r in range(0, vtable.getRealRowCount()): 
#Set hydrogen bonding 
  colhbd.setValueFromString(r, str(hbd[r]))

  if logpcol.getValue(r) < 3:
    logptval = 1
  elif logpcol.getValue(r) > 5:
    logptval = 0
  else:
    logptval = 1 + (-1*((logpcol.getValue(r)-3)/2))
  logpt.setValueFromString(r, str(logptval))
  
  if logdcol.getValue(r) < 2:
    logdtval = 1
  elif logdcol.getValue(r) > 4:
    logdtval = 0
  else:
    logdtval = 1 + (-1*((logdcol.getValue(r)-2)/2))
  logdt.setValueFromString(r, str(logdtval))

  if masscol.getValue(r) < 360:
    masstval = 1
  elif masscol.getValue(r) > 500:
    masstval = 0
  else:
    masstval = 1 + (-1*((masscol.getValue(r)-360)/140))
  masst.setValueFromString(r, str(masstval))

  if hbdcol.getValue(r) < 0.5:
    hbdtval = 1
  elif hbdcol.getValue(r) > 3.5:
    hbdtval = 0
  else:
    hbdtval = 1 + (-1*((hbdcol.getValue(r)-0.5)/3))
  hbdt.setValueFromString(r, str(hbdtval))

  if pkacol.getValue(r) < 8:
    pkatval = 1
  elif pkacol.getValue(r) > 10:
    pkatval = 0
  else:
    pkatval = 1 + (-1*((pkacol.getValue(r)-8)/2))
  pkat.setValueFromString(r, str(pkatval))
  
  if tpsacol.getValue(r) < 20:
    tpsatval = 0
  elif tpsacol.getValue(r) > 120:
    tpsatval = 0
  elif tpsacol.getValue(r) < 40:
    tpsatval = (tpsacol.getValue(r)-20)/20
  elif tpsacol.getValue(r) < 90:
    tpsatval = 1
  else:
    tpsatval = 1 + (-1*((tpsacol.getValue(r)-90)/30))
  tpsat.setValueFromString(r, str(tpsatval))

#Caclculate Totla CNS MPO SCORE
  cnsscore = logptval + logdtval + masstval + hbdtval + pkatval + tpsatval
  CNSMPO.setValueFromString(r, str(cnsscore))

vtable.fireTableStructureChanged