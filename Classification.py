class Classification:

    __instance = None
    __values = list()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Classification, cls).__new__(cls)
            # Put any initialization here.
        return cls.__instance

    def set_value(self, value):
        self.__values.append(value)

    def get_values(self):
        return self.__values
