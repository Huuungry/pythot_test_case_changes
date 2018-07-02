
path_to_credls="C:\scripts\credls.txt"

def get_credentials(path=""):
    a,b="",""
    try:
        with open(path,"r") as file:
            a = file.readline()[:-1]
            b = file.readline()
    except Exception:
        print("File with credls was not found or has incorrect format")
    return a, b
LOGIN = get_credentials(path_to_credls)[0]
PASSWORD = get_credentials(path_to_credls)[1]

def get_login():
    return LOGIN
def get_password():
    return PASSWORD