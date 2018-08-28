from hashring import *

if __name__ == '__main__':
    keys = generate_random(50000, 1000000)
    nodes = ['serv' + str(i) for i in range(20)]

    h = HashCircle(keys, [])


    for i in nodes:
        h.add_node(i)

    h.plot_all(3)

