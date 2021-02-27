class SimulatorSchedule:
    def __init__(self):
        self.street_names = []
        self.street_schedule = []

    def append(self, street_name, seconds):
        self.street_names.append(street_name)
        index = len(self.street_names) - 1
        self.street_schedule += [index] * seconds

    def __getitem__(self, item):
        return self.street_names[self.street_schedule[item]]
