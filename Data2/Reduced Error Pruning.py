def test_accuracy(tree, examples):
    current_node = tree.get_root()
    num_success = 0
    for example in examples:
        # print(str(tree.get_node(current_node, example.get_value(current_node.get_attribute().get_name()))))
        # print(example.get_value('parents'))
        while tree.get_node(current_node, example.get_value(current_node.get_attribute().get_name())):
            current_node = tree.get_node(current_node, example.get_value(current_node.get_attribute().get_name()))
        # print(str(current_node.get_attribute().get_name()) + " , " + str(example.get_classification()))
        if current_node.get_attribute().get_name() == example.get_classification():
            num_success = num_success + 1
        current_node = tree.get_root()
    accuracy = (num_success / len(examples)) * 100
    return accuracy


def reduced_error_pruning(tree, attributes, examples):
    while True:
        tree_copy = copy.deepcopy(tree)
        tree_copy.update_tree(attributes)
        accuracy = test_accuracy(tree_copy, examples)
        accuracy_gain = 0
        best_node_to_prune = None
        pruned_classification_node = None
        sub_examples = list()
        attribute_value = None
        for node in tree_copy.get_nodes():
            if node.get_father() is not None:
                father = node.get_father()
                children = father.get_children()
                for label, value in children.items():
                    if value == node:
                        attribute_value = label
                for example in examples:
                    if example.get_value(node.get_father().get_attribute().get_name()) == attribute_value:
                        sub_examples.append(example)
                classification_node = plurality_value(sub_examples).get_root()
                tree_copy.prune(node, classification_node)
                pruned_accuracy = test_accuracy(tree_copy, examples)
                print(str(accuracy), str(pruned_accuracy) + " se pruning eseguito su attributo " + node.get_attribute().get_name())
                if accuracy_gain <= pruned_accuracy - accuracy:
                    accuracy_gain = pruned_accuracy - accuracy
                    best_node_to_prune = tree.get_nodes()[tree.get_nodes().index(node)]
                    pruned_classification_node = classification_node
                sub_examples.clear()
                tree_copy.insert_node(father, attribute_value, node)
        if best_node_to_prune is not None:
            tree.prune(best_node_to_prune, pruned_classification_node)
            tree.update_tree(attributes)
        else:
            break