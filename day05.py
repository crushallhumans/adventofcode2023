# adventofcode 2023
# crushallhumans
# puzzle 5
# 12/5/2023

import os
import re
import sys
import math
import unittest
import socket
import hashlib
import pprint
import random
from functools import reduce
from functools import cache
from multiprocessing import Pool

pp = pprint.PrettyPrinter(indent=1, width=120)

DEBUG = False
parsed_dict = {}

def one_star(param_set, is_two_star = False):
    print("---------------one_star--------------------")
    global parsed_dict
    parsed_dict = reprocess_input(param_set)
    c = -1
    test_dict = {}
    dict_keys = parsed_dict['directed'].keys()

    if is_two_star:
        seed_ranges = parsed_dict['seed']
        actual_seeds = []
        while len(seed_ranges):
            seed_start = seed_ranges.pop(0)
            seed_end = seed_ranges.pop(0)
            for i in range(seed_start,seed_start+seed_end):
                actual_seeds.append(i)
        parsed_dict['seed'] = actual_seeds
    if DEBUG: pp.pprint(parsed_dict)

    # build maps & invert maps

    for i in parsed_dict['seed']:
        current_step = 'seed'
        next_step = 'soil'
        d = 0
        tval = i
        while current_step in dict_keys:
            tval = map_to_val(current_step,next_step,tval)
            if d == 0:
                test_dict[i] = tval
            current_step = next_step
            if current_step in dict_keys:
                next_step = parsed_dict['directed'][current_step]['next_step']
            d +=1
        if tval < c or c == -1:
            c = tval

    return [test_dict,c]


def two_star(param_set):
    print("---------------two_star--------------------")
    return one_star(param_set,True)

def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    parsed_dict = {
        'initial': {},
        'directed': {}
    }
    print('boo!' , param_set[0])
    parsed_dict['seed'] = list(map(lambda x:int(x),param_set.pop(0).split(': ')[1].split(' ')))
    param_set.pop(0)
    current_map_name = {}
    category_map = {}
    for i in param_set:
        title_re = re.findall(r'((.+)-to-(.+)) map:$',i)
        mapping_re = re.findall(r'(\d+) (\d+) (\d+)',i)
        if len(title_re) > 0:
            # carry through loop
            current_map_name = {
                'title': title_re[0][0],
                'source':  title_re[0][1],
                'destination':  title_re[0][2],
            }

            # seed initial parse record
            parsed_dict['initial'][current_map_name['title']] = {
                'source': current_map_name['source'],
                'destination': current_map_name['destination'],
                'mapping':[]
            }

            # seed directed graph
            if current_map_name['source'] not in parsed_dict['directed'].keys():
                parsed_dict['directed'][current_map_name['source']] = {current_map_name['destination']:[],'next_step': current_map_name['destination']}

        elif len(mapping_re) > 0:
            parsed_dict['directed'][current_map_name['source']][current_map_name['destination']].append([
                int(mapping_re[0][0]),int(mapping_re[0][1]),int(mapping_re[0][2]),current_map_name['source'],current_map_name['destination']
            ])
            parsed_dict['initial'][current_map_name['title']]['mapping'].append([
                int(mapping_re[0][0]),int(mapping_re[0][1]),int(mapping_re[0][2])
            ])

    return parsed_dict

@cache
def map_to_val(source_string,dest_string,val):
    global parsed_dict
    if source_string in parsed_dict['directed'] and dest_string in parsed_dict['directed'][source_string]:
        for i in parsed_dict['directed'][source_string][dest_string]:
            tval = translate_source_val(
                val,
                i[0],
                i[1],
                i[2]
            )
            if val != tval:
                return tval
        return val
    else:
        raise('bad source/dest pair for val: ',source_string,dest_string,val)

@cache
def translate_source_val(val,dest_range_start,source_range_start,range_len):
    #print("\t\ttranslate_source_val",val,dest_range_start,source_range_start,range_len)
    if val < (source_range_start + range_len) and val >= source_range_start:
        return val + (dest_range_start - source_range_start)
    else:
        return val

def puzzle_text():
    print("""--- Day N: X ---

""")



class testCase(unittest.TestCase):
    global DEBUG
    DEBUG = True

    test_set = (
        """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
    )

    def test_one_star_a(self):
        self.assertEqual(
            one_star(
                self.__class__.test_set
            )[0],
            {
                79:81,
                14:14,
                55:57,
                13:13
            }
        )

    def test_one_star(self):
        self.assertEqual(
            one_star(
                self.__class__.test_set
            )[1],
            35
        )

    def test_two_star(self):
        self.assertEqual(
            two_star(
                self.__class__.test_set
            )[1],
            46
        )



if __name__ == '__main__':
    try:
        sys.argv[1]
        puzzle_text()

    except:
        DEBUG = False

        username = 'crushing'
        m = hashlib.sha256()
        hostname = socket.gethostname()
        m.update(hostname.encode('utf8'))
        if m.hexdigest() == 'ec7c98e2b47378ec88e1f9cce8d6ed91b9d616787c8a37023fd5c67cef1ff71f':
            username = 'conrad.rushing'
        print ('hostname str :',hostname)
        print ('hostname hash:', m.hexdigest())

        filename_script = os.path.basename(__file__)
        print("---------------%s--------------------"%filename_script)
        filename = filename_script.split('.')[0]
        input_set = ()

        with open("/Users/%s/Development/crushallhumans/adventofcode2023/inputs/2023/%s.txt" % (username,filename)) as input_file:
            input_set = [input_line.strip() for input_line in input_file]
        ret = one_star(input_set)
        print (ret)

        ret = two_star(input_set)
        print (ret)
