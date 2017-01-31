#!/usr/bin/python3

import sys
from random import sample
import argparse

from sorts import *
from display import Display

def main(args):

    display = Display(args.wait)
    size = args.size

    if args.data == "reverse":
        array = list(reversed(range(1, size + 1)))
    elif args.data == "almost":
        array = list(range(1, size + 1))
        i, j = sample(range(size), 2) # select two distinct random indexes two switch
        array[i], array[j] = array[j], array[i] # switch the two numbers
    elif args.data == "random":
        array = list(range(1, size + 1))
        shuffle(array)
    #TODO: Add semi-ordered
    else:
        print(args.data, "is not a valid option for --data. Check sort.py -h for help")
        sys.exit()

    # check if requested sort is available
    if not args.algorithm in sorts:
        print(args.algorithm, "is not a valid sort. The options are:", ", ".join(sorts.keys()))
        sys.exit()
    else:
        sort = args.algorithm

    # fetch function for sort algorithm
    sort = sorts[sort]

    # first show unsorted array before starting
    display.print(array, tuple())

    sort(array, display)

    # do the cool animation at the end
    display.draw_completed_array(array)

    return


# there must be a better way!
sorts = {"bubble": bubble,
         "cocktail": cocktail,
         "selection": selection,
         "insertion": insertion,
         "merge": merge,
         "heap": heap,
         "quick": quick,
         "shell": shell,
         "bogo": bogo,
         "comb": comb}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visualisation of sorting algorithms built with Python and pygame")

    parser.add_argument("algorithm", type=str, default="bubble", nargs="?",
        help="algorithm to use when sorting array ({})".format(", ".join(sorts.keys())))

    parser.add_argument("--wait", type=int,
        help="time to wait (in milliseconds) between each step of the sort.")

    parser.add_argument("--data", type=str, default="random",
        help="type of input data (random, reverse, almost)")

    parser.add_argument("--size", type=int, default=100,
        help="size of to-be-sorted array")

    args = parser.parse_args()
    main(args)
