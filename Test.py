import latextable as latextable
from texttable import Texttable
import csv
from Example import Example
from SetOfRules import *
from Decision_Tree_Learning import *


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


class Test:

    def __init__(self):

        self._table = Texttable()
        self._table.set_cols_align(["c"] * 5)
        self._table.set_cols_dtype(['i', 'f', 'i', 'f', 'i'])
        self.accuracy_pre_pruning = []
        self.rule_set_size_pre_pruning = []
        self.accuracy_post_pruning = []
        self.rule_set_size_post_pruning = []

    def process(self, index):
        print("test n." + str(index))
        data = import_data()

        X, Y, x_train, x_validation, x_test, y_train, y_validation, y_test = split_dataset(data)

        #print(str(len(X)) + ', ' + str(len(x_train)) + ', ' + str(len(x_test)) + ', ' + str(len(x_validation)))

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

        # stampa l'albero
        tree.x_order()

        # definisce il set di regole estratto dalla struttura dell'albero
        set_of_rules = tree.get_set_of_rules()
        set_of_rules.set_default_rule(get_max_classification_occurrences(training_examples))

        #calcola l'accuratezza del set di regole sul training set
        accuracy = set_of_rules.test_accuracy(training_examples)
        print('accuracy on training set is: ' + str(accuracy) + ' %')

        # calcola l'accuratezza del set di regole sul test set prima di eseguire la strategia di pruning
        accuracy = set_of_rules.test_accuracy(test_examples)
        print('accuracy on test set before pruning is: ' + str(accuracy) + ' %')

        self.accuracy_pre_pruning.append(accuracy)
        self.rule_set_size_pre_pruning.append(set_of_rules.get_size())

        print("Il set di regole derivato dalla struttura dell'albero è: ")
        for rule in set_of_rules.get_rules():
            print(str(rule.get_preconditions()) + " , " + rule.get_post_condition())

        print('accuracy on validation set before pruning is: ' + str(set_of_rules.test_accuracy(validation_examples)) + ' %')

        # viene eseguita la strategia di pruning sul set di regole
        set_of_rules.rule_pruning(validation_examples)
        # viene calcolata l'accuratezza del test set sul nuovo set di regole
        accuracy = set_of_rules.test_accuracy(test_examples)

        self.accuracy_post_pruning.append(accuracy)
        self.rule_set_size_post_pruning.append(set_of_rules.get_size())

        print("Il set di regole dopo la strategia di pruning è: ")
        for rule in set_of_rules.get_rules():
            print(str(rule.get_preconditions()) + " , " + rule.get_post_condition())
        print('accuracy on test set after pruning is: ' + str(accuracy) + ' %')

        print('accuracy on validation set after pruning is: ' + str(set_of_rules.test_accuracy(validation_examples)) + ' %')

    def build_comparison_table(self):
        self._table.add_rows([["Test n.", r'\t' + "head{Accuratezza\\\\pre pruning}",
                               r'\t' + "head{Dimensione del Rule-Set\\\\ pre pruning}",
                               r'\t' + "head{Accuratezza\\\\post pruning}",
                               r'\t' + "head{Dimensione del Rule-Set\\\\post pruning}"]])

        for i in range(len(self.accuracy_pre_pruning)):
            self._table.add_row(
                [str(i + 1), str(self.accuracy_pre_pruning[i])[0:6] + " \%", self.rule_set_size_pre_pruning[i],
                 str(self.accuracy_post_pruning[i])[0:6] + " \%", self.rule_set_size_post_pruning[i]]
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

# def get_num_istances_per_classification(classification):
#     classifications = dict()
#
#     for c in classification.get_values():
#         classifications[c] = 0
#
#     print(classifications)
#
#     for c in Y:
#         classifications[c] += 1
#
#     print(classifications)


def main():
    test = Test()

    index = 1

    for i in range(10):
        test.process(index)
        index += 1

    test.print_comparison_table()


if __name__ == "__main__":
    main()
