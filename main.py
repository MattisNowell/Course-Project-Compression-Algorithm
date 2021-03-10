
def readCharInFile(file, position:int) -> chr:
    character = file.read(position)
    return character

def getFileCharNumber(file) -> int :
    content = file.read()
    number = len(content)
    del content 
    return number

"""
def countCharsInLines(path:str) -> dict :
    macroTable = []
    with open(path) as file:
        line = file.readline()
        while line :
            charTable = {}
            for char in line:
                if char in charTable :
                    charTable[char] = charTable[char]+1
                else :
                    charTable[char] = 1
            macroTable.append(charTable)
            line = file.readline()
    return macroTable
"""


if __name__ == "__main__" :
    macroTable = []
    with open("einstein.en.txt") as file:
        line = file.readline()
        while line :
            charTable = {}
            for char in line:
                if char in charTable :
                    charTable[char] = charTable[char]+1
                else :
                    charTable[char] = 1
            macroTable.append(charTable)
            line = file.readline()