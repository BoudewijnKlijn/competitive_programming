class Schedule:
    def __init__(self, intersection, street_duration_tuples):
        self.street_duration_tuples = street_duration_tuples
        self.intersection = intersection

    def __str__(self):
        text = f'{self.intersection}\n{len(self.street_duration_tuples)}\n'
        for street in self.street_duration_tuples:
            text += f'{street[0]} {street[1]}\n'

        return text
