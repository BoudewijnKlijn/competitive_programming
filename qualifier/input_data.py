
class Street:

    def __init__(self, begin, end, name, time):
        self.begin = begin  # Begin intersection (integer)
        self.end = end  # End intersection (integer)
        self.name = name
        self.time = time  # Time it takes to drive this street


class Car:

    def __init__(self, n_streets, path):
        self.n_streets = n_streets  # N streets in path
        self.path = path  # List of street names
        assert len(self.path) == self.n_streets


class InputData:

    def __init__(self, filename: str):
        with open(filename) as file:
            lines = file.readlines()

        # Read properties of problem
        first_line_elements = lines[0].split(" ")
        self.duration = int(first_line_elements[0])  # Duration of the simulation
        self.n_intersections = int(first_line_elements[1])
        self.n_streets = int(first_line_elements[2])
        self.n_cars = int(first_line_elements[3])
        # bonus = the bonus points per car who reaches its destination within duration of simulation
        self.bonus = int(first_line_elements[4])

        # Read streets
        self.streets = []
        street_lines = lines[1:1 + self.n_streets]
        for street_line in street_lines:
            line_elements = street_line.split(" ")
            self.streets.append(Street(
                begin=int(line_elements[0]),
                end=int(line_elements[1]),
                name=line_elements[2],
                time=int(line_elements[3])),
            )
        assert len(self.streets) == self.n_streets

        # Read cars
        self.cars = []
        car_lines = lines[1 + self.n_streets:]
        for car_line in car_lines:
            line_elements = car_line.split(" ")
            self.cars.append(Car(
                n_streets=int(line_elements[0]),
                path=line_elements[1:]
            ))


    # def get_data(self):
    #     return self.data
