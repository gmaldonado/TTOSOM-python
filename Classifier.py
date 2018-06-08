from Neuron import Neuron
from Utils import read_topology
from Utils import read_data_set


class TTOSOM:

    def __init__(self, topology, training_set):
        self.root = None
        self.training_set = training_set
        self.topology = topology

    def build_classifier(self):
        self.__describe_topology()

    def __describe_topology(self):
        self.root = Neuron(None, self.topology, self.training_set)
        print(self.root)