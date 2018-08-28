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
