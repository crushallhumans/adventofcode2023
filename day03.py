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

        if len(tracking_number_obj[0]):
            coord_hash = tracking_number_obj[2]
            number_map.add((tracking_number_obj[0],str(coord_hash)))
            for k in tracking_number_obj[1]:
                number_membership_map[k] = (tracking_number_obj[0],str(coord_hash))

        y += 1
    
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


#    if DEBUG: pp.pprint(included_numbers.keys())
    if DEBUG and 'DESPERATE' == 0:
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
    print("""
--- Day N: X ---

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
