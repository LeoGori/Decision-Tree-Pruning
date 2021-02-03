import latextable as latextable
from texttable import Texttable
from Decision_Tree_Learning import *
# import matplotlib.pyplot as plt
import csv
#import collections
#from datetime import datetime
#import random
from Example import Example
import copy
#import sklearn
from SetOfRules import *

def get_attributes():
    attributes = list()

    with open('Data/Attributes and values', 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            attr = Attribute(row[0])
            for value in row[1:]:
                attr.add_value(value)
            attributes.append(attr)
    return attributes


def get_examples_set(examples_attributes, examples_classifications, attributes):
    training_examples = list()
    for x, y in zip(examples_attributes, examples_classifications):
        example = Example()
        for attr, value in zip(attributes, x):
            example.add_value(attr.get_name(), value)
        example.set_classification(y)
        training_examples.append(example)

    return training_examples


def get_classification():
    my_file = open("Data/Classification", "r")
    content = my_file.read()
    content_list = content.split(", ")
    my_file.close()

    classification = Classification()

    for value in content_list:
        classification.set_value(value)

    return classification


def get_num_istances_per_classification(classification):
    classifications = dict()

    for c in classification.get_values():
        classifications[c] = 0

    print(classifications)

    for c in Y:
        classifications[c] += 1

    print(classifications)


class Test:

    def __init__(self):

        self._table = Texttable()
        self._table.set_cols_align(["c"] * 3)
        self._table.set_cols_dtype(['i', 'f', 'f'])
        self.accuracy_pre_pruning = []
        self.accuracy_post_pruning = []
        # self.plt = plt

    def process(self, index):
        print("test n." + str(index))
        data = import_data()

        X, Y, x_train, x_validation, x_test, y_train, y_validation, y_test = split_dataset(data)

        print(str(len(X)) + ', ' + str(len(x_train)) + ', ' + str(len(x_test)) + ', ' + str(len(x_validation)))

        # definisce un insieme di classificazioni prelevandole dal dataset
        classification = get_classification()

        # preleva gli attributi dal dataset
        attributes = get_attributes()
        clone_attributes = get_attributes()

        # definisce una lista di elementi di tipo Example costruiti sui valori del dataset
        training_examples = get_examples_set(x_train, y_train, attributes)

        validation_examples = get_examples_set(x_validation, y_validation, attributes)

        test_examples = get_examples_set(x_test, y_test, attributes)

        # esegue l'apprendimento dell'albero di decisione
        tree = decision_tree_learning(training_examples, clone_attributes, training_examples)
        print('la radice è ' + str(tree.get_root().get_attribute().get_name()))
        tree.x_order()

        # definisce il set di regole estratto dalla struttura dell'albero
        set_of_rules = tree.get_set_of_rules()

        #calcola l'accuratezza del set di regole sul training set
        accuracy = test_accuracy(set_of_rules.get_rules(), training_examples)
        print('accuracy on training set is: ' + str(accuracy) + ' %')

        # calcola l'accuratezza del set di regole sul test set prima di eseguire la strategia di pruning
        accuracy = test_accuracy(set_of_rules.get_rules(), test_examples)
        print('accuracy on test set before pruning is: ' + str(accuracy) + ' %')

        self.accuracy_pre_pruning.append(accuracy)

        for rule in set_of_rules.get_rules():
            print(str(rule.get_preconditions()) + " , " + rule.get_post_condition())

        print('accuracy on validation set before pruning is: ' + str(test_accuracy(set_of_rules.get_rules(), validation_examples)) + ' %')

        # viene eseguita la strategia di pruning sul set di regole
        set_of_rules.rule_pruning(validation_examples)
        # viene calcolata l'accuratezza del test set sul nuovo set di regole
        accuracy = test_accuracy(set_of_rules.get_rules(), test_examples)

        self.accuracy_post_pruning.append(accuracy)

        for rule in set_of_rules.get_rules():
            print(str(rule.get_preconditions()) + " , " + rule.get_post_condition())
        print('accuracy on test set after pruning is: ' + str(accuracy) + ' %')

        print('accuracy on validation set after pruning is: ' + str(test_accuracy(set_of_rules.get_rules(), validation_examples)) + ' %')

    def build_comparison_table(self):
        self._table.add_rows([["Test n.", "Accuratezza pre pruning", "Accuratezza post pruning"]])

        for i in range(len(self.accuracy_pre_pruning)):
            self._table.add_row(
                [str(i + 1), self.accuracy_pre_pruning[i], self.accuracy_post_pruning[i]]
            )

    def print_comparison_table(self):
        self.build_comparison_table()
        print('\nTexttable Table')
        print(self._table.draw())
        self.print_comparison_latex_code()
        # self.reset()

    def print_comparison_latex_code(self):
        print('\nTexttable Latex')
        print(latextable.draw_latex(self._table,
                                    caption="Confronto di accuratezza sul test set prima e dopo l'esecuzione "
                                            "della strategia di pruning"))


def main():
    test = Test()

    index = 1

    for i in range(10):
        test.process(index)
        index += 1

    test.print_comparison_table()


if __name__ == "__main__":
    main()
