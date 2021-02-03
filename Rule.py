class Rule:
    def __init__(self):
        self.__pre_conditions = dict()
        self.__post_condition = None

    def add_precondition(self, attribute_name, value):
        self.__pre_conditions[attribute_name] = value

    def remove_precondition(self, attribute_name):
        self.__pre_conditions.pop(attribute_name)

    def get_preconditions(self):
        return self.__pre_conditions

    def set_post_condition(self, classification):
        self.__post_condition = classification

    def get_post_condition(self):
        return self.__post_condition

    def __eq__(self, other):
        if isinstance(other, Rule):
            return self.__pre_conditions == other.get_preconditions() and \
                   self.__post_condition == other.get_post_condition()
        return False

    def __hash__(self):
        return hash(('preconditions', str(self.__pre_conditions),
                     'post_condition', self.__post_condition))
