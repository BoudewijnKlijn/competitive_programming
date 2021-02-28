from copy import deepcopy


class Schedule:
    def __init__(self, intersection, street_duration_tuples):
        if not isinstance(street_duration_tuples, tuple):
            raise ValueError(f'Expected type tuple for street_duration_tuples but got {type(street_duration_tuples)}')

        self.street_duration_tuples = street_duration_tuples
        self.intersection = intersection

    # def __deepcopy__(self):
    #     return Schedule(self.intersection, tuple([deepcopy(t) for t in self.street_duration_tuples]))

    def __str__(self):
        # dont add 0 duration streets
        final = [street for street in self.street_duration_tuples if street[1] > 0]

        text = f'{self.intersection}\n{len(final)}\n'
        for street in final:
            text += f'{street[0]} {street[1]}\n'

        return text
