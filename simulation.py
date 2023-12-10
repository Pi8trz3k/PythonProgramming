import math
import sheep
import wolf

MAXIMUM_NUMBER_OF_ROUNDS = 1
NUMBER_OF_SHEEP = 15
NUMBER_OF_WOLF = 1

herd_of_sheep = [sheep.Sheep() for shp in range(NUMBER_OF_SHEEP)]
wolf = wolf.Wolf()

def move_sheep(sheep_count):
    for shep_number in range(sheep_count):
        herd_of_sheep[shep_number].move()

def get_distance(obj1, obj2):
    return round(math.sqrt(pow(obj1.get_x() - obj2.get_x(), 2) + pow(obj1.get_y() - obj2.get_y(), 2)), 3)

def get_the_closest_sheep():
    distance = get_distance(herd_of_sheep[0], wolf)
    actual_the_closest_sheep = herd_of_sheep[0]
    sheep_number = 0

    for i in range(1, len(herd_of_sheep)):
        current_distance = get_distance(herd_of_sheep[i], wolf)

        if current_distance < distance:
            distance = current_distance
            actual_the_closest_sheep = herd_of_sheep[i]
            sheep_number = i

    return actual_the_closest_sheep, sheep_number

def game():

    # TO BE REMOVED
    print("----------------------------")
    for i in range(len(herd_of_sheep)):
        herd_of_sheep[i].print()
    print("----------------------------")

    is_chasing = False

    for round_number in range(MAXIMUM_NUMBER_OF_ROUNDS):
        #first stage
        # move_sheep(len(herd_of_sheep))

        # wolf.increment_x_by_distance()

        the_closest_sheep, sheep_number = get_the_closest_sheep()

        the_closest_sheep.print()
        print("closest num", sheep_number + 1)

        # #second stage
        # for i in range(len(herd_of_sheep)):
        #     distance = get_distance(herd_of_sheep[i], wolf)
        #     print("distance:", distance)
        #     print("wolf print")
        #     wolf.print()
        #     print("shep print")
        #     herd_of_sheep[i].print()
        #     break
        #
        # print("Round number:", round_number)
        # print("Position of wolf: ", round(wolf.get_x(), 3), round(wolf.get_y(), 3))
        # print("Number of alive sheeps:", len(herd_of_sheep))
        #
        # print()


game()
