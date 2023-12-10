class SimulationObjects:
    def __init__(self, x, y, movement_distance):
        self.x = x
        self.y = y
        self.movement_distance = movement_distance

    def print(self):
        print(self.x, self.y)

    def increment_x_by_distance(self):
        self.x = round(self.x + self.movement_distance, 1)

    def decrement_x_by_distance(self):
        self.x = round(self.x - self.movement_distance, 1)

    def increment_y_by_distance(self):
        self.y = round(self.y + self.movement_distance, 1)

    def decrement_y_by_distance(self):
        self.y = round(self.y - self.movement_distance, 1)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
