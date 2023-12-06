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
from itertools import chain
from multiprocessing import Pool

pp = pprint.PrettyPrinter(indent=1, width=120)

DEBUG = False

# trying out the range-based solution from @xavdid does Advent of Code:
# https://advent-of-code.xavd.id/writeups/2023/day/5/
# I'm retyping their solution, basically, as a way
# to let my fingers as well as my brain understand how it works.

Transformation  = tuple[range, int]
def parse_range(line: str) -> Transformation:
    dest_start, source_start, size = map(int, line.split())

    # convert dest|source|size into 
    #   range(source..source+size) object
    #   and operating offset (dest - source)
    return range(source_start, source_start+size), dest_start - source_start

def parse_map(map_block: str) -> list[Transformation]:
    if DEBUG: print(map_block.split("\n")[0])
    return sorted(
        [
            # first line of the block is the name, skip it w [1:] list slicing
            parse_range(l) for l in map_block.split("\n")[1:]
        ],
        key = lambda r: r[0].start
    )

def mask_number(number: int, transformations: list[Transformation]) -> int:
    for mask, offset in transformations:
        if number in mask:
            return number + offset
    return number

def one_star(input_list: list) -> int:
    blocks = input_list.split("\n\n")
    # first line is the integer seeds, space-separated after 7 chars of 'seeds: '
    seeds = [int(s) for s in blocks[0][6:].split()]

    # input is split into whole map blocks by the \n\n split
    #   first block is the seeds, skip it with [1:] list slicing
    map_layers = [parse_map(b) for b in blocks[1:]]

    result = []
    for seed in seeds:
        transformed_seed = seed
        for transformation in map_layers:
            transformed_seed = mask_number(transformed_seed,transformation)
        result.append(transformed_seed)
    
    return min(result)

def do_ranges_overlap(a: range, b: range) -> bool:
    return (a == b) or (a.start < b.stop and b.start < a.stop)

def shift_range(r: range, offset: int) -> range:
    return range(r.start+offset, r.stop+offset)

#explanation that made sense to me:
"""
Given a range and a list of transforms, 
return a new list of ranges where 
the appropriate section(s) have been shifted. 
We'll do that by applying each mask in order, if possible. 
It's also important (for this approach) that all ranges are *sorted*. 
This is because when we make cuts to the base range, we'll be assuming 
that anything lower than our current range doesn't need to be masked 
if it hasn't been already.

Broadly, there are 5 cases to cover:

1 - No overlap:
base:    12345
mask:         6789
result:  12345

2 - Mask whole range:
base:      345
mask:    1234567
result:    MMM

3 - Mask center portion of range:
base:    1234567
mask:      345
result:  12MMM??

4 - Mask left:
base:      34567
mask:    12345
result:    MMM??

5 - Mask right:
base:    12345
mask:      34567
result:  12MMM

The question marks above are why the sorted transforms are so important. 
In cases 3 and 4, we know that everything before (lower than) the current mask 
is settled, (because they've been processed in order)
but a subsequent (higher) mask could still apply. 
So we can't know what the rest of result will look like yet. 
We'll have to recurse a little.
"""

def apply_transformations(base: range, transformations: list[Transformation]) -> list[range]:
    for mask, offset in transformations:
        # 1 - no overlap, skip
        if not do_ranges_overlap(base, mask):
            continue

        # 2 - base entirely enclosed, shift all
        if mask.start <= base.start and base.stop <= mask.stop:
            return [shift_range(base, offset)]

        # 3 - mask is subset of base
        #       return unshifted left, shifted middle, and recurse for rest on right
        if base.start <= mask.start and mask.stop <= base.stop:
            return [
                range(base.start, mask.start),
                shift_range(mask, offset),
                *apply_transformations(range(mask.stop, base.stop), transformations)
            ]

        # 4 - mask overlaps only left side
        #       return shifted left, recurse for rest on right
        if mask.start <= base.start and mask.stop <= base.stop:
            return [
                shift_range(range(base.start, mask.stop), offset),
                *apply_transformations(range(mask.stop, base.stop), transformations)
            ]

        # 5 - mask overlaps only right side
        #       return unshifted left, shifted right
        if base.start <= mask.start and base.stop <= mask.stop:
            return [
                range(base.start, mask.start),
                shift_range(range(mask.start, base.stop), offset)
            ]

    # nothing has acted, pass base back
    return [base]

def two_star(input_list:list) -> int:
    blocks = input_list.split("\n\n")
    # first line is the integer seed pairs, space-separated after 7 chars of 'seeds: '
    #   can't use the elegant new Python 3.12 'batched' itertool :(
        # seeds = [
        #     range(start, start + size)
        #     for start, size in batched(map(int, blocks[0][6:].split()), 2)
        # ]        
    seed_pairs = blocks[0][6:].split()
    seeds = []
    while len(seed_pairs) >= 2:
        seed_start = int(seed_pairs.pop(0))
        seed_size = int(seed_pairs.pop(0))
        seeds.append(range(seed_start, seed_start + seed_size))
    if DEBUG: print(seeds)

    transformations = [parse_map(b) for b in blocks[1:]]
    
    result = []
    for seed_range in seeds:
        ranges = [seed_range]

        for map_block in transformations:
            ranges = list(
                chain.from_iterable(
                    apply_transformations(r, map_block)
                    for r in ranges
                )
            )
        # we only need the lowest result from each result group, 
        #   so after sorted do a [0].start suffix
        result.append(sorted(ranges, key = lambda r: r.start)[0].start)
        result = sorted(result)
        # the lowest result in my input was 0, which is not the right answer
        #   the next lowest result was. curious!
        if result[0] == 0: result.pop(0)
        if DEBUG: print(result)
    return min(result)







#crushing original solution
parsed_dict = {}
def crushing_one_star(param_set, is_two_star = False):
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


def crushing_two_star(param_set):
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
    print("""--- Day 5: If You Give A Seed A Fertilizer ---
You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

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
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?


--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
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
56 93 4"""
    )

    # def test_one_star_a(self):
    #     self.assertEqual(
    #         one_star(
    #             self.__class__.test_set
    #         )[0],
    #         {
    #             79:81,
    #             14:14,
    #             55:57,
    #             13:13
    #         }
    #     )

    def test_one_star(self):
        self.assertEqual(
            one_star(
                self.__class__.test_set
            ),
            35
        )

    def test_two_star(self):
        self.assertEqual(
            two_star(
                self.__class__.test_set
            ),
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

        file = open("/Users/%s/Development/crushallhumans/adventofcode2023/inputs/2023/%s.txt" % (username,filename))
        input_str = file.read()
        file.close()

        ret = one_star(input_str)
        print (ret)

        ret = two_star(input_str)
        print (ret)
