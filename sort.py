import sys
from random import randint, shuffle
import argparse

import pygame
from pygame.locals import *

def main(args):
    wait_time = args.wait

    screen = pygame.display.set_mode((500 + 200, 500 + 2))
    clock = pygame.time.Clock()

    # the 100 random numbers
    array = list(range(1, 101))
    shuffle(array)

    # check if requested sort is available
    if not args.algorithm in sorts:
        print(args.algorithm, "is not a valid sort. The options are:", ", ".join(sorts.keys()))
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
    x = 1
    for i, val in enumerate(array):
        y = val * 5
        # green bars for current bars. white for all others
        color = (0, 255, 0) if i in highlights else (255, 255, 255)

        pygame.draw.rect(screen, color, pygame.Rect(x, 501 - y, 5, y))
        x += 7

    pygame.display.update()
    
def draw_completed_array(screen, array):
    x = 1
    
    # this is just because the switching looks ugly otherwise
    # because the last switched indexes are still green
    show_array(screen, array, ())
    
    for i, val in enumerate(array):
        y = val * 5
        color = (0, 255, 0)

        pygame.draw.rect(screen, color, pygame.Rect(x, 501 - y, 5, y))
        x += 7
        
        pygame.time.wait(5)
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

def merge(array): pass
    
def heap(array): pass

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
             
    

# there must be a better way!
sorts = {"bubble": bubble,
         "cocktail": cocktail,
         "selection": selection,
         "insertion": insertion,
         "merge": merge,
         "heap": heap,
         "quick": quick,
         "shell": shell}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visualisation of sorting algorithms build with Python and pygame")

    parser.add_argument("algorithm", type=str, default="bubble", nargs="?",
        help="Algorithm to use when sorting array ({})".format(", ".join(sorts.keys())))

    parser.add_argument("--wait", type=int, metavar="wait_time",
        help="Time to wait (in milliseconds) between each step of the sort.")

    args = parser.parse_args()
    main(args)
