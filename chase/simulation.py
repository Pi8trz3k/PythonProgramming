import math
import csv
import json
from os.path import exists
from sheep import Sheep
from wolf import Wolf

MAXIMUM_NUMBER_OF_ROUNDS = 50
NUMBER_OF_SHEEP = 15
NUMBER_OF_WOLF = 1

herd_of_sheep = [Sheep(sheep + 1) for sheep in range(NUMBER_OF_SHEEP)]
wolf = Wolf()

def move_sheep():
    for shep_number in range(len(herd_of_sheep)):
        if herd_of_sheep[shep_number].is_alive():
            herd_of_sheep[shep_number].move()

def get_distance(sheep, wolff):
    return round(math.sqrt(pow(sheep.get_x() - wolff.get_x(), 2) + pow(sheep.get_y() - wolff.get_y(), 2)), 3)

def get_the_closest_sheep():
    distance = None
    actual_the_closest_sheep = None
    sheep_number = None

    # find 1 sheep that's alive - first or second sheep after few round can be dead
    for i in range(len(herd_of_sheep)):
        if herd_of_sheep[i].is_alive():
            distance = get_distance(herd_of_sheep[i], wolf)
            actual_the_closest_sheep = herd_of_sheep[i]
            sheep_number = i
            break

    # goind through herd and if sheep is alive - count distance
    for i in range(len(herd_of_sheep)):
        if herd_of_sheep[i].is_alive():
            current_distance = get_distance(herd_of_sheep[i], wolf)

            if current_distance < distance:
                distance = current_distance
                actual_the_closest_sheep = herd_of_sheep[i]
                sheep_number = i

    return actual_the_closest_sheep, sheep_number

def is_within_range_of_attack(sheep, wolff):
    if get_distance(sheep, wolf) <= wolff.get_movement_distance():
        return True
    else:
        return False

def set_new_position(wolff, sheep):
    wolf_x, wolf_y = wolff.get_x(), wolff.get_y()
    sheep_x, sheep_y = sheep.get_x(), sheep.get_y()

    distance_increment_x = ((wolf_x + 1) - sheep_x) ** 2 + (wolf_y - sheep_y) ** 2
    distance_decrement_x = ((wolf_x - 1) - sheep_x) ** 2 + (wolf_y - sheep_y) ** 2

    distance_increment_y = (wolf_x - sheep_x) ** 2 + ((wolf_y + 1) - sheep_y) ** 2
    distance_decrement_y = (wolf_x - sheep_x) ** 2 + ((wolf_y - 1) - sheep_y) ** 2

    min_distance = min(distance_increment_x, distance_decrement_x,
                       distance_increment_y, distance_decrement_y)

    if min_distance == distance_increment_x:
        wolff.increment_x_by_distance()
    elif min_distance == distance_decrement_x:
        wolff.decrement_x_by_distance()
    elif min_distance == distance_increment_y:
        wolff.increment_y_by_distance()
    else:
        wolff.decrement_y_by_distance()

def write_to_csv(round_number, alive_sheep):
    file_exists = exists('alive.csv')

    with open('alive.csv', 'a', newline='') as csv_file:
        if file_exists:
            writer = csv.writer(csv_file)
            writer.writerow((round_number, alive_sheep))
        else:
            field_names = ['round number', 'sheep alive']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerow({'round number': round_number, 'sheep alive': alive_sheep})

def number_of_sheep_alive():
    alive_count = 0
    for i in range(len(herd_of_sheep)):
        if herd_of_sheep[i].is_alive():
            alive_count += 1
    return alive_count

def get_sheep_position_list():
    position_list = []
    for i in range(len(herd_of_sheep)):
        if herd_of_sheep[i].is_alive():
            position_list.append((herd_of_sheep[i].get_x(), herd_of_sheep[i].get_y()))
        else:
            position_list.append(('null', 'null'))

    return position_list

