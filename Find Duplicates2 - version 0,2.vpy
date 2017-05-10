#Version 0.1
#Goal of script is to find duplicate compounds by XPC number, then average
#columns as it makes sense

#import necessary libraries
import com.dotmatics.vortex.mol2img.Mol2Img
import sys
import com.dotmatics.vortex.util.Util as Util
import subprocess

#util path depending on OS
if Util.getPlatform() == Util.PlatformIsWindows:
  sys.path.append(vortex.getVortexFolder() + '\\modules\jythonconsole')
  sys.path.append(vortex.getVortexFolder() + '\\modules\jythonlib')
else:
  sys.path.append(vortex.getVortexFolder() + '/modules/jythonconsole')
  sys.path.append(vortex.getVortexFolder() + '/modules/jythonlib')

#if  nothing is open, die
dup_col = vtable.findColumnWithName("Duplicate", 0)

if dup_col is not None:
	vortex.alert('You already ran this script. Please delete the duplicate column and try again if you are sure!')
else:	
	#create dup column	
	dup_col = vtable.findColumnWithName("Duplicate", 1, vortex.STRING)
	
	#column for XPC numbers
	id_entered = vortex.input("Enter the name of the ID column, or leave blank to use 'ID'")
	if id_entered == "": id_entered = "ID"
	id_col = vtable.findColumnWithName(id_entered, 0)
	
	#find all columns
	column_count = vtable.getColumnCount()
	done_list = []		#this stores which row num has been checked, so that we dont do it again 
	
	for r in range(0, int(vtable.getRealRowCount())):
		#get current row's xpc num
		curr_xpc = id_col.getValueAsString(r)
		
		#if this cpd has been done already, then move on
		if r in done_list: continue
		
		#this becomes true if cpd has duplicates
		has_duplicates = False
		
		#og data keeps running total of values from each column
		data = ['x']*column_count
		#average count keeps a tally of how many compounds have data in each column
		average_count = ['x']*column_count
	
		#populate current data, start at 1 to avoid structuer, and end at -2 to avoid DUPLICATE column we just created
		for k in range (1, column_count - 1):
			curr_data = vtable.getColumn(k).getValueAsString(r)
			#some numbers are -infinity and i dont know how to check for that. num + 1 should be bigger than 1 (no negative numbers possble (TO--DO: RIGHT?!?!?!?!?)) if not, its
			#negative infinity so ignore it
			try:
				curr_data = float(curr_data)
				data[k]  = curr_data
				average_count[k] = 1
			except:
				continue
				#data_text[k] = curr_data		
		
		
		
		#loop through rest of table (start at curr row + 1)
		for t in range (r + 1, int(vtable.getRealRowCount())):
			#get XPC number 
			test_xpc = id_col.getValueAsString(t)
			
			#if the row's xpc matches current xpc, then
			if curr_xpc == test_xpc:
				#found dupe. write that current cpd is a dupe after this loop
				has_duplicates = True
	
				#loop through columns start at 1 and finish -2 to avoid STRUCTURE and DUPLICATE columns
				for j in range(1, column_count - 1):
					#curr data stores data in current column, 
					curr_data = vtable.getColumn(j).getValueAsString(t)
					#if it's numeric a
					try:
						curr_data = float(curr_data)
					except:
						continue
	
						#add to data list
					if data[j] == 'x':
						data[j] = float(curr_data)
						average_count[j] = 1
					else:
						data[j] = data[j] + float(curr_data)
						average_count[j] += 1
					#vortex.alert(data[j])
					#vortex.alert(average_count[j])
				#mark row duplicate
				dup_col.setValueFromString(t, str("DUPLICATE - DELETE"))
				#add this row to the list of cpds that are done, so we dont do it again
				done_list.append(t)
		
		#if duplicates found , then  make average and update
		if has_duplicates == True:
			dup_col.setValueFromString(r, "DUPLICATE - AVERAGED")
			
			for m in range(1, column_count - 1):
				#vortex.alert(data[m])
				#vortex.alert(average_count[m])
				if data[m] != 'x': #!= "":# and not(r in done_list):
					average = float(data[m]) / float(average_count[m])
					#vortex.alert(str(average))
					
					#attempt to write strin
					vtable.getColumn(m).setValueFromString(r, str(average))		#To--DO: THIS FAISL TO WRITE IF THE COLUMN IS NOT A DOUBLE (e.g INTEGER)
					
					#see if worked
					try:
						read = float(vtable.getColumn(m).getValueAsString(r))
					except:
						#couldnt write it!!!
						#rewrite as integer
						vtable.getColumn(m).setValueFromString(r, str(int(average)))				
		else:
			dup_col.setValueFromString(r, "NO DUPLICATES")
				
	vtable.fireTableDataChanged
	vtable.fireTableStructureChanged
	






