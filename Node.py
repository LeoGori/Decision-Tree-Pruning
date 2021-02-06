from Attribute import Attribute


class Node:
    def __init__(self, attr):
        self._attribute = attr
        self._children = dict()
        self._father = None
        self._examples = None
        #self._level = None

    def add_child(self, label, node):
        self._children[label] = node

    def get_children(self):
        return self._children

    def get_child(self, label):
        return self._children.get(label)

    def set_attribute(self, attr):
        self._attribute = attr

    def get_attribute(self):
        return self._attribute

    def get_father(self):
        return self._father

    def set_father(self, node):
        self._father = node

    def print(self):
        print(self._attribute)

    def __str__(self):
        string = "nodo " + str(self._attribute.get_name())
        if self._father:
            string += " con padre " + str(self._father.get_attribute().get_name()) + ","
        string += " con figli:"
        for label, node in self._children.items():
            string += "\n(" + label + ", " + node.get_attribute().get_name() + ")"
        
        return string

    def __eq__(self, other):
        if isinstance(other, Node):
            return self._attribute == other.get_attribute()
        return False


    # def set_examples(self, data):
    #     self._examples = data
    #
    # def get_examples(self):
    #     return self._examples

    # def set_level(self, lv):
    #     self._level = lv
    #
    # def get_level(self):
    #     return self._level