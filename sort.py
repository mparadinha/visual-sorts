import sys
from random import randint, shuffle

import pygame
from pygame.locals import *

def main():
    if len(sys.argv) < 2:
        print("usage: python sort.py [<sort type>] [--wait=WAIT_TIME]")
        print("sorts:", ", ".join(sorts.keys()))
        print("e.g: python sort.py insertion --wait=25")

    screen = pygame.display.set_mode((500 + 200, 500 + 2))
    clock = pygame.time.Clock()

    wait_time = None
    for arg in sys.argv:
        if "--wait" in arg: wait_time = int(arg.split("=")[-1])
    args = [arg for arg in sys.argv if "--wait" not in arg]

    # the 100 random numbers
    array = list(range(1, 101))
    shuffle(array)

    # sort algorithm default to bubble sort
    if args[-1] in sorts: sort = sorts[args[-1]]
    else:
        print("no sort specified. defaulting to bubble sort")
        sort = bubble

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

    # wait for key press before closing
    while True:
        for event in pygame.event.get():
            if event.type in [QUIT, KEYUP]:
                pygame.quit()
                return

def show_array(screen, array, tested):
    x = 1
    for i, val in enumerate(array):
        y = val * 5
        # green bars for current bars. white for all others
        color = (0, 255, 0) if i in tested else (255, 255, 255)

        pygame.draw.rect(screen, color, pygame.Rect(x, 501 - y, 5, y))
        x += 7

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
        while array[i] < aux and i <= j:
            i += 1
        while aux < array[j] and j >= i:
            j -= 1
        if i >= j: break
        array[i], array[j] = array[j], array[i]
        #yield(array[i], array[j])
        
    array[i], array[last] = array[last], array[i]
    #yield(array[i], array[last])
    
    return i

def quick(array):
    stack = []
    stack.extend((0, len(array) - 1))
    while stack:
        r = stack.pop()
        l = stack.pop()
        if r <= l: continue
        
        i = partition(array, l, r)
        if i - l > r - i:
            stack.extend((l, i - 1, i + 1, r))
        else:
            stack.extend((i + 1, r, l, i - 1))
        yield(l, r)
        
    yield(l, r)
        

# basically, a generalized insertion sort
def shell(array):
    gaps = [1, 8, 23, 77, 281, 1073, 4193] # one of the fastest sequences 
    
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

main()
