from Classifier import TTOSOM
from Utils import read_topology
from Utils import read_data_set


topology = read_topology("./topology.tree")
data_set = read_data_set("https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv")

classifier = TTOSOM(topology,data_set)
classifier.build_classifier()
