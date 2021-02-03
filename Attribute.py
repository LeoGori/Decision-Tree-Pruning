class Attribute:

    def __init__(self, name):
        self._name = name
        self.__set_of_values = []

    def add_value(self, values):
        self.__set_of_values.append(values)

    def get_set_of_values(self):
        return self.__set_of_values

    def get_name(self):
        return self._name

    def __eq__(self, other):
        if isinstance(other, Attribute):
            return self._name == other.get_name()
        return False


