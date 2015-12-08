
# function to check for comments in code

def commentchecker(string):
    
    substring1 = " //"
    substring2 = "/*"
    substring3 = "/"
    
    flag01 = False
    flag02 = False
    
    if substring1 in string:
        flag01 = True
        #print("you have a comment")
    elif substring2 in string:
        flag01 = True
        #print("you have a multiline comment")
    elif string.startswith(substring3):
        flag01 = True

        
    return flag01