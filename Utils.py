import requests
import io
import pandas as pd
import sys


def read_topology(topology_file_path):
    with open(topology_file_path) as topology_file:
        topology_description = topology_file.readline().split(" ")

    topology = []
    for i in range(len(topology_description)):
        current_element = {"id": i, "number_of_children": int(topology_description[i])}
        topology.append(current_element)
    return topology

# Currently this is reading from an URL, it might be changed in the future
def read_data_set(path):
    url_content = requests.get(path).content
    data_set = pd.read_csv(io.StringIO(url_content.decode('utf-8')))
    return data_set


# This method is only created if you want to check the structure of the tree
def print_tree(neuron, indent):
    if neuron is not None:
        if indent > 0:
            for k in range(indent):
                sys.stdout.write(' ')
        print(neuron.id)
        for child in neuron.children:
            print_tree(child, indent + 2)
