import sqlite3
from keySearch import *



print "Beggining test on keySearch..."
conn = sqlite3.connect('test2.db')
c = conn.cursor()
for row in c.execute('SELECT source_code FROM appvulnerability WHERE vulnerability_id=10'):
	result = keySearch(row[0])
	if result[0]:
	        print "Passed Key test:\t" + inQuotes(row[0])
		#print "line of code:\t" + row[0]
print "End of test on keySearch..."


print ""
print ""
print ""

print doesEntryExist("DasdfadsfdEBUG") #should return false
print doesEntryExist("DEBUG") # Should return true
