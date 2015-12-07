# Function - KeySearch:
# **Parameters : inputString- a line of code or a string 
# **Output : False if key does not look like a private key of anykind
#	     Returns Array[True, Keytype]- keytype will be null if cant specifiy 
def keySearch ( inputString ):
	if ressemblesKey(inputString):
		keyType = keyTypeDetection(inputString)
		return [True, Keytype];			

	return False;

def keyTypeDetection(inputString):
	return "null";

def ressemblesKey(inputString):
	extract = inQuotes(inputString) 
	if extract != False:
                 if lengthIsLessThan14(extract):
                         return False;
                 if containsSpaces(extract):
                         return False;
	unique_letters   = uniqueLetterCount(extract)
	symbolCount      = symbolCount(extract)
	numberCount		 = numberCount(extract)
	unique_upperCase = uniqueUpperCaseCount(extract)
	unique_lowerCase = uniqueLowerCaseCount(extract)
	if unique_letters > 5 or numberCount == len(extract) or unique_upperCase == len(extract) or (unique_letters > 2 and symbolCount > 0 and unique_upperCase > 0 and unique_lowercase):
		return True;

	return False;


def inQuotes(inputString):
	import re
	result = re.findall(r'"([^"]*)"', inputString)
	if result != "":
		return result;
	result = re.findall(r"'(.*?)'", inputString)
	if result != "":
                return result;
	return False;

def containsSpaces (inputString):
	if ' ' in inputString:
		return True;
	return False;


def lengthIsLessThan14(inputString):
	if len(inputString) < 14:
		return True;
	return False

def numberCount(inputString):
	digit = 0
	for i in inputString:
   		if i.isnumeric():
			digit += 1
	return digit;

def symbolCount(inputString):
	symbolCount = 0
	for i in inputString:
		if i.isalnum() == False:
			symbolCount += 1
	return symbolCount;

def uniqueLetterCount(inputString):
	arr = []
        for i in inputString:
		if i.isalpha() and not i in arr:
			arr.append(i)
	return len(arr);

def uniqueLowerCaseCount(inputString):
	arr = []
	for i in inputString:
		if i.isalpha() and not i in arr and i.islower():
			arr.append(i)
	return len(arr);

def uniqueUpperCaseCount(inputString):
	arr = []
	for i in inputString:
		if i.isalpha() and not i in arr and i.isupper():
			arr.append(i)
	return len(arr);
