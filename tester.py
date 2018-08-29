from hashring import *
import string

if __name__ == '__main__':
    keys = generate_random(50, 100000)

    node_prefix_length = 5
    node_count = 5

    node_prefix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(node_prefix_length))

    nodes = [node_prefix + '-' + str(i) for i in range(node_count)]

    print(nodes)

    # Default node weight is set to 3
    # Prefix length is set to 5
    h = HashCircle(keys, [], node_prefix_length, 3)

    for i in nodes:
        # Passing True will regenerate map only after entire node
        # Node weight set to 5
        h.add_weighted_node(i, 3, True)

    h.remove_weighted_node(nodes[0],5,True)

    h.plot_all(3)
