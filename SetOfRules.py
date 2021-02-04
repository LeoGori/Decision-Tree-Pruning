from Rule import Rule


class SetOfRules:

    def __init__(self):
        self.rules = list()
        self.default_rule = Rule()

    def add_rule(self, rule):
        self.rules.append(rule)

    def get_rules(self):
        return self.rules

    def get_size(self):
        return len(self.rules)

    def set_default_rule(self, classification):
        self.default_rule.set_post_condition(classification)

    def order_set(self, examples):
        d = dict()
        for rule in self.rules:
            d[rule] = test_rule_accuracy(rule, examples)
        d = dict(sorted(d.items(), key=lambda item: item[1]))

        l = [k for k in d]
        l.reverse()

        self.rules = l

    def remove(self, rule):
        self.rules.remove(rule)

    def remove_duplicates(self):
        self.rules = list(dict.fromkeys(self.rules))

    def rule_pruning(self, examples):
        for rule in list(self.rules):
            while True:
                # print('regola ' + str(rule.get_preconditions()) + ', ' + rule.get_post_condition())
                original_accuracy = test_rule_accuracy(rule, examples)
                accuracy_gain = 0
                best_precondition_to_prune = None
                preconditions = list(rule.get_preconditions().items())
                for attribute_name, value in preconditions:
                    rule.remove_precondition(attribute_name)
                    pruned_accuracy = test_rule_accuracy(rule, examples)
                    rule.add_precondition(attribute_name, value)
                    # print(str(original_accuracy), str(pruned_accuracy) + " per precondition " + attribute_name, value)
                    if accuracy_gain < pruned_accuracy - original_accuracy:
                        best_precondition_to_prune = attribute_name
                        accuracy_gain = pruned_accuracy - original_accuracy
                if best_precondition_to_prune is not None:
                    rule.remove_precondition(best_precondition_to_prune)
                    if not rule.get_preconditions():
                        self.rules.remove(rule)
                else:
                    break
        self.order_set(examples)

    def test_accuracy(self, examples):
        if len(examples) == 0:
            return 0
        num_success = 0
        for example in examples:
            output = self.predict(example)
            if output.get_post_condition() == example.get_classification():
                num_success = num_success + 1
        accuracy = (num_success / len(examples)) * 100
        return accuracy

    def predict(self, example):
        values = example.get_values().items()
        for rule in self.rules:
            if rule.get_preconditions().items() <= values:
                return rule
        return self.default_rule

    # def shuffle(self):
    #     random.shuffle(self.rules)


def test_rule_accuracy(rule, examples):
    if len(examples) == 0:
        return 0
    num_success = 0
    num_covers = 0
    for example in examples:
        output = rule_predict(rule, example)
        if output:
            num_covers = num_covers + 1
            if output.get_post_condition() == example.get_classification():
                num_success = num_success + 1
    if num_covers == 0:
        return 0
    accuracy = (num_success / num_covers) * 100
    return accuracy


def test_rule_coverage(rule, examples):
    if len(examples) == 0:
        return 0
    num_covers = 0
    for example in examples:
        output = rule_predict(rule, example)
        if output:
            num_covers = num_covers + 1
    accuracy = (num_covers / len(examples)) * 100
    return accuracy


def rule_predict(rule, example):
    values = example.get_values().items()
    if rule.get_preconditions().items() <= values:
        return rule
    return None
