class Neuron:

    def __init__(self, parent, topology, data_set):
        number_of_children = topology[0]["number_of_children"]
        #review stuff related to random, such as the seed
        self.weight = data_set.sample(1)
        self.children = []
        self.parent = parent
        self.id = topology[0]["id"]

        del topology[0]
        for i in range(number_of_children):
            self.children.append(Neuron(self,topology,data_set))

