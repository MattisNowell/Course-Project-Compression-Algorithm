from collections import Counter
from node import Node
import sys
from typing import List


def get_file_char_number(opened_text_file) -> int:
    """
    Returns the number of characters contained in a given text file.
    """
    opened_text_file.seek(0, 0)

    text = opened_text_file.read()
    number = len(text)
    # The text is deleted as text files to be compressed are often quite voluminous.
    del text

    return number


def count_chars_in_lines(opened_text_file) -> list:
    """
    Returns a list containing dictionaries with the number of each character for each line. Each dictionary contains the
    data for a specific line.
    """
    opened_text_file.seek(0, 0)

    macro_table = []

    line = file.readline()
    while line:
        # Here is a loop that counts the characters in a line and stores the data in a dictionary with the key being
        # the character and the value being the number of apparition in the line (the data is unordered):
        char_table = {}
        for CHAR in line:
            if CHAR in char_table:
                char_table[CHAR] = char_table[CHAR] + 1
            else:
                char_table[CHAR] = 1
        # The dictionary containing the data of a line is stored in a list that will eventually contain dictionaries
        # for all lines in the file:
        macro_table.append(char_table)
        # The program passes on to the next line in file to repeat the process:
        line = file.readline()
    del line

    return macro_table


def calculate_percentage(opened_text_file, data: dict) -> dict:
    """
    Calculates the percentage of each character in a given text file. 
    Returns the data in a dictionary.
    """
    total_char_number = get_file_char_number(opened_text_file)

    percentage_dict = {}

    # Classic percentage calculation using the frequency of the concerned character and the total number of
    # characters in the text file:
    for CHAR in data:
        percentage_dict[CHAR] = (data[CHAR] / total_char_number) * 100

    return percentage_dict


if __name__ == "__main__":

    if sys.argv[1] == 'help':

        print("Command 'python3 main.py {action: 'compress'/'decompress'/'help'} {file path: not required if "
              "action=help}' ")

    elif sys.argv[1] == 'compress':

        file = open(sys.argv[2])

        print("Loading and processing file characters...")
        macroTable = count_chars_in_lines(file)

        # Because the function 'countCharsInLines' returns a list of dictionaries, it is necessary
        # to merge all dictionaries into a single data structure.
        # This is easily done with the class Counter but requires multiple conversions as follows :
        macroCounter = Counter()
        for dictionary in macroTable:
            dictToCounter = Counter(dictionary)
            macroCounter = macroCounter + dictToCounter
        macroDictionary = dict(macroCounter)

        # To facilitate the rest of the coding, operations will be made with the probabilities of
        # each character rather than their number of apparition. The corresponding data is fetched
        # using the 'calculatePercentage' function:
        percentageDict = calculate_percentage(file, macroDictionary)

        # The data requires to be sorted from less frequent to most frequent.
        # This is done with the function sorted but this returns a list of only chars sorted by their percentage
        # The date must then be transferred to a dictionary containing both the sorted char and their percentage
        sortedPercentageList = sorted(percentageDict, key=percentageDict.get)
        sortedPercentageDict = {}
        for char in sortedPercentageList:
            sortedPercentageDict[char] = percentageDict[char]
        print(sortedPercentageDict)

        # As the Node class constructor verifies the parameters of the created object to decide if it should treat it as
        # a base node corresponding to a specific character, or as a composed node built from two other nodes, it is
        # required to generate these base nodes before hand with each their needed data. The base nodes will be stored
        # in a list as follows:
        base_node_list: List[Node] = []
        for char in sortedPercentageDict:
            base_node_list.append(Node(character=char, probability=sortedPercentageDict.get(char)))

        # Once the base nodes are created, we can created the Huffman Tree based on them. This algorithm eventually
        # leads to a list containing a single Node with a probability of 100% that points to all children nodes.
        node_list = base_node_list
        while len(node_list) != 1:
            node_list.append(Node(node_list[0], node_list[1]))
            node_list.pop(1)
            node_list.pop(0)
            node_list.sort(key=lambda x: x.get_probability())
        top_node = node_list[0]

        current_node: Node = top_node
        binary_representation: str = ''
        for i in range(1):
            current_node = current_node.first_child_node
            binary_representation = binary_representation + str(current_node.binary_id)
        print(current_node.chars, current_node.probability)
        for i in range(5):
            current_node = current_node.second_child_node
            binary_representation = binary_representation + str(current_node.binary_id)
        print(current_node.chars, current_node.probability, binary_representation)

    elif sys.argv[1] == 'decompress':

        print("Under development...")
