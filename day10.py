# adventofcode 2023
# crushallhumans
# puzzle 10
# 12/10/2023

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
from shapely.geometry.polygon import Polygon as ShapelyPolygon
from functools import reduce
from functools import cache
from itertools import chain
from multiprocessing import Pool
pp = pprint.PrettyPrinter()

DEBUG = False


# copying this bad boy in from my 2021 solutions
class CartesianTheater():
    # max_x = -1
    # max_y = -1
    # points = {}
    # inited = False
    # max_steps = 0
    # rows = []
    # cols = []
    # start = (0,0)
    # pipe_dict = {}
    # cardinal_directions = []
    def __init__(self):
        self.max_x = 0
        self.max_y = 0
        self.points = {}
        self.rows = []
        self.cols = []
        self.max_steps = 0
        self.inited = False
        self.start = (0,0)
        self.shapely_polygon_points = []
        self.shapely_points = []
        self.shapely_polygon = ShapelyPolygon()
        self.points_in_polygon = 0
        self.pipe_dict = {
           #'x':[(dirN),(dirE),(dirS),(dirW)]
           #         5      6      7      8
            '|':[(0,-1),(0, 0),(0, 1),(0, 0)],
            '-':[(0, 0),(1, 0),(0, 0),(-1,0)],
            'L':[(0, 0),(0, 0),(1, 6),(5,-1)], # if W, now N; if S, now E
            'J':[(0, 0),(5,-1),(-1,8),(0, 0)], # if E, now N; if S, now W
            '7':[(-1,8),(7, 1),(0, 1),(0, 0)], # if E, now S; if N, now W
            'F':[(1, 6),(0, 0),(0, 0),(7, 1)], # if W, now S; if N, now E
        }
        self.cardinal_directions = [
            (0,-1), # N
            (1, 0), # E
            (0, 1), # S
            (-1,0), # W
        ]

    def __str__(self):
        return self.stringify()
    
    def stringify(self, show_steps = False, show_path_only = False, show_inner_points = False):
        if not self.inited:
            return "need at least one row or point"

        s = ''
        for i in range(0,self.max_y):
            for j in range(0,self.max_x):
                match = (j,i)
                if not match in self.points.keys():
                    s += '*'
                else:
                    if show_steps or show_path_only:
                        if self.points[match][0] == 'S':
                            s += 'S'
                        elif self.points[match][1] > 0:
                            # add termcolor set escape sequence here (calc from match[1] val along spectrum)
                            s += str(self.points[match][1] if not show_path_only else self.points[match][0])
                            # add termcolor reset escape sequence here
                        elif self.points[match][1] == -1:
                            s += "\x1b[48;2;255;0;0m$\x1b[0m"
                        else:
                            s += '.'
                    else:
                        s += str(self.points[match][0])
            s += "\n"
        if show_steps: s += "(steps shown)\n"
        s += "\n"

        return s

    def add_row(self,i):
        self.rows.append(list(i))
        if not self.max_x:
            self.max_x = len(list(i))
        self.max_y += 1
        self.inited = True

    def build_cols(self):
        for i in range(0,self.max_x):
            col = []
            for j in self.rows:
                col.append(j[i])
            self.cols.append(col.copy())

    def build_points(self):
        c = 0
        for i in self.cols:
            d = 0
            for j in i:
                self.points[(c,d)] = [j,0]
                self.shapely_points.append(ShapelyPoint(c,d))
                if j == 'S':
                    self.points[(c,d)] = [j,1]
                    self.start = (c,d)
                d += 1
            c += 1

    def add_coords(self,a,b):
        return tuple(map(sum,zip(a,b)))

    def find_steps(self, find_points = False):
        # from start
        # find any pipes connected in neighborhood
        if DEBUG: print(self.start)
        initial_pipes = []

        shapely_polygon_points = [self.start]
        for dir,i in enumerate(self.cardinal_directions):
            c = self.add_coords(self.start,i)
            if (
                c in self.points.keys() # point exists
                and self.points[c][0] in self.pipe_dict.keys() # point is a pipe
                and self.pipe_dict[self.points[c][0]][dir] != (0,0) # pipe connects in point direction from start
            ):
                if DEBUG: print('dir: ',dir,c)
                if DEBUG: print('point: ',self.points[c][0])
                if DEBUG: print('pipe: ',self.pipe_dict[self.points[c][0]])
                if DEBUG: print('pipe@dir: ',self.pipe_dict[self.points[c][0]][dir])
                initial_pipes.append((c,dir))
        if DEBUG: print(initial_pipes)

        for i in initial_pipes:
            dir = i[1]
            coords = i[0]
            step_counter = 1 #pathing begins 1 step away from Start
    
            # follow path, setting steps along the way
            # stop when cursor == start
            c = 1000000000000000000
            if DEBUG: print('return to ',self.start)
            while coords != self.start and c > -1:
                if coords not in shapely_polygon_points:
                    shapely_polygon_points.append(coords)
                if DEBUG: print("\tcoords & dir",coords,dir)
                if not self.points[coords][1] or step_counter < self.points[coords][1]:
                    self.points[coords][1] = step_counter
                pipe_instructions = self.pipe_dict[self.points[coords][0]]
                x = pipe_instructions[dir][0]
                y = pipe_instructions[dir][1]
                if x > 4: # change direction
                    if DEBUG: print("\t\tchange dir: ",dir,' -> ',x - 5)
                    dir = x - 5
                    x = 0
                elif y > 4:
                    if DEBUG: print("\t\tchange dir: ",dir,' -> ',y - 5)
                    dir = y - 5
                    y = 0
                #if DEBUG: print("\t",pipe_instructions[dir],(x,y))
                coords = self.add_coords(coords,(x,y))
                c -= 1
                step_counter += 1

        for i in self.points.keys():
            if self.points[i][1] > self.max_steps:
                self.max_steps = self.points[i][1]

        if find_points:
            if DEBUG: print('shapely_polygon_points',shapely_polygon_points)
            self.shapely_polygon = ShapelyPolygon(shapely_polygon_points)
            self.points_in_polygon = 0
            for i in self.points.keys():
                if self.points[i][1] == 0:
                    if self.shapely_polygon.contains(ShapelyPoint(i)):
                        self.points[i][1] = -1
                        self.points_in_polygon += 1
            print(self.stringify(False,True,True))
        else:
            print(self.stringify(False,True))
        


