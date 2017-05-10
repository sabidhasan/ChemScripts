# flag duplicates
#

# Vortex imports. not needed but used by default
import com.dotmatics.vortex.util.Util as Util
import com.dotmatics.vortex.mol2img.jni.genImage as genImage
import com.dotmatics.vortex.mol2img.Mol2Img as mol2Img
import math


PotencyColumn = vtable.findColumnWithName("NAFLUX-H-Nav1.6",0)
pICColumn = vtable.findColumnWithName("pIC50",1)

rows = vtable.getRealRowCount()

for r in range(0, int(rows)):
	potency = -1*math.log(PotencyColumn.getValue(r)/1000000,10)
	pICColumn.setValueFromString(r, str(potency))

vtable.fireTableStructureChanged