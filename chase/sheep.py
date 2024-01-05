import random
import simulation_objects as so

class Sheep(so.SimulationObjects):
    def __init__(self, sequence_number):
        super().__init__(round(random.uniform(-10.0, 10.0), 1), round(random.uniform(-10.0, 10.0), 1), 0.5)
        self.__sequence_number = sequence_number
        self.__is_alive = True

    def choose_direction(self):
        """
        Values:
        1 - up (north)
        2 - right (east)
        3 - down (south)
        4 - left (west)
        """
        return random.randint(1, 4)

    def move(self):
        direction = self.choose_direction()

        match direction:
            case 1:
                self.increment_y_by_distance()
            case 2:
                self.increment_x_by_distance()
            case 3:
                self.decrement_y_by_distance()
            case 4:
                self.decrement_x_by_distance()

    def get_sequence_number(self):
        return self.__sequence_number

    def set_sequence_number(self, new_sequence_number):
        self.__sequence_number = new_sequence_number

    def is_alive(self):
        return self.__is_alive

    def set_is_not_alive(self):
        self.__is_alive = False
