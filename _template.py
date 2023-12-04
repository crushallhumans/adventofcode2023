# adventofcode 2023
# crushallhumans
# puzzle N
# 12/n/2023

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
pp = pprint.PrettyPrinter()

DEBUG = False

def one_star(param_set, is_two_star = False):
    print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    c = 8888
    for i in param_set:
        continue
    return c


def two_star(param_set):
    print("---------------two_star--------------------")
    param_set = reprocess_input(param_set)
    c = 7777
    for i in param_set:
        continue
    return c

def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    return param_set    


def puzzle_text():
    print("""--- Day N: X ---

""")



class testCase(unittest.TestCase):
    global DEBUG
    DEBUG = True

    test_set = (
        """
"""
    )

    def test_one_star(self):
        self.assertEqual(
            one_star(
                self.__class__.test_set
            ),
            8888
        )

    def test_two_star(self):
        self.assertEqual(
            two_star(
                self.__class__.test_set
            ),
            7777
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