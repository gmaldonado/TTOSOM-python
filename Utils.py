import requests
import io
import pandas as pd
import sys


# Currently this is reading from an URL, it might be changed in the future
def read_data_set(path):
    url_content = requests.get(path).content
    data_set = pd.read_csv(io.StringIO(url_content.decode('utf-8')))
    return data_set.values


# This method is only created if you want to check the structure of the tree
def print_tree(neuron, indent):
    if neuron is not None:
        if indent > 0:
            for k in range(indent):
                sys.stdout.write(' ')
        print(neuron.node_id)
        for child in neuron.children:
            print_tree(child, indent + 2)

#@staticmethod
def retrieve_classes_as_map(classes):
    classes_as_map = {}
    for i in range(len(classes)):
        classes_as_map[classes[i]] = i
    return classes_as_map
