import random

class Neuron:

    _global_identifier = 0

    def __init__(self, parent, number_of_children, height, data_set):
        Neuron._global_identifier += 1
        self.node_id = self._global_identifier
        self.children = []
        self.weight = random.choice(data_set)
        self.parent = parent
        self.number_of_children = number_of_children
        self.height = height

        if height <= 0:
            return None

        for i in range(number_of_children):
            self.children.append(Neuron(self, self.number_of_children, self.height-1,data_set))






