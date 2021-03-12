from collections import Counter 

def getFileCharNumber(textFile) -> int :
    """
    Returns the number of characters contained in a given text file.
    """
    text = textFile.read()
    number = len(text)
    del text 
    
    return number

def countCharsInLines(path:str) -> list :
    """
    Returns a list containing dictionaries with the number of each character for each line.
    Each dictionary contains the data for a specific line.
    """
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

def calculatePercentage(textFile, data:dict) -> dict:
    """
    Calculates the percentage of each character in a given text file. 
    Returns the data in a dictionary.
    """
    totalCharNumber = getFileCharNumber(textFile)

    percentageDict = {}
    
    for char in data:
        percentageDict[char] = (data[char]/ totalCharNumber)*100
        
    return percentageDict



if __name__ == "__main__" :

    macroTable = countCharsInLines("einstein.en.txt")
    
    file = open("einstein.en.txt")
    
    #Because the function 'countCharsInLines' returns a list of dictionaries, it is necessary 
    #to merge all dictionaries into a single data structure.
    #This is easily done with the class Counter but requires multiplie conversions as follows : 
    macroCounter = Counter()
    for dictionary in macroTable :
        dictToCounter = Counter(dictionary)
        macroCounter = macroCounter + dictToCounter
    macroDictionary = dict(macroCounter)
    
    percentageDict = calculatePercentage(file, macroDictionary)
 
    
    for char.values() in macroDictionary:
        
    
    
    
            
            
            