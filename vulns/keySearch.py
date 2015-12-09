# Function - KeySearch:
# **Parameters : inputString- a line of code or a string 
# **Output : False if key does not look like a private key of anykind
#	     Returns Array[True, Keytype]- keytype will be null if cant specifiy 
import re
DEBUG = False 
TESTDB = False

def keySearch ( inputString ):
	if ressemblesKey(inputString):
		keyType = keyTypeDetection(inputString)
		return [True, keyType];			

	return [False, None];

def keyTypeDetection(inputString):
	return None;

def ressemblesKey(inputString):
	extract = inQuotes(inputString) 
	extract = str(extract)
	if extract != False:
		if lengthNotAppropriate(extract):
			return False;
		if containsSpaces(extract):
			return False;


		unique_letters   = uniqueLetterCount(extract)
		symbols		     = symbolCount(extract)
		numbers			 = numberCount(extract)
		unique_upperCase = uniqueUpperCaseCount(extract)
		unique_lowerCase = uniqueLowerCaseCount(extract)


		## Filter out typical file names and websites
		if "/" in extract: #website detection
			if DEBUG:
				print "Detected web url..."
			return False

		if "\\" in extract: #website detection
			if DEBUG:
				print "Detected seperator"
			return False
	
		if doSymbolsRepeat(extract): 
			if DEBUG:
				print "Detected repeating symbols"
			return False

		extension = checkIfFilename(extract)
		if extension:
			if DEBUG:
				print "Detected filename..." 
			return False

		
		if checkConsecutiveASCII(extract):
			if DEBUG:
				print "Detected consecutive letters... not random key"
			return False

		if checkIncrementingASCII(extract):
			if DEBUG:
				print "Detected consecutive letters... not random key"
			return False
		
		## THE REGEX ring
		#Searches for Format word_numbers
		if re.findall(r'[\w]*_[\d]*', extract):
			if DEBUG:
				print ""
			return 

		#Searches for Format numbers_word
		if re.findall(r'[\d]*_[\w]*', extract):
			if DEBUG:
				print ""
			return False


		if doesEntryExist(inputString):
			if DEBUG:
				print "entry already exists"
			return False







		#we know that this must at least be a password of some type
		if numbers == len(extract): 
			if DEBUG:
				print "All numbers detected... Most likely password or key"
			return True;
		
		if unique_upperCase == unique_letters and numbers > 2: 
			if DEBUG:
				print "All upper case letters and numbers detected... Most likely a key"
			return True;
	
		if (unique_letters > 6 and symbols > 0 and unique_upperCase > 0  and unique_lowerCase > 0 and numbers > 2):
			if DEBUG:
				print "Detected: Symbols, numbers, random upper case and lower case chars...Most likely a key or token"
			return True;
		
		if (symbols>0 and unique_letters > 6 and unique_upperCase == 0 and unique_lowerCase > 0 and numbers > 2):
			if DEBUG:
				print "Detected: Symbols, numbers, and random lower case chars... Most likely a key"
			return True;
		
		if (unique_letters > 6 and unique_upperCase == 0 and unique_lowerCase > 0 and numbers > 2):
			if DEBUG:
				print "Detected: numbers, and random lower case chars... Most likely a key"
			return True;
	return False;	


def inQuotes(inputString):
	result = re.findall(r'"([^"]*)"', inputString)
	if result:
		if DEBUG:
			print "Extracted string = " + result[0] + " from " + inputString
		return result[0];
	if DEBUG:
		print "Was unable to extract potential string from - "+ str(inputString) 
	return False;

def containsSpaces (inputString):
	if ' ' in inputString:
		if DEBUG:
			print "\tContains spaces."
		return True;
	if DEBUG:
		print "\tDoes not contain spaces."
	return False;


def lengthIsLessThan14(inputString):
	if len(inputString) < 14:
		if DEBUG:
			print "\tLength is < 14"
		return True;
	if DEBUG:
		print "\tLength is > 14"

def lengthNotAppropriate(inputString):
	if len(inputString) < 13 or len(inputString) > 60:
		if DEBUG:
			print "\tLength does not fit specifications of  13 < len > 60"
		return True;
	if DEBUG:
		print "\tLength is ok"
	return False

def numberCount(inputString):
	digit = 0
	for i in inputString:
   		if i.isdigit():
			digit += 1
	if DEBUG:
		print "\tnumberCount of " + inputString + " = " + str(digit)
	return digit;

def symbolCount(inputString):
	symbolCount = 0
	for i in inputString:
		if i.isalnum() == False:
			symbolCount += 1
	if DEBUG:
		print "\tsymbolCount = " + str(symbolCount)
	return symbolCount;

def uniqueLetterCount(inputString):
	arr = []
        for i in inputString:
		if i.isalpha() and not i in arr:
			arr.append(i)
	if DEBUG:
		print "\tuniqueLetterCount = " + str(len(arr))
	return len(arr);

def uniqueLowerCaseCount(inputString):
	arr = []
	for i in inputString:
		if i.isalpha() and not i in arr and i.islower():
			arr.append(i)
	if DEBUG:
		print "\tuniqueLowerCaseCount of = " + str(len(arr))
	return len(arr);

def uniqueUpperCaseCount(inputString):
	arr = []
	for i in inputString:
		if i.isalpha() and not i in arr and i.isupper():
			arr.append(i)
	if DEBUG:
		print "\tuniqueUpperCaseCount of = " + str(len(arr))
	return len(arr)

def checkIfFilename(extract):
	count = extract.count('.')
	if count > 1: 
		return True
	elif count == 1:
		loc = extract.index('.')
		if DEBUG:
			print "length: "+ str(len(extract))
			print "location:"+ str(loc)
			print extract
			print "length of extension = "+str((len(extract) - loc))
			print "extension =" + str((len(extract) - loc) < 8)
		if (len(extract) - loc) < 6:
			return True

	return False

def checkIncrementingASCII(inputString):

	#if "abc" in inputString.lower() or "123" in inputString:
	for x in xrange(len(inputString)):
		try:
			if (ord(inputString[x])+1) == ord(inputString[x+1]):
				if (ord(inputString[x+1])+1) == ord(inputString[x+2]):
					if DEBUG:
						print "Found Foward incrementing ASCII"
					return True
		except:
			pass
		try: 
			if (ord(inputString[x])+1) == ord(inputString[x+1]):
				if (ord(inputString[x+1])-1) == ord(inputString[x+2]):		
					if DEBUG:
						print "Found Backwards incrementing ASCII"
					return True
		except:
			pass
	return False


def checkConsecutiveASCII(inputString):

	#if "abc" in inputString.lower() or "123" in inputString:
	for x in xrange(len(inputString)):
		try:
			if (ord(inputString[x])) == ord(inputString[x+1]):
				if (ord(inputString[x+1])) == ord(inputString[x+2]):
					if DEBUG:
						print "Found Foward consecutive ASCII"
					return True
		except:
			pass
		
	return False

def doSymbolsRepeat(inputString):
	arr = []
	for i in inputString:
		if (i.isalnum() == False) and not i in arr:
			arr.append(i)
		elif i in arr:
			return True
	return False

def doesEntryExist(inputString):
	import sqlite3
	# If you are using a test db change the mother variable uptop
	if TESTDB:
		conn = sqlite3.connect('test2.db')
	else:
		conn = sqlite3.connect('../apekit.db')
	c = conn.cursor()
	#print inputString
	for row in c.execute("SELECT source_code FROM appvulnerability WHERE vulnerability_id=10 AND source_code like \'%"+inputString+"%\'"):
		return True
	return False