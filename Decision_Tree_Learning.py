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


def test_accuracy(rules, examples):
    if len(examples) == 0:
        return 0
    num_success = 0
    for example in examples:
        output = predict(rules, example)
        if output and output.get_post_condition() == example.get_classification():
            num_success = num_success + 1
    accuracy = (num_success / len(examples)) * 100
    return accuracy


def predict(rules, example):
    values = example.get_values().items()
    for rule in rules:
        if rule.get_preconditions().items() <= values:
            return rule
    return None


def test_rule_accuracy(rule, examples):
    if len(examples) == 0:
        return 0
    num_success = 0
    num_covers = 0
    for example in examples:
        output = rule_predict(rule, example)
        if output:
            num_covers = num_covers + 1
            if output.get_post_condition() == example.get_classification():
                num_success = num_success + 1
    if num_covers == 0:
        return 0
    accuracy = (num_success / num_covers) * 100
    return accuracy


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


def rule_predict(rule, example):
    values = example.get_values().items()
    if rule.get_preconditions().items() <= values:
        return rule
    return None


def order_set_of_rules(rules, examples):
    d = dict()
    for rule in rules:
        d[rule] = test_rule_accuracy(rule, examples)
    d = dict(sorted(d.items(), key=lambda item: item[1]))

    l = [k for k in d]
    l.reverse()

    return l


def rule_pruning(rules, examples):
    for rule in list(rules):
        while True:
            # print('regola ' + str(rule.get_preconditions()) + ', ' + rule.get_post_condition())
            original_accuracy = test_rule_accuracy(rule, examples)
            accuracy_gain = 0
            best_precondition_to_prune = None
            preconditions = list(rule.get_preconditions().items())
            for attribute_name, value in preconditions:
                rule.remove_precondition(attribute_name)
                pruned_accuracy = test_rule_accuracy(rule, examples)
                rule.add_precondition(attribute_name, value)
                # print(str(original_accuracy), str(pruned_accuracy) + " per precondition " + attribute_name, value)
                if accuracy_gain < pruned_accuracy - original_accuracy:
                    best_precondition_to_prune = attribute_name
                    accuracy_gain = pruned_accuracy - original_accuracy
            if best_precondition_to_prune is not None:
                rule.remove_precondition(best_precondition_to_prune)
                if not rule.get_preconditions():
                    rules.remove(rule)
            else:
                break
    #rules = remove_duplicates(rules)
    rules = order_set_of_rules(rules, examples)
    return rules


def remove_duplicates(rules):
    return list(dict.fromkeys(rules))

# def shuffle_set_of_rules(rules):
#     random.shuffle(rules)
