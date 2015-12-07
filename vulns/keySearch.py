# Function - KeySearch:
# **Parameters : inputString- a line of code or a string 
# **Output : False if key does not look like a private key of anykind
#	     Returns Array[True, Keytype]- keytype will be null if cant specifiy 
DEBUG = False

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
		if lengthIsLessThan14(extract):
			return False;
		if containsSpaces(extract):
			return False;


		unique_letters   = uniqueLetterCount(extract)
		symbols		     = symbolCount(extract)
		numbers			 = numberCount(extract)
		unique_upperCase = uniqueUpperCaseCount(extract)
		unique_lowerCase = uniqueLowerCaseCount(extract)

		if unique_letters > 5 or numbers == len(extract) or unique_upperCase == len(extract) or (unique_letters > 2 and symbols > 0 and unique_upperCase > 0 and unique_lowerCase):
			return True;
	return False;


def inQuotes(inputString):
	import re
	result = re.findall(r'"([^"]*)"', inputString)
	if result != "":
		if DEBUG:
			print "Extracted string = " + str(result)
		return result;
	result = re.findall(r"'(.*?)'", inputString)
	if result != "":
		if DEBUG:
			print "Extracted string = " + str(result)
		return result;
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
	return len(arr);
