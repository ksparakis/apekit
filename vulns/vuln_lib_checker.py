class CVE:
	id = ""
	link = ""
	description = ""
	key_search = ""
	
	def __init__(self):
		self.key_search = list()
		
	def match(self,str):
#		In this function, you can pass a string and look for the key words that would be 
#		indicators of potential vulnerabilities.
#		It will take in a string and return true if it finds one or more of the search words
#		in it. 
		for i in range(0,len(self.key_search)):
			res = str.find(self.key_search[i])
			if res != -1:
				return True

		return False

class VulnLibChecker:
	l = list();
	
	def __init__(self):
		c = 0
		t = CVE();
		
		f = open('vulnerabilities.txt')
		for line in iter(f):
			if c == 0:
				t.id = line[:-1]
				c = 1
			elif c == 1:
				t.link = line[:-1]
				c = 2
			elif c == 2:
				t.description = line[:-1]
				c = 3
			elif c == 3:
				if(line[0] == "*"):
					c = 0
					self.l.append(t)
					t = CVE()
					continue
				else:
					t.key_search.append(line[:-1])		
				
		f.close()
				
		
	
	def add2list(self, obj):
#		You can use this call to add more vulnerabilitie to VulnLibChecker's list 
		self.l.append(obj);
		
	def s_keys(self):
#		This function will list all the possible vulnerabilities we want to look for
#		in our the APKs. They are separed by CVE number and the strings we look for 
#		to indicate a potential vulnerability.
		for ii in range(0,len(self.l)):
			print "Searching for "  + self.l[0].id + ":"
			
			for jj in range(0, len(self.l[ii].key_search)):
				print self.l[ii].key_search[jj]
				
			print "" 

	def vulnCheck(self, str):
#		This function will look through all the vulnerabilities in VulnLibChecker and 
#		see if the given string coulld represent any potential vulnerability. 
#		It returns a list of CVE numbers.
		report = []
		for ii in range(0,len(self.l)):
			bool = self.l[ii].match(str)
			if bool:
				report.append(int(self.l[ii].id))
		return report


if __name__ == "__main__":
	vln = VulnLibChecker()
	print vln.vulnCheck("com.android.mms.transaction.MESSAGE_SENT .processMessage")
	print vln.vulnCheck("")
