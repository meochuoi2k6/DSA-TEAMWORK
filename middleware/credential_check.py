


def checkName (name : str) ->bool:
    valid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    if not name or len(name) < 3 or len(name) > 20:
        return False
    for char in name:
        if char not in valid_characters:
            return False
    return True
def checkPhoneNumber(phone : str) ->bool:
    if not phone or len(phone) != 10 or phone.startwith(0) or not phone.isdigit():
        return False
    return True
def checkEmail(email : str) ->bool:
    valid_domains = {
        "gmail.com",
        "yahoo.com",
        "outlook.com",
        "hotmail.com"
    }
    valid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
    if not email:
        return False
    #Prefix check
    counting = 0
    postfix = ""
    for char in email:
        if char == "@":
            postfix = email[email.index(char)+1:]
            break
        if char in valid_characters:
            counting += 1
        if counting > 20:
            return False
    if counting < 3:
        return False
    #Domain check
    if postfix not in valid_domains:
        return False
    return True
