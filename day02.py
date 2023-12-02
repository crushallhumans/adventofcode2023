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
    print("""--- Day 2: Cube Conundrum ---
You're launched high into the atmosphere! The apex of your trajectory just barely reaches the surface of a large island floating in the sky. You gently land in a fluffy pile of leaves. It's quite cold, but you don't see much snow. An Elf runs over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow. He'll be happy to explain the situation, but it's a bit of a walk, so you have some time. They don't get many visitors up here; would you like to play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. Each time you play this game, he will hide a secret number of cubes of each color in the bag, and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag, grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input). Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?

--- Part Two ---
The Elf says they've stopped producing snow because they aren't getting any water! He isn't sure why the water stopped; however, he can show you how to get to the water source to check it out for yourself. It's just up ahead!

As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
Game 4 required at least 14 red, 3 green, and 15 blue cubes.
Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?

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
