# Function - KeySearch:
# **Parameters : inputString- a line of code or a string 
# **Output : False if key does not look like a private key of anykind
#	     Returns Array[True, Keytype]- keytype will be null if cant specifiy 
def keySearch ( inputString ):
	if ressemblesKey(inputString):
		keyType = keyTypeDetection(inputString)
		return [True, Keytype];			

	return False;


def ressemblesKey(inputString):
	extract = inQuotes(inputString) 
	if extract != False:
                 if lengthIsLessThan14(extract):
                         return False;
                 if containsSpaces(extract):
                         return False;
	unique_letters   = uniqueLetterCount(extract)
	symbolCount      = symbolCount(extract)
	numberCount	 = numberCount(extract)
	unique_upperCase = uniqueUpperCaseCount(extract)
	unique_lowerCase = uniqueLowerCaseCount(extract)
	if unique_letters > 5 || numberCount = len(extract) || unique_upperCase = len(extract) || (unique_letters > 2 && symbolCount > 0 && unique_upperCase > 0 && unique_lowercase):
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
        	digit+=1
	return digit;

def symbolCount(inputString):
	symbolCount = 0
        for i in inputString:
                  if i.isalnum() == False:
                  symbolCount+=1
          return symbolCount;
	return 0;

def uniqueLetterCount(inputString):
	arr = []
        for i in inputString:
		if i.isalpha() && !i in arr:
			arr.append(i)
	return len(arr);

def uniqueLowerCaseCount(inputString):
	arr = []
	for i in inputString:
		if i.isalpha() && !i in arr && i.islower():
			arr.append(i)
	return len(arr);

def uniqueUpperCaseCount(inputString):
	arr = []
	for i in inputString:
		if i.isalpha() && !i in arr && i.isupper():
			arr.append(i)
	return len(arr);
