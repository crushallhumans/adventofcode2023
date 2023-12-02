# adventofcode 2023
# crushallhumans
# puzzle 2
# 12/2/2023

import os
import re
import sys
import math
import unittest
import pprint
pp = pprint.PrettyPrinter()
from functools import reduce

DEBUG = False

def one_star(param_set, cube_definition, is_one_star = True):
    if is_one_star: print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    c = 8888
    if DEBUG: pp.pprint(param_set)
    cube_max = 0
    if cube_definition:
        for k in cube_definition.keys():
            cube_max += cube_definition[k]
    possible_sum = 0
    for i in param_set:
        possible_game = True
        for j in i['set_objects']:
            if j['cube_sum'] > cube_max:
                possible_game = False
            for k in cube_definition.keys():
                if k in j.keys():
                    if j[k] > cube_definition[k]:
                        possible_game = False
        if is_one_star:
            if possible_game:
                possible_sum += int(i['game_index'])
        else:
            possible_sum += reduce(lambda x, y: x*y, i['maximums'].values())
    return possible_sum


def two_star(param_set):
    print("---------------two_star--------------------")
    return one_star(param_set,{},False)

def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    rr = re.compile('^Game (\d+): (.*)$')
    game_objects = []
    for i in param_set:
        game_parts = re.findall(rr,i)
        game_index = game_parts[0][0]
        cube_string = game_parts[0][1]
        cube_sets = cube_string.split('; ')
        set_objects = []
        maximums = {}
        for cs in cube_sets:
            set_object = {'cube_sum':0}
            color_sets = cs.split(', ')
            if DEBUG: print(color_sets)
            for color_set in color_sets:
                color_set_split = color_set.split(' ')
                color_name = color_set_split[1]
                color_int = int(color_set_split[0])
                set_object[color_name] = color_int
                set_object['cube_sum'] += color_int
                if color_name not in maximums.keys():
                    maximums[color_name] = 0
                if color_int > maximums[color_name]:
                    maximums[color_name] = color_int
            set_objects.append(set_object.copy())
        game_objects.append({
            'game_index':game_index,
            'set_objects':set_objects.copy(),
            'maximums':maximums.copy()
        })
        if DEBUG: print("")
    return game_objects    


def puzzle_text():
    print("""
--- Day N: X ---

""")



class testCase(unittest.TestCase):
    global DEBUG
    DEBUG = True

    test_set = (
        """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""",
        {'red':12,'green':13,'blue':14}
    )

    def test_one_star(self):
        self.assertEqual(
            one_star(
                self.__class__.test_set[0],
                self.__class__.test_set[1],
            ),
            8
        )

    def test_two_star(self):
        self.assertEqual(
            two_star(
                self.__class__.test_set[0]
            ),
            2286
        )



if __name__ == '__main__':
    try:
        sys.argv[1]
        puzzle_text()

    except:
        DEBUG = False
        filename_script = os.path.basename(__file__)
        print("---------------%s--------------------"%filename_script)
        filename = filename_script.split('.')[0]
        input_set = ()
        with open("/Users/crushing/Development/crushallhumans/adventofcode2023/inputs/2023/%s.txt" % filename) as input_file:
            input_set = [input_line.strip() for input_line in input_file]
        ret = one_star(input_set,{'red':12,'green':13,'blue':14})
        print (ret)

        ret = two_star(input_set)
        print (ret)