def delete_last_character():
    with open('pos.json', 'rb+') as fh:
        fh.seek(-1, 2)
        fh.truncate()

def write_to_json(round_number):

    if exists('pos.json'):
        if round_number == 1:
            delete_last_character()
            with open('pos.json', 'a') as json_file:
                json_file.write(',{{'
                                '\n\t"round_no": {round_no},'
                                '\n\t"wolf_pos": {wolf_pos},'
                                '\n\t"sheep_pos": {sheep_pos}'
                                '\n}},\n'
                .format(
                    round_no=round_number,
                    wolf_pos=json.dumps(wolf.to_dict()),
                    sheep_pos=json.dumps(get_sheep_position_list())
                ))
        elif round_number == 50:
            with open('pos.json', 'a') as json_file:
                json_file.write('{{'
                                '\n\t"round_no": {round_no},'
                                '\n\t"wolf_pos": {wolf_pos},'
                                '\n\t"sheep_pos": {sheep_pos}'
                                '\n}}]'
                .format(
                    round_no=round_number,
                    wolf_pos=json.dumps(wolf.to_dict()),
                    sheep_pos=json.dumps(get_sheep_position_list())
                ))
        else:
            with open('pos.json', 'a') as json_file:
                json_file.write('{{'
                                '\n\t"round_no": {round_no},'
                                '\n\t"wolf_pos": {wolf_pos},'
                                '\n\t"sheep_pos": {sheep_pos}'
                                '\n}},\n'
                .format(
                    round_no=round_number,
                    wolf_pos=json.dumps(wolf.to_dict()),
                    sheep_pos=json.dumps(get_sheep_position_list())
                ))
    else:
        with open('pos.json', 'a') as json_file:
            json_file.write('[{{'
                            '\n\t"round_no": {round_no},'
                            '\n\t"wolf_pos": {wolf_pos},'
                            '\n\t"sheep_pos": {sheep_pos}'
                            '\n}},\n'
            .format(
                round_no=round_number,
                wolf_pos=json.dumps(wolf.to_dict()),
                sheep_pos=json.dumps(get_sheep_position_list())
            ))

def game():
    is_chasing = False
    eaten = False
    the_closest_sheep = None
    the_closest_sheep_sheep_number = None

    for round_number in range(MAXIMUM_NUMBER_OF_ROUNDS):
        move_sheep()

        if is_chasing:
            if is_within_range_of_attack(the_closest_sheep, wolf):
                wolf.set_x(the_closest_sheep.get_x())
                wolf.set_y(the_closest_sheep.get_y())

                the_closest_sheep.set_x(None)
                the_closest_sheep.set_y(None)
                the_closest_sheep.set_is_not_alive()

                is_chasing = False

                eaten = True
            else:
                set_new_position(wolf, the_closest_sheep)
        else:
            the_closest_sheep, the_closest_sheep_sheep_number = get_the_closest_sheep()

            if is_within_range_of_attack(the_closest_sheep, wolf):
                wolf.set_x(the_closest_sheep.get_x())
                wolf.set_y(the_closest_sheep.get_y())

                the_closest_sheep.set_x(None)
                the_closest_sheep.set_y(None)
                the_closest_sheep.set_is_not_alive()

                eaten = True
            else:
                is_chasing = True
                set_new_position(wolf, the_closest_sheep)

        print("Round number:", round_number + 1, "wolf position:", wolf.get_x(), wolf.get_y(), "sheep alive: ",
              number_of_sheep_alive())

        if is_chasing:
            print("Wolf is chasing sheep", the_closest_sheep.get_sequence_number())
        if eaten:
            print("Sheep with number", the_closest_sheep.get_sequence_number() , "was eaten")
            eaten = False

        write_to_json(round_number + 1)
        write_to_csv(round_number + 1, number_of_sheep_alive())

        if number_of_sheep_alive() == 0:
            print("Game ended, every sheep has been eaten")
            break

        print()

game()
