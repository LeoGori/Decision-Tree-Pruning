# Implementation of a learning strategy and decision tree pruning
In the following repository, algorithms for learning decision trees are implemented using entropy as a measure of impurity (described in the book "Artificial Intelligence: A Modern Approach," P. Norvig, S. Russell, §18.3) and a pruning strategy on a set of rules extracted from the tree structure based on the error on the validation set (described in the book "Machine Learning," T. Mitchell, §3.7.1.2).

# How to use the code
To execute the test for comparing accuracy before and after applying the pruning strategy, it is necessary to download the [Nursery dataset](https://archive.ics.uci.edu/ml/datasets/Nursery) and place the 'nursery.data' file inside the 'Data' directory. After that, to run the tests described in the report, simply execute the `Test.py` file.

# Code description
The files that make up the project are:

- [**_Classification.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Classification.py): a class that gathers the possible classifications of the dataset, defined in the 'Classification' file inside the 'Data' directory. For convenience, the file is initialized with the classifications of the Nursery dataset but can be overwritten for the use of other datasets. **Note**: various classifications must be separated by ", " (e.g., 'TRUE, FALSE').
- [**_Attribute.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Example.py): a class that collects attribute names and their legal values, defined in the 'Attributes and values' file inside the 'Data' directory. For convenience, the file is initialized with the attributes followed by their legal values for the Nursery dataset but can be overwritten for the use of other datasets. **Note**: each line starts with the attribute name, followed by its distinct values separated by "," (e.g., 'color,red,green,yellow').
- [**_Example.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Example.py): a class that records (Attribute, Value) pairs for each attribute of a dataset example.
- [**_Node.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Node.py): a class representing a node entity for building a decision tree, which records the chosen attribute values based on information gain using entropy.
- [**_Tree.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Tree.py): a class that collects elements of type **Node** in a tree-like structure.
- [**_Rule.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Rule.py): a class representing a decision rule, which records a set of (Attribute, Value) pairs as _Preconditions_ and the corresponding classification as _Postcondition_.
- [**_SetOfRules.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/SetOfRules.py): a class that collects a list of elements of type **Rule** responsible for executing the pruning strategy and subsequently sorting the decision list.
- [**DecisionTreeLearning.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/DecisionTreeLearning.py): a file containing functions for learning the decision tree.
- [**_Test.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Test.py): a class that performs tests on decision trees generated on randomly selected portions of the dataset and records the accuracy values of decision structures before and after the pruning strategy.

# Language and libraries
The project was implemented using _Python 3.8_ as the programming language. The following libraries were also used:

- **copy**: to perform the deepcopy of certain lists.
- **texttable**: for generating Latex code to build tables to collect accuracy values.
- **csv and pandas**: for reading information such as dataset examples from csv-type text files.
- **sklearn**: for dataset splitting and random extraction of example sets for generating training, validation, and test sets.
- **math**: for using the log(x) function for entropy calculation.
