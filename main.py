
def readCharInFile(path:str, position:int) -> chr:
    file = open(path)
    character = file.read(position)
    return character

def getFileCharNumber(path:str) -> int :
    file = open(path)
    content = file.read()
    number = len(content)
    del content 
    return number
    
if __name__ == "__main__" :
    charTable = []
    for i in range(getFileCharNumber("einstein.en.txt")) :
        charTable.append(readCharInFile("einstein.en.txt", i))