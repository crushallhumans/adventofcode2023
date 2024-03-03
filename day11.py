# adventofcode 2023
# crushallhumans
# puzzle 11
# 12/11/2023

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
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import LineString as ShapelyLineString
from shapely.geometry.polygon import Polygon as ShapelyPolygon
from functools import reduce
from functools import cache
from itertools import chain
from multiprocessing import Pool
pp = pprint.PrettyPrinter()

DEBUG = False

class CartesianTheater():
    def __init__(self, expansion_rate = 2):
        self.max_x = 0
        self.max_y = 0
        self.points = {}
        self.rows = []
        self.cols = []
        self.empty_rows = []
        self.empty_cols = []
        self.max_steps = 0
        self.inited = False
        self.start = (0,0)
        self.shapely_points = {}
        self.distances = {}
        self.cardinal_directions = [
            (0,-1), # N
            (1, 0), # E
            (0, 1), # S
            (-1,0), # W
        ]
        self.expansion_rate = expansion_rate

    def __str__(self):
        return self.stringify(show_galaxy_numbers=True)
    
    def stringify(self, show_paths = False, show_galaxy_numbers = False):
        if not self.inited:
            return "need at least one row or point"

        s = ''
        for i in range(0,self.max_y):
            for j in range(0,self.max_x):
                match = (j,i)
                if not match in self.points.keys():
                    s += '*'
                else:
                    n = self.points[match]
                    if show_galaxy_numbers and n[1]:
                        s += str(n[1])
                    else:
                        s += n[0]
            s += "\n"
        s += "\n"

        return s

    def add_row(self,i):
        self.rows.append(list(i))
        if not self.max_x:
            self.max_x = len(list(i))
        if self.expansion_rate < 100:
            if len(set(list(i))) == 1:
                for n in range(0,self.expansion_rate-1):
                    self.rows.append(list('.' * self.max_x))
                    self.max_y += 1
        self.max_y += 1
        self.inited = True

    def build_cols(self):
        operating_max_x = self.max_x 
        for i in range(0,operating_max_x):
            col = []
            for j in self.rows:
                col.append(j[i])
            self.cols.append(col.copy())
            if self.expansion_rate < 100:
                if len(set(col)) == 1:
                    for n in range(0,self.expansion_rate-1):
                        self.cols.append(col.copy())
                        self.max_x += 1
            
    def build_points(self):
        c = 0
        galaxy = 1
        for i in self.cols:
            d = 0
            for j in i:
                self.points[(c,d)] = [j,0]
                if j == '#':
                    self.points[(c,d)] = [j,str(galaxy)]
                    self.shapely_points[str(galaxy)] = ShapelyPoint(c,d)
                    galaxy += 1
                d += 1
            c += 1
        if self.expansion_rate > 100:
            for i in self.rows:



    def get_distances(self):
        for i in self.shapely_points.keys():
            for j in self.shapely_points.keys():
                pair = tuple(sorted([i,j]))
                if i != j and pair not in self.distances.keys():
                    ii = self.shapely_points[i]
                    jj = self.shapely_points[j]
                    self.distances[pair] = int(abs(ii.x - jj.x) + abs(ii.y - jj.y))
                    print(pair,ii,jj,self.distances[pair])
                    # self.distances[pair] = int(self.shapely_points[i].distance(self.shapely_points[j]))
                    # ii = self.shapely_points[i]
                    # jj = self.shapely_points[j]
                    # ln = ShapelyLineString([ii,jj])
                    # points_intersecting = 0
                    # for n in range(int(ii.x)-1,int(jj.x)+1):
                    #     for m in range(int(ii.y)-1,int(jj.y)+1):
                    #         print("\t\t",n,m)
                    #         sp = ShapelyPoint(n,m)
                    #         if sp.intersects(ln):
                    #             points_intersecting += 1
                    # print("\tpoints_intersecting: ", points_intersecting)

    def add_coords(self,a,b):
        return tuple(map(sum,zip(a,b)))