def one_star(param_set, is_two_star = False):
    print("---------------one_star--------------------")
    ct = reprocess_input(param_set)
    ct.find_steps()
    return ct.max_steps


def two_star(param_set):
    print("---------------two_star--------------------")
    ct = reprocess_input(param_set)
    ct.find_steps(find_points = True)
    return ct.points_in_polygon

def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    c = CartesianTheater()
    for i in param_set:
        c.add_row(i)
    c.build_cols()
    c.build_points()
    return c


def puzzle_text():
    print("""--- Day 10: Pipe Maze ---
You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....
If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....
In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF
In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....
You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....
In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...
Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?


--- Part Two ---
You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....
In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO
In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?
""")



class testCase(unittest.TestCase):
    global DEBUG
    DEBUG = True

    test_set = (
        [""".....
.S-7.
.|.|.
.L-J.
.....""",4],
["""7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ""",8],
["""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""",4],
[""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""",8],
["""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""",10]
    )

    def test_one_star(self):
        self.assertEqual(
            one_star(
                self.__class__.test_set[0][0]
            ),
            self.__class__.test_set[0][1]
        )
    def test_one_star_complex(self):
        self.assertEqual(
            one_star(
                self.__class__.test_set[1][0]
            ),
            self.__class__.test_set[1][1]
        )

    def test_two_star_a(self):
        self.assertEqual(
            two_star(
                self.__class__.test_set[2][0]
            ),
            self.__class__.test_set[2][1]
        )
    def test_two_star_b(self):
        self.assertEqual(
            two_star(
                self.__class__.test_set[3][0]
            ),
            self.__class__.test_set[3][1]
        )
    def test_two_star_c(self):
        self.assertEqual(
            two_star(
                self.__class__.test_set[4][0]
            ),
            self.__class__.test_set[4][1]
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