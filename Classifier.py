from Neuron import Neuron
from Utils import read_topology
from Utils import read_data_set


class TTOSOM:

    def __init__(self):
        self.root = None

    def describe_topology(self, topology_path, data_set_path):
        topology = read_topology(topology_path)
        data_set = read_data_set(data_set_path)
        self.root = Neuron(None, topology, data_set)
