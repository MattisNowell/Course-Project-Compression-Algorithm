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

    macro_table: list = []

    line = file.readline()
    while line:
        # Here is a loop that counts the characters in a line and stores the data in a dictionary with the key being
        # the character and the value being the number of apparition in the line (the data is unordered):
        char_table: dict = {}
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
    total_char_number: int = get_file_char_number(opened_text_file)

    percentage_dict: dict = {}

    # Classic percentage calculation using the frequency of the concerned character and the total number of
    # characters in the text file:
    for CHAR in data:
        percentage_dict[CHAR] = (data[CHAR] / total_char_number) * 100

    return percentage_dict


def bit_to_byte(bit_string: str) -> list:
    """
    Converts a string type variable that contains a sequence of bits into a list type variable that contains the
    corresponding byte representation.
    """
    byte_table = []

    for chunk_position in range(0, len(bit_string) - 8, 8):
        chunk: str = ''

        for bit_position in range(8):
            chunk = chunk + bit_string[bit_position + chunk_position]

        bit_chunk_to_int = int(chunk, 2)
        byte_table.append(bit_chunk_to_int)

    return byte_table


def byte_to_bit(byte_array: bytes) -> str:
    """
    Converts a list type variable that contains a sequence of bytes into a string type variable that contains the
    corresponding bit representation.
    """
    bit_string: str = ''
    for byte in byte_array:
        byte_transformation = bin(byte)
        byte_transformation = byte_transformation[2:]
        bit_string = bit_string + byte_transformation
    return bit_string


if __name__ == "__main__":

    if sys.argv[1] == 'help':

        print("Command 'python3 main.py {action: 'compress'/'decompress'/'help'} {file path: not required if "
              "action=help}' ")

    elif sys.argv[1] == 'compress':

        path: str = sys.argv[2]

        file = open(path)
        total_char_number: int = get_file_char_number(file)

        print("Loading and processing file data...")
        macroTable = count_chars_in_lines(file)

        # Because the function 'countCharsInLines' returns a list of dictionaries, it is necessary
        # to merge all dictionaries into a single data structure.
        # This is easily done with the class Counter but requires multiple conversions as follows :
        macroCounter: Counter = Counter()
        for dictionary in macroTable:
            dictToCounter: Counter = Counter(dictionary)
            macroCounter = macroCounter + dictToCounter
        macroDictionary: dict = dict(macroCounter)

        # To facilitate the rest of the coding, operations will be made with the probabilities of
        # each character rather than their number of apparition. The corresponding data is fetched
        # using the 'calculatePercentage' function:
        print("Calculating data frequencies...")
        percentageDict: dict = calculate_percentage(file, macroDictionary)

        # The data requires to be sorted from less frequent to most frequent.
        # This is done with the function sorted but this returns a list of only chars sorted by their percentage
        # The date must then be transferred to a dictionary containing both the sorted char and their percentage
        print("Sorting frequency list...")
        sortedPercentageList = sorted(percentageDict, key=percentageDict.get)
        sortedPercentageDict = {}
        for char in sortedPercentageList:
            sortedPercentageDict[char] = percentageDict[char]

        # As the Node class constructor verifies the parameters of the created object to decide if it should treat it as
        # a base node corresponding to a specific character, or as a composed node built from two other nodes, it is
        # required to generate these base nodes before hand with each their needed data. The base nodes will be stored
        # in a list as follows:
        print("Creating and loading the Huffman Tree...")
        base_node_list: List[Node] = []
        for char in sortedPercentageDict:
            base_node_list.append(Node(character=char, probability=sortedPercentageDict.get(char)))

        # Once the base nodes are created, we can created the Huffman Tree based on them. This algorithm eventually
        # leads to a list containing a single node ("top_node") with a probability of 100% that points to all children
        # nodes. The Huffman Tree is created by first initializing a list of all nodes with the base nodes. The program
        # then picks the two first elements of the list and merges them into one node before deleting them of the list
        # The program then sorts the list to put the two least frequent nodes in 1st and 2nd place of the list, making
        # itself ready to repeat the process until one node is left in the list.
        node_list = base_node_list
        while len(node_list) != 1:
            node_list.append(Node(node_list[0], node_list[1]))
            node_list.pop(1)
            node_list.pop(0)
            node_list.sort(key=lambda x: x.probability)
        top_node = node_list[0]

        # The cursor in the file is set back to the beginning to read it and contain it into a string
        # A variable current_node is created to keep track of the program's actions in the Huffman Tree and is set
        # to the top_node since it is the main entrance to the rest of the Huffman Tree.
        file.seek(0, 0)
        text: str = file.read()
        current_node: Node = top_node

        # The following code's goal is to gather a specific character's binary representation created by the Huffman
        # Tree by going through it. Since the program will potentially deal with large files, methods to reduce the
        # time required to go through each character of the file and find its binary representation. To do so, we
        # create a dictionary (char_to_binary_dict) that will register every character's binary representation.
        # Thus the program only needs to go through the Huffman Tree once per character.
        # Once a character's binary representation is fetched, it is added to the global file's bit representation
        # (binary_file_representation) as follows:
        print("Encoding the data...")
        char_to_binary_dict: dict = {}
        binary_file_representation: str = ''
        for CHAR in text:
            if CHAR in char_to_binary_dict:
                binary_file_representation = binary_file_representation + char_to_binary_dict[CHAR]
            else:
                # To retrieve the binary representation of a character, the program starts from the top node.
                # For each current node the program looks at each child node's char list and the current node is then
                # set to the child node that contains the searched character. The binary value of that specific
                # child node is then added to the char's global bit representation (binary_char_representation).
                # The global bit representation is then registered in a list to use later as discussed above.
                binary_char_representation: str = ''
                while len(current_node.chars) != 1:
                    if CHAR in current_node.first_child_node.chars:
                        current_node = current_node.first_child_node
                        binary_char_representation = binary_char_representation + str(current_node.binary_id)
                    else:
                        current_node = current_node.second_child_node
                        binary_char_representation = binary_char_representation + str(current_node.binary_id)
                    binary_file_representation = binary_file_representation + binary_char_representation
                    char_to_binary_dict[CHAR] = binary_char_representation
            current_node = top_node

        # Once the bit representation of the entire file is retrieved, it is necessary to convert it into a byte
        # file to be written in a new file. Bits are converted to bytes by group of 8 bits. Therefore, we
        # make sure that the file's bit representation can be exactly divided in to group of 8 bits. If not, we
        # add 0 until the rule si followed. The file then goes through the function bit_to_byte() that retrieves
        # these 8 bit groups and converts them into decimal values to then store them in a list usable by the
        # python bytearray() function that converts decimal values to a series of bytes (byte_series).
        print("Writing the data to a new file...")
        if len(binary_file_representation) % 8 != 0:
            binary_file_representation = binary_file_representation + '0' * (len(binary_file_representation) % 8)
            byte_series = bytearray(bit_to_byte(binary_file_representation))
        else:
            byte_series = bytearray(bit_to_byte(binary_file_representation))

        # A file containing the byte result of the first file and its Huffman Tree is then created.
        with open("test_compressed.txt", 'w+b') as bin_file:
            bin_file.seek(0, 0)
            bin_file.truncate(0)
            bin_file.write(byte_series)

        print("Done !")

    elif sys.argv[1] == 'decompress':

        # Yet to be included.

        print("Under development...")
