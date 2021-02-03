from Tree import Tree
import pandas as pd
from sklearn.model_selection import train_test_split
from Attribute import Attribute
from Classification import Classification
import math


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
    classification = list()
    for example in examples:
        classification.append(example.get_classification())
    t = Tree()
    a = Attribute(max(classification, key=classification.count))
    t.set_root(a)
    return t


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


def import_data():
    balance_data = pd.read_csv(
        'Data/nursery.data',
        sep=',', header=None)

    return balance_data


def split_dataset(balance_data):
    # Separating the target variable
    X = balance_data.values[:, 0:8].tolist()
    Y = balance_data.values[:, 8].tolist()

    # Splitting the dataset into train and test
    X_train, X_test_and_validation, y_train, y_test_and_validation = train_test_split(
        X, Y, test_size=0.4)

    X_validation, X_test, y_validation, y_test = train_test_split(
        X_test_and_validation, y_test_and_validation, test_size=0.5)

    return X, Y, X_train, X_validation, X_test, y_train, y_validation, y_test


# def test_rule_quality(rule, examples):
#     if len(examples) == 0:
#         return 0
#     num_success = 0
#     for example in examples:
#         output = rule_predict(rule, example)
#         if output:
#             if output.get_post_condition() == example.get_classification():
#                 num_success = num_success + 1
#     accuracy = (num_success / len(examples)) * 100
#     return accuracy

# def shuffle_set_of_rules(rules):
#     random.shuffle(rules)
