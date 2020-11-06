

class RunningAverage:
    def __init__(self):
        self.values = []

    def add(self, val):
        self.values.append(val)

    def add_all(self, vals):
        self.values += vals

    def get(self):
        return sum(self.values) / len(self.values)

    def flush(self):
        self.values = []
