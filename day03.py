# adventofcode 2023
# crushallhumans
# puzzle 3
# 12/3/2023

import os
import re
import sys
import math
import unittest
import pprint
import random
pp = pprint.PrettyPrinter()
from functools import reduce

DEBUG = False

def one_star(param_set, step_two = False):
    print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    digit_map = {}
    number_map = set()
    number_membership_map = {}
    symbol_list = []
    gear_list = []
    x = 0
    y = 0
    max_x = len(param_set[0])
    max_y = len(param_set)
    if DEBUG: print('maximums',max_x,max_y)

    # parse grid into sparse map of number and symbol coordinates
    for i in param_set:
        x = 0
        tracking_number_obj = ['',[],'']
        for j in i:
            if DEBUG: print(x,y,j)
            coords = (x,y)
            digit_map[coords] = j
            if re.match(r'[0-9]',j):
                tracking_number_obj[0] += '' + j
                tracking_number_obj[1].append(coords)
                tracking_number_obj[2] += '' + str(x) + ',' + str(y) + ';'
            else:
                if len(tracking_number_obj[0]):
                    coord_hash = tracking_number_obj[2]
                    number_map.add((tracking_number_obj[0],str(coord_hash)))
                    for k in tracking_number_obj[1]:
                        number_membership_map[k] = (tracking_number_obj[0],str(coord_hash))
                tracking_number_obj = ['',[],'']
                if j != '.':
                    symbol_list.append(coords)
                    if j == '*':
                        gear_list.append(coords)
            x += 1

        # ugly hack - catch last number on a line before advancing to next line
        if len(tracking_number_obj[0]):
            coord_hash = tracking_number_obj[2]
            number_map.add((tracking_number_obj[0],str(coord_hash)))
            for k in tracking_number_obj[1]:
                number_membership_map[k] = (tracking_number_obj[0],str(coord_hash))

        y += 1
    
    # scan symbol neighborhoods for number coordinates in sparse map
    included_numbers = {}
    found_numbers = set()
    for i in symbol_list:
        x = i[0]
        y = i[1]
        yy = y - 1
        for c in range(0,3):
            xx = x - 1
            for d in range(0,3):
                if (xx,yy) != (x,y) and (xx,yy) in number_membership_map:
                    if DEBUG: print((number_membership_map[(xx,yy)],i))
                    found_numbers.add(number_membership_map[(xx,yy)])
                    included_numbers[(number_membership_map[(xx,yy)],i)] = True
                xx += 1
            yy += 1

    # step 2 - only process the neighborhoods of 'gear' symbols, further process 2-key membership
    gears_with_two = []
    gears_with_two_sum = 0
    for i in gear_list:
        x = i[0]
        y = i[1]
        yy = y - 1
        gear_number_total = {}
        for c in range(0,3):
            xx = x - 1
            for d in range(0,3):
                if (xx,yy) != (x,y) and (xx,yy) in number_membership_map:
                    gear_number_total[(number_membership_map[(xx,yy)])] = True
                xx += 1
            yy += 1
        gear_keylist = list(gear_number_total.keys())
        if len(gear_keylist) == 2:
            if DEBUG: pp.pprint(gear_keylist)
            gears_with_two.append(i)
            gears_with_two_sum += int(gear_keylist[0][0]) * int(gear_keylist[1][0])

    # omg I made a mistake
    # I wasn't processing numbers if they were last on a line 
    # and drove myself crazy debugging the neighborhood scanners instead
    if DEBUG and 'DESPERATE' == 0:
        found_numbers_by_symbols = set()
        for i,v in number_membership_map.items():
            x = i[0]
            y = i[1]
            yy = y - 1
            for c in range(0,3):
                xx = x - 1
                for d in range(0,3):
                    if (xx,yy) != (x,y) and (xx,yy) in symbol_list:
                        found_numbers_by_symbols.add(v)
                    xx += 1
                yy += 1

            # so much set differencing to find nothing
            print('DEBUG:') 
            print('all:') 
            pp.pprint(number_map)
            print('found:') 
            pp.pprint(found_numbers)
            xset = number_map - found_numbers
            print('not found:') 
            pp.pprint(xset)
            print('included:') 
            pp.pprint(included_numbers) 
            print('found reversed:') 
            pp.pprint(found_numbers_by_symbols) 
            xxset = found_numbers_by_symbols.difference(found_numbers)
            print('sym->num x num->sym:') 
            pp.pprint(xxset)
            print('end not found:') 
                # it is not 524899
            print(sum(map(lambda x:int(x[0]),found_numbers)))

    if step_two:
        return gears_with_two_sum

    return sum(map(lambda x:int(x[0]),found_numbers))


def two_star(param_set):
    print("---------------two_star--------------------")
    return one_star(param_set,True)

def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    return param_set    


def puzzle_text():
    print("""--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
          

--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

""")



class testCase(unittest.TestCase):
    global DEBUG
    DEBUG = True

    test_set = (
        """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    )

    def test_one_star(self):
        self.assertEqual(
            one_star(
                self.__class__.test_set
            ),
            4361
        )

    def test_two_star(self):
        self.assertEqual(
            two_star(
                self.__class__.test_set
            ),
            467835
        )



if __name__ == '__main__':
    DEBUG = False
    try:
        sys.argv[1]
        puzzle_text()

    except:
        filename_script = os.path.basename(__file__)
        print("---------------%s--------------------"%filename_script)
        filename = filename_script.split('.')[0]
        input_set = ()
        with open("/Users/crushing/Development/crushallhumans/adventofcode2023/inputs/2023/%s.txt" % filename) as input_file:
            input_set = [input_line.strip() for input_line in input_file]
        ret = one_star(input_set)
        print (ret)

        ret = two_star(input_set)
        print (ret)
