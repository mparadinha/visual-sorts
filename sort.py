import sys
from random import randint, shuffle, sample
import argparse

import pygame
from pygame.locals import *

def main(args):
    wait_time = args.wait

    screen = pygame.display.set_mode((700, 500 + 2))
    clock = pygame.time.Clock()
    size = args.size

    if args.data == "reverse":
        array = list(reversed(range(1, size + 1)))
    elif args.data == "almost":
        array = list(range(1, size + 1))
        i, j = sample(array, 2) # select two distinct random indexes two switch
        array[i], array[j] = array[j], array[i] # switch the two numbers
    elif args.data == "random":
        array = list(range(1, size + 1))
        shuffle(array)
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
    show_array(screen, array, tuple())

    for tested in sort(array):
        screen.fill((0, 0, 0))
        show_array(screen, array, tested)

        # check if window was closed
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYUP and event.key == K_q:
                pygame.quit()
                return

        # wait before drawing the next iteration
        if wait_time: pygame.time.wait(wait_time)

    # do the cool animation at the end
    draw_completed_array(screen, array)
    
    # wait for key press before closing
    while True:
        for event in pygame.event.get():
            if event.type in [QUIT, KEYUP]:
                pygame.quit()
                return

def show_array(screen, array, highlights):
    bar_size = (700 / len(array)) / 1.4
    space = 0.4 * bar_size

    x = space // 2
    for i, val in enumerate(array):
        y = round((500 * val) / len(array))

        # green bars for current bars. white for all others
        color = (0, 255, 0) if i in highlights else (255, 255, 255)

        pygame.draw.rect(screen, color, pygame.Rect(round(x), 501 - y, round(bar_size), y))
        x += bar_size + space

    pygame.display.update()
 
def draw_completed_array(screen, array):
    bar_size = (700 / len(array)) / 1.4
    space = 0.4 * bar_size

    # we have 500 ms for the whole array
    wait_time = 500 // len(array)

    # this is just because the switching looks ugly otherwise
    # because the last switched indexes are still green
    show_array(screen, array, ())

    x = space // 2 
    for i, val in enumerate(array):
        y = round((500 * val) / len(array))

        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(round(x), 501 - y, round(bar_size), y))
        x += bar_size + space
        
        pygame.time.wait(wait_time)
        pygame.display.update()

def bubble(array):
    rounds = len(array)
    switched = True
    last = rounds - 1 # last switched index

    while switched and rounds > 0:
        switched = False

        for i in range(rounds - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                switched = True
                last = i + 1
            yield (i, i + 1)

        rounds = last

def cocktail(array):
    """kinda like bubble sort only it works both ways"""
    start, end = 0, len(array) - 1
    switched = True

    while switched and start < end:
        switched = False
        first, last = start, end

        # go forwards
        switched = False
        for i in range(start, end):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                last = i + 1
                switched = True
            yield (i, i + 1)
        end = last
        if not switched: break # no switches, list is ordered

        # go backwards
        switched = False
        for i in reversed(range(start, end)):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                first = i
                switched = True
            yield (i, i + 1)
        start = first

def selection(array):

    n = len(array)
    for j in range(n - 1):

        # find the smallest item after index j
        imin = j
        for i in range(j + 1, n):
            if array[i] < array[imin]: imin = i
            yield (j, i, imin)

        if imin != j:
            array[j], array[imin] = array[imin], array[j]
            yield (j, imin)

def insertion(array):

    n = len(array)
    for i in range(1, n):
        if array[i] > array[i - 1]: continue

        for j in range(0, i):
            yield (j, i)
            if array[i] < array[j]:
                array.insert(j, array.pop(i))
                break
        yield (j,)

def fix_down(array, idx, end):
    while 2 * idx < end - 1:
        child = 2 * idx + 1
        
        if child < end - 1 and array[child] < array[child + 1]: child += 1
        if array[idx] < array[child]:
            array[idx], array[child] = array[child], array[idx]
        
        idx = child
        
    return array

def heap(array):
    start = (len(array) - 2) // 2
    
    while start >= 0:
        array = fix_down(array, start, len(array) - 1)
        start -= 1
        
    last = len(array) - 1
    
    while last > 0:
        array[last], array[0] = array[0], array[last]
        array = fix_down(array, 0, last)
        last -= 1
        yield(0, last) # placeholder; need to figure out a way to take child and idx from fix_down
    
def merge(array): pass

def partition(array, first, last):
    aux = array[last]
    i = first - 1
    j = last
    
    while True:
        i += 1
        j -= 1
        while array[i] < aux and i <= j: i += 1
        while aux < array[j] and j >= i: j -= 1
        if i >= j: break
        array[i], array[j] = array[j], array[i]
        
    array[i], array[last] = array[last], array[i]
    
    return i

def quick(array):
    """ not recursive because yield would stop working """
    
    stack = []
    stack.extend((0, len(array) - 1))
    while stack:
        right = stack.pop()
        left = stack.pop()
        if right <= left: continue
        
        i = partition(array, left, right)
        yield(i, right) # this doesn't work like the other ones yet, working on it
        if i - left > right - i:
            stack.extend((left, i - 1, i + 1, right))
        else:
            stack.extend((i + 1, right, left, i - 1))
        
def shell(array):
    """ shellsort is basically a more general version of insertion sort 
    the gaps array is one of the simplest sequences """
    gaps = [1, 8, 23, 77, 281, 1073, 4193]
    
    for h in reversed(gaps):
        for i in range(h, len(array)):
            aux = array[i]
            j = i
            while j >= h and array[j - h] > aux:
                array[j - h], array[j] = array[j], array[j - h]
                yield(j, j - h)
                j -= h
            array[j] = aux
             
def bogo(array):
    """ included just because it's hilarious(ly ineffective). O(n!) complexity 
        might be a lot more effective with a custom-made check-if-sorted function
        but I didn't think it would matter much in this case. """
    
    while sorted(array) != array:
        shuffle(array)
        yield tuple() # returns an empty tuple just to draw the array

def comb(array):
    h = len(array) - 1 
    switched = True
    shrink = 1.25
    
    while h > 1:
        h = int(h // shrink)
        
        i = 0
        while i + h < len(array):
            if array[i] > array[i + h]:
                array[i], array[i + h] = array[i + h], array[i]
                yield(i, i + h)
            i += 1

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
