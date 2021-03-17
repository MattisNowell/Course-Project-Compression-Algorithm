class Node:
    probability: float = 0.0

    first_child_node: "Node" = None

    second_child_node: "Node" = None

    binary_id: bool = 0

    def __init__(self, first_child_node: "Node" = None, second_child_node: "Node" = None, character: chr = None,
                 probability: float = 0.0):
        self.first_child_node = first_child_node
        self.second_child_node = second_child_node
        if character is not None and probability != 0.0:
            self.probability = probability
            self.chars: list = []
            self.chars.append(character)
        else:
            self.probability = first_child_node.get_probability() + second_child_node.get_probability()
            self.chars = first_child_node.chars + second_child_node.chars
            first_child_node.binary_id = 0
            second_child_node.binary_id = 1

    def get_first_node(self) -> "Node":
        return self.first_child_node

    def get_second_node(self) -> "Node":
        return self.second_child_node

    def get_binary_id(self) -> bool:
        return self.binary_id

    def get_probability(self) -> float:
        return self.probability

    def set_first_node(self, first_child_node: "Node") -> None:
        self.first_child_node = first_child_node

    def set_second_node(self, second_child_node: "Node") -> None:
        self.second_child_node = second_child_node
