class SimulationObjects:
    def __init__(self, x, y, movement_distance):
        self.__x = x
        self.__y = y
        self.__movement_distance = movement_distance

    def print(self):
        print(self.__x, self.__y)

    def increment_x_by_distance(self):
        self.__x = round(self.__x + self.__movement_distance, 1)

    def decrement_x_by_distance(self):
        self.__x = round(self.__x - self.__movement_distance, 1)

    def increment_y_by_distance(self):
        self.__y = round(self.__y + self.__movement_distance, 1)

    def decrement_y_by_distance(self):
        self.__y = round(self.__y - self.__movement_distance, 1)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_x(self, new_x):
        self.__x = new_x

    def set_y(self, new_y):
        self.__y = new_y

    def get_movement_distance(self):
        return self.__movement_distance