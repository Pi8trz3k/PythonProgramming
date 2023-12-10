import random
import simulation_objects as so

class Sheep(so.SimulationObjects):
    def __init__(self):
        super().__init__(round(random.uniform(-10.0, 10.0), 1), round(random.uniform(-10.0, 10.0), 1), 0.5)

    def choose_direction(self):
        """
        Method returns direction in which sheep will move

        Values:
        1 - up (north)
        2 - right (east)
        3 - down (south)
        4 - left (west)

        :return:
            int: Number which indicates what direction will be chosen
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