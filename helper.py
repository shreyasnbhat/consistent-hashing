import random
import math

INT_MAX = int("".join(['f'] * 32), 16)


def generate_random(size, max_cap):
    l = []

    for i in range(size):
        l.append(random.randint(1, max_cap))

    return l


def hash_to_coordinates(hash, x=0, y=0, radius = 1):
    radians = (hash / INT_MAX) * (2 * math.pi)
    return x + (radius * math.cos(radians)), y + (radius * math.sin(radians))


def get_annotation_position(hash,radius,flag):
    radians = (hash / INT_MAX) * (2 * math.pi)
    if flag:
        return (radius + 1) * math.cos(radians) , (radius + 1) * math.sin(radians)
    else:
        return (radius - 1) * math.cos(radians) , (radius - 1) * math.sin(radians)


def slice(tuples):
    x = [tuples[i][0] for i in range(len(tuples))]
    y = [tuples[i][1] for i in range(len(tuples))]
    return x,y
