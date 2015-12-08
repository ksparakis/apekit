def httpschecker(string):

    substring1 = "http:"
    substring2 = "https:"

    #bool flag1 = false
    #bool flag2 = false

    flag1 = False
    flag2 = False

    result = False

    #string = ("http://www.supersecret.com")

    if (substring1 in string):
        flag1 = True
        #print("http is in here")
    if (substring2 in string):
        flag2 = True


    #print("Out of the loops!")

    if (flag1 == True and flag2 == True):
        #print("Yay you are safe")
        result = False
    elif (flag1 == True and flag2 == False):
        #print("Oh no, you are not safe!")
        result = True
    elif (flag1 == False and flag2 == False):
        #print("No URL's in this code, broseph!")
        result = False
    return result
