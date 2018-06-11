from Classifier import TTOSOM
from Utils import read_topology
from Utils import read_data_set
from Utils import retrieve_classes_as_map


topology = read_topology("./topology.tree")
data_set = read_data_set("https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv")

classes = ["virginica","setosa","versicolor"]
classes_as_map = retrieve_classes_as_map(classes)


classifier = TTOSOM(topology,data_set,12,0.9,0,0,5000,classes_as_map)
classifier.build_classifier()
