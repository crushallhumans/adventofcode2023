# adventofcode 2023
# crushallhumans
# puzzle 1
# 12/1/2023

import os
import re
import sys
import math
import unittest

DEBUG = True

def one_star(param_set):
    print("---------------one_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0
    digit_re = re.compile(r"\d")
    for i in param_set:
        n = ''
        for j in i:
            if re.match(digit_re,j):
                n = j
                break
        for j in i[::-1]:
            if re.match(digit_re,j):
                n = n + '' + j
                break
        c += int(n)
    return c

def find_digit_words(i,digit_word_re_list,reverse = False):
    word_index = ['',-1]
    for j in digit_word_re_list:
        s_list = re.finditer(j,i)
        for s in s_list:
            word = s.group()
            idx = s.start()
            reverse_idx = (len(i) - 1) - idx
            if DEBUG: print(word,idx,reverse_idx)
            replace_index = False
            if reverse:
                idx = reverse_idx

            if idx < word_index[1] or word_index[1] == -1:
                replace_index = True
                
            if replace_index:
                word_index = [word,idx]
    return word_index

def number_digit_comparator(number_set,digit_word_set,digit_word_list):
    is_digit_word = False
    if number_set == [] and digit_word_set == ['',-1]:
        raise "Bad comparator: empty sets"
    elif number_set == []:
        is_digit_word = True
    elif digit_word_set == ['',-1]:
        is_digit_word = False 
    else:
        if DEBUG: print('comparing: ',int(number_set[1]),digit_word_set[1])
        if int(number_set[1]) < digit_word_set[1]:
            is_digit_word = False 
        else:
            is_digit_word = True
        
    if is_digit_word:
        if DEBUG: print('digit_word_set[0]',digit_word_set[0])
        return digit_word_list.index(digit_word_set[0])
    else:
        if DEBUG: print('number_set[0]',number_set[0])
        return int(number_set[0])


def two_star(param_set):
    print("---------------two_star--------------------")
    param_set = reprocess_input(param_set)
    c = 0
    digit_re = re.compile(r"\d")
    digit_word_list = [
        'zero',
        'one',
        'two',
        'three',
        'four',
        'five',
        'six',
        'seven',
        'eight',
        'nine',
    ]
    digit_word_re_list = []
    for i in digit_word_list:
        digit_word_re_list.append(
            re.compile(i)
        )
    for i in param_set:
        if DEBUG: print(i)
        n = ''
        first_number = []
        last_number = []
        first_digit_word = []
        last_digit_word = []
        d = 0
        if DEBUG: print('forward')
        for j in i:
            if re.match(digit_re,j):
                n = j
                first_number = [j,d]
                break
            d += 1
        if DEBUG: print('first_number',first_number)
        first_digit_word = find_digit_words(i,digit_word_re_list)
        if DEBUG: print('first_digit_word',first_digit_word)

        n = str(number_digit_comparator(first_number,first_digit_word,digit_word_list))
        if DEBUG: print('determined first n',n)

        if DEBUG: print('')
        if DEBUG: print('backward')
        d = 0
        for j in i[::-1]:
            if re.match(digit_re,j):
                last_number = [j,d]
                break
            d += 1
        if DEBUG: print('last_number',last_number)
        last_digit_word = find_digit_words(i,digit_word_re_list,True)
        if DEBUG: print('last_word_index',last_digit_word)

        n += '' + str(number_digit_comparator(last_number,last_digit_word,digit_word_list))
        if DEBUG: print('determined last n',n)

        if DEBUG: print(n)
        c += int(n)
        if DEBUG: print('-----------------------')
        if DEBUG: print('')
    return c

def reprocess_input(param_set):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l
    return param_set    


def puzzle_text():
    print("""
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?
""")



class testCase(unittest.TestCase):
    global DEBUG
    DEBUG = True

    test_set = (
"""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""",
"""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    )
    
    def test_one_star(self):
        self.assertEqual(
            one_star(
                self.__class__.test_set[0]
            ),
            142
        )

    def test_two_star(self):
        self.assertEqual(
            two_star(
                self.__class__.test_set[1]
            ),
            281
        )



if __name__ == '__main__':
    try:
        sys.argv[1]
        puzzle_text()

    except:
#        DEBUG = False
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
