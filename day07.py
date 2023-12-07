# adventofcode 2023
# crushallhumans
# puzzle 7
# 12/7/2023

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
from operator import itemgetter,ior
from functools import reduce
from functools import cache
from itertools import chain
from multiprocessing import Pool
pp = pprint.PrettyPrinter()

DEBUG = False

CARD_LABELS = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
# numeric value is cards[] idx + 2

def one_star(param_set, is_two_star = False, wild_cards = []):
    if is_two_star:
        print("---------------two_star--------------------")
    else:
        print("---------------one_star--------------------")
    param_set = reprocess_input(param_set, wild_cards=wild_cards)
    c = 0
    hands_sorted = sorted(
        param_set['hands'], 
        key=itemgetter('strength','binary_strength')
    )
    d = 1
    for i in hands_sorted:
        bidval = i['bid'] * d
        c += bidval
        if DEBUG: print(i,bidval,c,d)
        d += 1
    return c

def two_star(param_set):
    return one_star(param_set, True, ['J'])

def reprocess_input(param_set, wild_cards = []):
    if isinstance(param_set,str):
        l = []
        l = [input_line.strip() for input_line in param_set.splitlines()]
        param_set = l

    # wilds are the lowest value, reassemble list
    if len(wild_cards):
        for i in wild_cards:
            if CARD_LABELS.index(i):
                c = CARD_LABELS.pop(CARD_LABELS.index(i))
                CARD_LABELS.insert(0,c)

    card_dict = {
        'original_input_array':param_set,
        'hands':[]
    }
    for i in param_set:
        cards = list(i.split(' ')[0])
        bid = i.split()[1]
        cards_numeric = list(map(lambda x: CARD_LABELS.index(x) + 2, cards))
        cards_sorted_numeric = sorted(cards_numeric,reverse=True)

        hand = {
            'cards':cards.copy(),
            'cards_numeric':cards_numeric.copy(),
            'cards_sorted_numeric':cards_sorted_numeric.copy(),
            'cards_sorted_handwise':[],
            'cards_sorted_bitfield':[],
            'card_sums':{},
            'card_multiples':{},
            'strength':0,
            'binary_strength':0,
            'strength_name':'',
            'total_card_value':0,
            'bid':int(bid),
            'highest':('',0)
        }

        for j in cards:
            if j not in hand['card_sums']:
                hand['card_sums'][j] = 0
            hand['card_sums'][j] += 1

            # what should we add the wildcard sum to?
            if (
                j != 'J' and
                (
                    hand['card_sums'][j] > hand['highest'][1]
                    or
                    hand['card_sums'][j] == hand['highest'][1] and
                    CARD_LABELS.index(j) + 2 > CARD_LABELS.index(hand['highest'][0]) + 2
                )
            ):
                hand['highest'] = (j,hand['card_sums'][j])

        # handle wilds
        for wc in wild_cards:
            if wc in hand['card_sums']:
                # handle 5 wilds
                if hand['card_sums'][wc] == 5:
                    hand['card_sums']['A'] = 5
                else:
                    hand['card_sums'][hand['highest'][0]] += hand['card_sums'][wc]
                del hand['card_sums'][wc]

        #not actually doing a handwise sort - comparison in AoC instructions is L-to-R dumb
        #def handwise_sort(x):
        #    return hand['card_sums'][x], CARD_LABELS.index(x) + 2
        #hand['cards_sorted_handwise'] = list(map(lambda x: CARD_LABELS.index(x) + 2, sorted(cards,key=handwise_sort, reverse = True)))
        # for j in hand['cards_sorted_handwise']
        
        # understanding cribbed from here: 
        #   https://jonathanhsiao.com/blog/evaluating-poker-hands-with-bit-math
        bb = 16
        for j in hand['cards_numeric']:
            hand['cards_sorted_bitfield'].append(j << bb)
            bb -= 4
        hand['binary_strength'] = reduce(ior, hand['cards_sorted_bitfield'])

        # tried to do binary math here, but was conceptually incorrect
        #     hand['card_multiples'][j] *=  CARD_LABELS.index(j) + 2
        # for j in hand['card_multiples']:
        #     hand['card_multiples'][j] *= hand['card_sums'][j]
        # print(hand['card_multiples'])
        # hand['total_card_value'] = sum(hand['card_multiples'].values())

        #five of a kind 7
        if len(hand['card_sums'].keys()) == 1:
            hand['strength'] = 7
            hand['strength_name'] = 'five of a kind'

        #four of a kind 6
        elif 4 in hand['card_sums'].values():
            hand['strength'] = 6
            hand['strength_name'] = 'four of a kind'

        #full house 5
        elif sorted(hand['card_sums'].values()) == [2,3]:
            hand['strength'] = 5
            hand['strength_name'] = 'full boat'

        #three of a kind 4
        elif 3 in hand['card_sums'].values():
            hand['strength'] = 4
            hand['strength_name'] = 'three of a kind'

        #two pair 3
        elif sorted(hand['card_sums'].values()) == [1,2,2]:
            hand['strength'] = 3
            hand['strength_name'] = 'two pair'

        #one pair 2
        elif 2 in hand['card_sums'].values():
            hand['strength'] = 2
            hand['strength_name'] = 'one pair'

        #else high card 1
        else:
            hand['strength'] = 1
            hand['strength_name'] = 'high card'

        card_dict['hands'].append(hand.copy())

    return card_dict


def puzzle_text():
    print("""--- Day 7: Camel Cards ---
Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?

--- Part Two ---
To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
KK677 is now the only two pair, making it the second-weakest hand.
T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.
With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
""")



class testCase(unittest.TestCase):
    global DEBUG
    DEBUG = True

    test_set = (
        """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    )

    def test_one_star(self):
        self.assertEqual(
            one_star(
                self.__class__.test_set
            ),
            6440
        )

    def test_two_star(self):
        self.assertEqual(
            two_star(
                self.__class__.test_set
            ),
            5905
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
