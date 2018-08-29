from hashring import *

if __name__ == '__main__':
    keys = generate_random(100, 1000000)
    nodes = ['s' + str(i) for i in range(10)]

    h = HashCircle(keys, [])


    for i in nodes:
        h.add_node(i)

    h.plot_all(3)

