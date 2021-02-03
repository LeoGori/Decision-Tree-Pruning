from Node import Node
from Rule import Rule
from SetOfRules import SetOfRules
import copy
from Attribute import Attribute


class Tree:

    def __init__(self):
        self.__root = None
        self.__height = None
        self.__nodes = list()

    def get_nodes(self):
        return self.__nodes

    def set_root(self, attr):
        self.__root = Node(attr)

    def get_root(self):
        return self.__root

    def insert(self, label, node):
        self.insert_node(self.__root, label, node)

    def insert_node(self, current_node, label, node):
        current_node.add_child(label, node)
        node.set_father(current_node)

    def x_order(self):
        self._x_order(self.__root)

    def _x_order(self, v):
        if v.get_children():
            attr = v.get_attribute()
            print(attr.get_name())
            if v.get_father() is not None:
                print(str(v.get_father().get_attribute().get_name()))
            for value in attr.get_set_of_values():
                print("label: " + value + ", node: " + v.get_child(value).get_attribute().get_name())
            for value in attr.get_set_of_values():
                self._x_order(v.get_child(value))

    def get_node(self, node, attr_value):
        return node.get_child(attr_value)

    def prune(self, node, classification_node):
        if node != self.__root:
            father = node.get_father()
            labels = list(father.get_children().keys())
            nodes = list(father.get_children().values())
            father.add_child(labels[nodes.index(node)], classification_node)
            node.set_father(None)

    def update_tree(self, attributes):
        self.__nodes.clear()
        node = self.__root
        self.__nodes.append(node)
        self.__update_tree(node, attributes)

    def __update_tree(self, node, attributes):
        for child in node.get_children().values():
            if child.get_attribute() in attributes:
                self.__nodes.append(child)
                self.__update_tree(child, attributes)

    def get_height(self):
        return max(self.__nodes)

    def get_set_of_rules(self):
        node = self.__root
        rules = SetOfRules()
        rule = Rule()
        self.__get_set_of_rules(node, rules, rule)
        return rules

    def __get_set_of_rules(self, current_node, rules, rule):
        if current_node.get_children():
            for label, node in current_node.get_children().items():
                rule.add_precondition(current_node.get_attribute().get_name(), label)
                self.__get_set_of_rules(node, rules, rule)
                rule.remove_precondition(current_node.get_attribute().get_name())
        else:
            rule.set_post_condition(current_node.get_attribute().get_name())
            rule_copy = copy.deepcopy(rule)
            rules.add_rule(rule_copy)
