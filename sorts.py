from random import shuffle

def bubble(array, display):
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
            display.print(array, (i, i+1))
            #yield (i, i + 1)

        rounds = last

def cocktail(array, display):
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
            display.print(array, (i, i + 1))
        end = last
        if not switched: break # no switches, list is ordered

        # go backwards
        switched = False
        for i in reversed(range(start, end)):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                first = i
                switched = True
            display.print(array, (i, i + 1))
        start = first

def selection(array, display):

    n = len(array)
    for j in range(n - 1):

        # find the smallest item after index j
        imin = j
        for i in range(j + 1, n):
            if array[i] < array[imin]: imin = i
            display.print(array, (j, i, imin))

        if imin != j:
            array[j], array[imin] = array[imin], array[j]
            display.print(array, (j, imin))

def insertion(array, display):

    n = len(array)
    for i in range(1, n):
        if array[i] > array[i - 1]: continue

        for j in range(0, i):
            display.print(array, (j, i))
            if array[i] < array[j]:
                array.insert(j, array.pop(i))
                break
        display.print(array, (j,))

def fix_down(array, idx, end):
    while 2 * idx < end - 1:
        child = 2 * idx + 1

        if child < end - 1 and array[child] < array[child + 1]: child += 1
        if array[idx] < array[child]:
            array[idx], array[child] = array[child], array[idx]

        idx = child

    return array

def heap(array, display):
    start = (len(array) - 2) // 2

    while start >= 0:
        array = fix_down(array, start, len(array) - 1)
        start -= 1

    last = len(array) - 1

    while last > 0:
        array[last], array[0] = array[0], array[last]
        array = fix_down(array, 0, last)
        last -= 1
        # placeholder; need to figure out a way to take child and idx from fix_down
        display.print(array, (0, last))


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

def quick(array, display):
    """ not recursive because yield would stop working """

    stack = []
    stack.extend((0, len(array) - 1))
    while stack:
        right = stack.pop()
        left = stack.pop()
        if right <= left: continue

        i = partition(array, left, right)
        # this doesn't work like the other ones yet, working on it
        display.print(array, (i, right))
        if i - left > right - i:
            stack.extend((left, i - 1, i + 1, right))
        else:
            stack.extend((i + 1, right, left, i - 1))

def shell(array, display):
    """ shellsort is basically a more general version of insertion sort
    the gaps array is one of the simplest sequences """
    gaps = [1, 8, 23, 77, 281, 1073, 4193]

    for h in reversed(gaps):
        for i in range(h, len(array)):
            aux = array[i]
            j = i
            while j >= h and array[j - h] > aux:
                array[j - h], array[j] = array[j], array[j - h]
                display.print(array, (j, j - h))
                j -= h
            array[j] = aux

def bogo(array, display):
    """ included just because it's hilarious(ly ineffective). O(n!) complexity
        might be a lot more effective with a custom-made check-if-sorted function
        but I didn't think it would matter much in this case. """

    while sorted(array) != array:
        shuffle(array)
        # returns an empty tuple just to draw the array
        display.print(array, tuple())

def comb(array, display):
    h = len(array) - 1
    switched = True
    shrink = 1.25

    while h > 1:
        h = int(h // shrink)

        i = 0
        while i + h < len(array):
            if array[i] > array[i + h]:
                array[i], array[i + h] = array[i + h], array[i]
                display.print(array, (i, i + h))
            i += 1


def join(array, l, m, r, aux):
    k=l
    i, j = l, m

    while k<r:
        if i < m and (j >= r or array[i] <= array[j]):
            aux[k] = array[i]
            i += 1
        else:
            aux[k] = array[j]
            j += 1

        k += 1

    k = l
    while k < r:
        array[k] = aux[k]
        k += 1


def mergesort(array, l, r, aux, display):
    if r-l < 2:
        return

    m = (r+l)//2
    mergesort(array, l, m, aux, display)
    mergesort(array, m, r, aux, display)
    display.print(array, ())
    return join(array, l, m, r, aux)


def merge(array, display):
    print(len(array))
    aux = list(range(len(array)))
    mergesort(array, 0, len(array), aux, display)
