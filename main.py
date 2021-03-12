from collections import Counter 
import sys

def getFileCharNumber(textFile) -> int :
    """
    Returns the number of characters contained in a given text file.
    """
    text = textFile.read()
    number = len(text)
	#The text is deleted as text files to be compressed are often quite voluminous. 
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
			#Here is a loop that counts the characters in a line and stores the data in a dictionary with the key being 
			#the character and the value being the number of apparition in the line (the data is unordered):
			charTable = {}
			for char in line:
				if char in charTable :
					charTable[char] = charTable[char]+1
				else :
					charTable[char] = 1
			#The dictionary containing the data of a line is stored in a list that will eventually contain dictionaries for all
			#lines in the file:
			macroTable.append(charTable)
			#The program passes on to the next line in file to repeat the process:
			line = file.readline()
		file.close()
		del line
	
	return macroTable

def calculatePercentage(textFile, data:dict) -> dict:
    """
    Calculates the percentage of each character in a given text file. 
    Returns the data in a dictionary.
    """
    totalCharNumber = getFileCharNumber(textFile)

    percentageDict = {}
    
	#Classic percentage calculation using the frequency of the concerned character and the total number of characters in the 
	#text file:
    for char in data:
        percentageDict[char] = (data[char]/ totalCharNumber)*100
        
    return percentageDict



if __name__ == "__main__":
	
	if sys.argv[1] == 'help':
	
		print("Command 'python3 main.py {action: 'compress'/'decompress'/'help'} {file path: not required if action=help}' ")
		
	elif sys.argv[1] == 'compress':
	
		macroTable = countCharsInLines(sys.argv[2])
    
		file = open(sys.argv[2])
		
		#Because the function 'countCharsInLines' returns a list of dictionaries, it is necessary 
		#to merge all dictionaries into a single data structure.
		#This is easily done with the class Counter but requires multiple conversions as follows : 
		macroCounter = Counter()
		for dictionary in macroTable :
			dictToCounter = Counter(dictionary)
			macroCounter = macroCounter + dictToCounter
		macroDictionary = dict(macroCounter)
		
		#To facilitate the rest of the coding, operations will be made with the probabilities of
		#each character rather than their number of apparition. The corresponding data is fetched 
		#using the 'calculatePercentage' function:
		percentageDict = calculatePercentage(file, macroDictionary)
		
		#The data requires to be sorted from less frequent to most frequent.
		#This is done with the function sorted but this returns a list of only chars sorted by their percentage
		#The date must then be retransfered to a dictionary containing both the sorted char and their percentage
		sortedPercentageList = sorted(percentageDict, key=percentageDict.get)
		sortedPercentageDict = {}
		for char in sortedPercentageList:
			sortedPercentageDict[char] = percentageDict[char]
		print(sortedPercentageDict)
		
	elif sys.argv[1] == 'decompress':
		
		print("Under development...")