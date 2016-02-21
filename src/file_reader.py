import re

def readFromFile (query):
    query = query+":\n"
    file_obj = open("config.txt", "r")
    eof = False
    while (not eof):
        line = file_obj.readline()
        if (line == "\n"):
            eof = True
        if (line == query):
            return re.sub("[\n]", "", file_obj.readline())
    return "Err"
