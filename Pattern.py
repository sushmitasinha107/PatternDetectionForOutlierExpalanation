class Pattern:
    fixed = None
    variable = None
    value = None
    pattern = None
    metric = None

    def __init__(self, fixed, variable, value, pattern, metric):
        self.fixed = fixed
        self.variable = variable
        self.value = value
        self.pattern = pattern
        self.metric = metric

    def get_fixed(self):
        return self.fixed

    def get_variable(self):
        return self.variable

    def get_value(self):
        return self.value

    def get_pattern(self):
        return self.pattern

    def get_metric(self):
        return self.metric