def one_star(param_set, is_two_star = False):
    print("---------------one_star--------------------")
    ct = reprocess_input(param_set, 2)
    ct.get_distances()
    return sum(ct.distances.values())


def two_star(param_set):
    print("---------------two_star--------------------")
    ct = reprocess_input(param_set,1000000)
    ct.get_distances()
    return sum(ct.distances.values())

def reprocess_input(param_set, expansion_rate = 2):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    c = CartesianTheater(expansion_rate = expansion_rate)
    for i in param_set:
        c.add_row(i)
    c.build_cols()
    c.build_points()
    print(c)
    return c


def puzzle_text():
    print("""
""")



class testCase(unittest.TestCase):
    global DEBUG
    DEBUG = True

    test_set = (
        ["""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""",374],
    )

    def test_one_star(self):
        self.assertEqual(
            one_star(
                self.__class__.test_set[0][0]
            ),
            self.__class__.test_set[0][1]
        )

    def test_two_star(self):
        self.assertEqual(
            two_star(
                self.__class__.test_set[0][0]
            ),
            self.__class__.test_set[0][1]
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



# truecolor - try to draw the path in 24bit color in terminal
"""
#!/bin/bash
# This file was originally taken from iterm2 https://github.com/gnachman/iTerm2/blob/master/tests/24-bit-color.sh
#
#   This file echoes a bunch of 24-bit color codes
#   to the terminal to demonstrate its functionality.
#   The foreground escape sequence is ^[38;2;<r>;<g>;<b>m
#   The background escape sequence is ^[48;2;<r>;<g>;<b>m
#   <r> <g> <b> range from 0 to 255 inclusive.
#   The escape sequence ^[0m returns output to default

setBackgroundColor()
{
    #printf '\x1bPtmux;\x1b\x1b[48;2;%s;%s;%sm' $1 $2 $3
    printf '\x1b[48;2;%s;%s;%sm' $1 $2 $3
}

resetOutput()
{
    echo -en "\x1b[0m\n"
}

# Gives a color $1/255 % along HSV
# Who knows what happens when $1 is outside 0-255
# Echoes "$red $green $blue" where
# $red $green and $blue are integers
# ranging between 0 and 255 inclusive
rainbowColor()
{ 
    let h=$1/43
    let f=$1-43*$h
    let t=$f*255/43
    let q=255-t

    if [ $h -eq 0 ]
    then
        echo "255 $t 0"
    elif [ $h -eq 1 ]
    then
        echo "$q 255 0"
    elif [ $h -eq 2 ]
    then
        echo "0 255 $t"
    elif [ $h -eq 3 ]
    then
        echo "0 $q 255"
    elif [ $h -eq 4 ]
    then
        echo "$t 0 255"
    elif [ $h -eq 5 ]
    then
        echo "255 0 $q"
    else
        # execution should never reach here
        echo "0 0 0"
    fi
}

for i in `seq 0 127`; do
    setBackgroundColor $i 0 0
    echo -en " "
done
resetOutput
for i in `seq 255 -1 128`; do
    setBackgroundColor $i 0 0
    echo -en " "
done
resetOutput

for i in `seq 0 127`; do
    setBackgroundColor 0 $i 0
    echo -n " "
done
resetOutput
for i in `seq 255 -1 128`; do
    setBackgroundColor 0 $i 0
    echo -n " "
done
resetOutput

for i in `seq 0 127`; do
    setBackgroundColor 0 0 $i
    echo -n " "
done
resetOutput
for i in `seq 255 -1 128`; do
    setBackgroundColor 0 0 $i
    echo -n " "
done
resetOutput

for i in `seq 0 127`; do
    setBackgroundColor `rainbowColor $i`
    echo -n " "
done
resetOutput
for i in `seq 255 -1 128`; do
    setBackgroundColor `rainbowColor $i`
    echo -n " "
done
resetOutput
"""