from Classifier import TTOSOM
from Utils import read_data_set
from Utils import retrieve_classes_as_map


data_set = read_data_set("https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv")

classes = ["virginica","setosa","versicolor"]
classes_as_map = retrieve_classes_as_map(classes)

classifier = TTOSOM(data_set,12,0.9,0,0,100000,classes_as_map)
classifier.build_classifier()