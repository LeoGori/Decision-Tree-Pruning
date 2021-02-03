class Example:

    def __init__(self):
        self._values = dict()
        self.__classification = None

    def add_value(self, attr_name, value):
        self._values.setdefault(attr_name, value)

    def get_value(self, attr_name):
        return self._values.get(attr_name)

    def get_values(self):
        return self._values

    def set_classification(self, classification):
        self.__classification = classification

    def get_classification(self):
        return self.__classification
