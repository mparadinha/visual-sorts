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


def mergesort(left, right):
    sorted = []
    while left or right:
        if not left:
            sorted.append(right.pop())
        elif not right:
            sorted.append(left.pop())
        else:
            if left[-1] > right[-1]:
                sorted.append(left.pop())
            else:
                sorted.append(right.pop())
    return list(reversed(sorted))

def merge(array):
    if len(array) < 2:
        return array
    middle = len(array)//2
    left = mergesort(array[:middle])
    right = mergesort(array[middle:])
    return merge(left, right)
def merge(array):
    stack = []
    if len(array > 1):
        middle = len(array)/2
        left = merge(array[0:middle])
        right = merge(array[middle:-1])
    return join(left, right)
