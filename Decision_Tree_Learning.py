from Tree import Tree
import pandas as pd
from sklearn.model_selection import train_test_split
from Attribute import Attribute
from Classification import Classification
import math


# algoritmo descritto in R&N 2009 §18.3
def decision_tree_learning(examples, attributes, parent_examples):
    if not examples:
        return plurality_value(parent_examples)
    elif have_same_classification(examples) is True:
        t = Tree()
        a = Attribute(examples[0].get_classification())
        t.set_root(a)
        return t
    elif not attributes:
        return plurality_value(examples)
    else:
        A = importance(attributes, examples)
        tree = Tree()
        tree.set_root(A)
        attributes.remove(A)
        for value in A.get_set_of_values():
            subset_of_examples = []
            for example in examples:
                if example.get_value(A.get_name()) == value:
                    subset_of_examples.append(example)
            subtree = decision_tree_learning(subset_of_examples, attributes, examples)
            tree.insert(value, subtree.get_root())
        return tree


def plurality_value(examples):
    classification = get_max_classification_occurrences(examples)
    t = Tree()
    a = Attribute(classification)
    t.set_root(a)
    return t


def get_max_classification_occurrences(examples):
    classification = Classification()
    classifications = dict()

    for c in classification.get_values():
        classifications[c] = 0

    for example in examples:
        classifications[example.get_classification()] += 1

    v = list(classifications.values())

    k = list(classifications.keys())
    return k[v.index(max(v))]


def have_same_classification(examples):
    classification = list()
    for example in examples:
        classification.append(example.get_classification())
    if classification.count(classification[0]) == len(classification):
        return True
    else:
        return False


def importance(attributes, examples):
    most_important_attribute = attributes[0]
    min = None
    for attribute in attributes:
        rem = remainder(attribute, examples)
        if min is None:
            min = rem
        if min > rem:
            min = rem
            most_important_attribute = attribute

        # print(rem, attribute.get_name())
    return most_important_attribute


def remainder(attribute, examples):
    sub_examples = list()
    rem = 0
    for value in attribute.get_set_of_values():
        for example in examples:
            if example.get_value(attribute.get_name()) == value:
                sub_examples.append(example)
        rem = rem + (len(sub_examples) / len(examples)) * get_entropy(sub_examples)
        sub_examples.clear()
    return rem


def get_entropy(examples):
    classifications = list()
    classification_occurrences = list()
    classif = Classification()
    entropy = 0
    if len(examples) != 0:
        for example in examples:
            classifications.append(example.get_classification())
        for classification in classif.get_values():
            classification_occurrences.append(classifications.count(classification))
        # print(str(classification_occurrences))
        for class_occur in classification_occurrences:
            probability = class_occur / len(examples)
            if probability != 0:
                entropy = entropy + (probability * math.log2(probability))
    return -entropy
