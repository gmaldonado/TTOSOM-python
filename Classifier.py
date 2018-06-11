from Neuron import Neuron
import random
from math import sqrt
import sys
from random import randint

#TODO check everything related to seed
class TTOSOM:

    def __init__(self, topology, training_set, initial_radius, initial_learning_rate,final_radius, final_learning_rate, iterations, classes_as_map):
        self.root = None
        self.training_set = training_set
        self.topology = topology
        self.initial_radius = initial_radius
        self.initial_learning_rate = initial_learning_rate
        self.final_radius = final_radius
        self.final_learning_rate = final_learning_rate
        self.iterations = iterations
        self.map = {}
        self.neurons_list = []
        self.classes_as_map = classes_as_map

    def build_classifier(self):
        self.__describe_topology()
        self.__cluster()
        self.__compute_labels()

    def __compute_labels(self):
        labeled_data = []
        for i in range(len(self.training_set)):
            aux = self.training_set[i]
            if not (aux[-1] == "?"):
                labeled_data.append(aux)
        #TODO this should be only for generating cluster vector REFACTOR
        cluster_vector = self.__generate_cluster_vector(labeled_data)
        self.__assign_class_to_neurons(self.root, labeled_data,cluster_vector)

    def __assign_class_to_neurons(self, node, data, cluster_vector):
        num_attributes = len(data[0]) - 1

        if node is not None:
            classes = [0]*len(data)
            for i in range(len(cluster_vector)):
                if cluster_vector[i] == node.id:
                    class_index = self.classes_as_map[data[i][num_attributes]]
                    classes[class_index] += 1

            counter = 0
            for clazz in classes:
                counter += clazz

            if counter != 0:
                max_value = -sys.maxsize - 1
                popular_class_index = -1
                for i in range(len(classes)):
                    if classes[i] > max_value:
                        max_value = classes[i]
                        popular_class_index = i
                node.weight[num_attributes] = popular_class_index
            else:
                node.weight[num_attributes] = randint(0, len(self.classes_as_map)-1)

            for child in node.children:
                self.__assign_class_to_neurons(child, data, cluster_vector)

    def classify_instance(self, instance):
        class_index = len(instance) - 1
        bmu = self.__find_bmu(instance,self.root)
        return bmu.weight[class_index]

    def __generate_cluster_vector(self, labeled_data):
        cluster_vector = [0] * len(self.training_set)
        for i in range(len(self.training_set)):
            cluster_vector[i] = self.__cluster_instance(labeled_data[i])
        return cluster_vector

    def __cluster_instance(self, instance):
        bmu = self.__find_bmu(instance, self.root)
        return bmu.id

    def __describe_topology(self):
        self.root = Neuron(None, self.topology, self.training_set)
        self.__tree_to_array(self.root)
        self.__pre_compute_neighbors()

    #TODO This should be done when creating tree instead of parsing a tree o a list REFACTOR
    def __tree_to_array(self,node):
        if node is not None:
            self.neurons_list.append(node)
            for child in node.children:
                self.__tree_to_array(child)

    def __pre_compute_neighbors(self):
        for neuron in self.neurons_list:
            radius = 0
            radius_to_neurons = {}
            #TODO revisit this do-while approach
            condition = True
            while(condition):
                bubble_of_activity = []
                bubble_of_activity.append(neuron)
                self.__calculate_neighborhood(bubble_of_activity,neuron,radius,None)
                #check this line
                radius_to_neurons[radius] = bubble_of_activity
                radius += 1
                condition=len(bubble_of_activity)<len(self.neurons_list)
            self.map[neuron.id] = radius_to_neurons

    def __calculate_neighborhood(self,bubble_of_activity,current,radius,origin):
        if radius <= 0:
            return
        else:
            for child in current.children:
                bubble_of_activity.append(child)
                self.__calculate_neighborhood(bubble_of_activity,child,radius-1,current)
            parent = current.parent
            #check this, to see if is the same as java
            if parent is not None and parent is not origin:
                bubble_of_activity.append(parent)
                self.__calculate_neighborhood(bubble_of_activity,parent,radius-1,current)
        return

    def __cluster(self):
        current_radius = self.initial_radius
        current_learning_rate = self.initial_learning_rate

        for i in range(self.iterations):
            current_instance = random.choice(self.training_set)
            self.__train(current_instance,self.root,round(current_radius),current_learning_rate)
            current_radius = self.__calculate_value(current_radius, self.initial_radius, self.final_radius)
            current_learning_rate = self.__calculate_value(current_learning_rate, self.initial_learning_rate,
                                                           self.final_learning_rate)

    def __train(self, input_sample, root, radius, learning_rate):
        bmu = self.__find_bmu(input_sample,root)
        bubble_of_activity = self.__get_precomputed_bubble(radius,bmu)

        for neuron in bubble_of_activity:
            self.__update_rule(neuron.weight,learning_rate,input_sample)

    def __get_precomputed_bubble(self,radius,bmu):
        selected_bmu = self.map[bmu.id]

        if (radius+1) > len(selected_bmu):
            bubble_of_activity = selected_bmu[len(selected_bmu)-1]
        else:
            bubble_of_activity = selected_bmu[round(radius)]
        return bubble_of_activity

    def __calculate_value(self, current_value, initial_value, final_value):
        delta = (initial_value - final_value) / self.iterations
        current_value -= delta
        return current_value

    @staticmethod
    def __update_rule(weight, learning_rate, instance_to_train):
        for i in range(len(weight) - 1):
            value = weight[i] + learning_rate * (instance_to_train[i] - weight[i])
            weight[i] = value

    def __find_bmu(self,input_sample,best_so_far):
        distance_result = self.__calculate_euclidean_distance(input_sample,best_so_far.weight)
        for neuron in self.neurons_list:
            current_distance = self.__calculate_euclidean_distance(input_sample,neuron.weight)
            if current_distance < distance_result:
                best_so_far = neuron
                distance_result = current_distance
        return best_so_far

    @staticmethod
    def __calculate_euclidean_distance(x, y):
        result = 0.0
        for i in range(len(x)-1):
            result += (x[i]-y[i])**2

        return sqrt(result)

