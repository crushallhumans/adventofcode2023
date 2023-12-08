# adventofcode 2023
# crushallhumans
# puzzle 8
# 12/8/2023

import os
import re
import sys
import math
import unittest
import socket
import hashlib
import pprint
import random
import time
from functools import reduce
from functools import cache
from itertools import chain
from multiprocessing import Pool
pp = pprint.PrettyPrinter()

DEBUG = False

def one_star(param_set, is_two_star = False):
    print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0
    if DEBUG: pp.pprint(param_set)
    node = 'AAA'
    turn_counter = 0
    while c < 100000000:
        step = param_set['connections'][node]
        node = step[param_set['turn_routine'][turn_counter]]
        if DEBUG: print(node,step)
        turn_counter += 1
        if turn_counter >= param_set['routine_len']:
            turn_counter = 0
        c += 1
        if node == 'ZZZ':
            break
    return c


def two_star(param_set):
    print("---------------two_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0
    search_op = param_set['starting_a']
    if DEBUG: pp.pprint(param_set)

    paths = []
    for start in search_op:
        path = 0
        turn_counter = 0
        while start[2] != 'Z':
            step = param_set['connections'][start]
            start = step[param_set['turn_routine'][turn_counter]]
            turn_counter += 1
            if turn_counter >= param_set['routine_len']:
                turn_counter = 0
            path += 1
        paths.append(path)

    c = math.lcm(*paths)
    #bruteforce - holy shit that didn't work, 30m = 2.5B rounds, 10^13 rounds estimate for complete
    # while True:
    #     search_op_current = search_op.copy()
    #     search_op = []
    #     all_z = True
    #     for node in search_op_current:
    #         step = param_set['connections'][node]
    #         node = step[param_set['turn_routine'][turn_counter]]
    #         search_op.append(node)
    #         if list(node).pop() != 'Z':
    #             all_z = False
    #         if DEBUG: print(search_op)
    #     turn_counter += 1
    #     if turn_counter >= param_set['routine_len']:
    #         turn_counter = 0
    #     c += 1
    #     if not c % 10000000:
    #         print(c)
    #     if all_z:
    #         break

    return c

def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    param_dict = {}
    param_dict['turn_routine_str'] = param_set[0]
    param_dict['turn_routine'] = list(map(lambda x:0 if x == 'L' else 1,list(param_dict['turn_routine_str'])))
    param_dict['routine_len'] = len(param_dict['turn_routine'])
    param_dict['connections'] = {}
    param_dict['starting_a'] = []
    
    for i in param_set[2:]:
        inst = i.split(' = ')
        param_dict['connections'][inst[0]] = []
        for j in inst[1][1:][:-1].split(', '):
            param_dict['connections'][inst[0]].append(j)
        if list(inst[0]).pop() == 'A':
            param_dict['starting_a'].append(inst[0])
    return param_dict


def puzzle_text():
    print("""--- Day N: X ---

""")



class testCase(unittest.TestCase):
    global DEBUG
    DEBUG = True

    test_set = (
        """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""",
        """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""",
        """LR

11A = (11B, YYY)
11B = (YYY, 11Z)
11Z = (11B, YYY)
22A = (22B, YYY)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
YYY = (YYY, YYY)"""
    )

    def test_one_star(self):
        self.assertEqual(
            one_star(
                self.__class__.test_set[0]
            ),
            2
        )
        self.assertEqual(
            one_star(
                self.__class__.test_set[1]
            ),
            6
        )

    def test_two_star(self):
        self.assertEqual(
            two_star(
                self.__class__.test_set[2]
            ),
            6
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

        start = (time.time() * 1000)
        ret = one_star(input_set)
        print (ret)
        print ('elapsed:',(time.time() * 1000) - start,'ms')

        start = (time.time() * 1000)
        ret = two_star(input_set)
        print (ret)
        print ('elapsed:',(time.time() * 1000) - start,'ms')
