class Node:
    """
    Class node is the class that creates and manages the data relative to each element in the final
    data structure created by the Huffman Tree. A node object points to two other nodes that are its child nodes.
    Its parameters are its probability that is the sum of its children's own probability. It also has a binary id
    that is attributed depending to its sibling node (a node it does not point two but to which its parent node
    points to in a pair with the current node)
    """
    probability: float = 0.0

    first_child_node: "Node" = None

    second_child_node: "Node" = None

    binary_id: bool = 0

    # The constructor is built in a way that leaves the possibility to create a standard node (i.e. a node that is
    # the pairing of two children nodes) but also base nodes to which we can initialize the needed data such as
    # a base character and its corresponding frequency and that does not point to any child node.
    def __init__(self, first_child_node: "Node" = None, second_child_node: "Node" = None, character: chr = None,
                 probability: float = 0.0):
        if character is not None and probability != 0.0:
            self.first_child_node = None
            self.second_child_node = None
            self.probability = probability
            self.chars: list = []
            self.chars.append(character)
        else:
            self.first_child_node = first_child_node
            self.second_child_node = second_child_node
            self.probability = first_child_node.probability + second_child_node.probability
            self.chars = first_child_node.chars + second_child_node.chars
            first_child_node.binary_id = 0
            second_child_node.binary_id = 1