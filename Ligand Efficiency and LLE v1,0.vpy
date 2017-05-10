# Vortex Scripting Example
#
# This example shows how the functionality of Vortex can be extended
# using the inbuilt scripting support. The scripting is implemented using
# Jython (which is a Java implementation of the popular Python programming
# language).
#
# Save the file in ${user.home}\vortex\scripts to test it via the Scripts
# menu on the main toolbar of Vortex.
#
# A number of things are predefined for convenience
#	vortex	- the current vortex instance that the script is running in
#	vws		- the active workspace within the vortex instance
#	vtable	- the table contained in the active workspace
#
# Additionally a number of packages are imported with aliases
#	com.dotmatics.vortex		- v
#	com.dotmatics.vortex.Layout	- layout
#
# Author: Mike Hartshorn
# Copyright (C) dotmatics Limited, 2008
#
# Modified by Steve Wesolowski to include LLE, 2016

if vws is None:
	vortex.alert("You must load a workspace to use this script")
else:
	import math

	# Get the list of column names for the table
	columnNames = vtable.getColumnNames()

	# Create a set of tabs for the different parts of the user interface
	tabs = javax.swing.JTabbedPane()

	# Create the main part of the user interface
	content = javax.swing.JPanel()

	layout.fill(content, javax.swing.JLabel("IC50 column"), 0, 0)

	columnsIC50 = javax.swing.JComboBox(columnNames)
	
	layout.fill(content, columnsIC50, 1, 0)

	ic50factors = [1.0, 1.e-3, 1.e-6, 1.e-9, math.log(10)]
	ic50labels = ["M", "mM", "uM", "nM", "pIC50"]
	
	ic50units = javax.swing.JComboBox(ic50labels)

	ic50units.setSelectedIndex(2)
	
	layout.fill(content, ic50units, 1, 5)

	layout.fill(content, javax.swing.JLabel("IC50 units"), 0, 5)
	
	layout.fill(content, javax.swing.JLabel("Heavy atom count column"), 0, 10)

	layout.fill(content, javax.swing.JLabel("LogP (or LogD) column"), 0, 15)
	
	columnsLogP = javax.swing.JComboBox(columnNames)
	
	layout.fill(content, columnsLogP, 1, 15)

	columnsMW = javax.swing.JComboBox(columnNames)

	layout.fill(content, columnsMW, 1, 10)

#	layout.fill(content, javax.swing.JLabel("Generate HAC from #MW?"), 0, 40)

#	generateHAC = javax.swing.JCheckBox()

#	generateHAC.setSelected(0)

#	layout.fill(content, generateHAC, 1, 40)

#	layout.fill(content, javax.swing.JLabel("Conversion factor"), 0, 50)

#	conversion = javax.swing.JTextField("13.6")

#	layout.fill(content, conversion, 1, 50, layout.HORIZONTAL)

	layout.fill(content, javax.swing.JLabel("Ligand Efficiency column"), 0, 60)

	lename = javax.swing.JTextField("LE")

	layout.fill(content, lename, 1, 60)

	layout.fill(content, javax.swing.JLabel("Ligand Lipophilicity Efficiency column"), 0, 70)

	llename = javax.swing.JTextField("LLE")

	layout.fill(content, llename, 1, 70)


	layout.fill(content, javax.swing.JLabel("Add plot?"), 0, 80)

	addplot = javax.swing.JCheckBox()

	addplot.setSelected(1)

	layout.fill(content, addplot, 1, 80)

	# Add the column content to the tab panel
	tabs.addTab("Columns", content)


	# show the dialog and process the input if the user presses ok
	ret = vortex.showInDialog(tabs, "Calculate Ligand Efficiencies")

	if ret == vortex.OK:
		mwcolumn = vtable.getColumn(columnsMW.getSelectedIndex())
		ic50column = vtable.getColumn(columnsIC50.getSelectedIndex())
		
		logPcolumn = vtable.getColumn(columnsLogP.getSelectedIndex())

		lecolumn = vtable.findColumnWithName(lename.getText(), 1)
		lecolumn.setType(vortex.DOUBLE)

		llecolumn = vtable.findColumnWithName(llename.getText(), 1)
		llecolumn.setType(vortex.DOUBLE)
		
		rows = vtable.getRealRowCount()
		
		units = ic50units.getSelectedIndex()
		
		ic50factor = ic50factors[units]
				
#		conversionFactor = float(conversion.getText())
		
		
		for r in range(0, rows):
			mw = mwcolumn.getValue(r)
			
			#if generateHAC.isSelected():
			#mw = mw/conversionFactor
			
			ic50 = ic50column.getValue(r)
			logP = logPcolumn.getValue(r)

				#le = 0.001
			
			if abs(mw) > 1.e-3:
				
				# expressions spelled out for recognitionof the terms
				if units == 4:
					# pIC50 so fudge out to ln ic50
					le = 8.314 * 298.15 * ic50 * ic50factor/(mw*4184)
					lle = ic50 - logP
				else:
#must correct logic so that cmpds with blank or negative values #are handled properly
					if ic50 <= 0:
						continue
					else:
						le = -8.314 * 298.15 * math.log(ic50*ic50factor)/(mw*4184)
						lle = -1 * math.log10(ic50*ic50factor) - logP
			lecolumn.setDouble(r, le)
			llecolumn.setDouble(r, lle)
				
		if addplot.isSelected():
			leid = vtable.getColumnId(lecolumn)
			mwid = vtable.getColumnId(mwcolumn)
		
			vws.addChart(0, mwid, leid, -1)
			
		vtable.fireTableStructureChanged();
		