import hashlib
from collections import defaultdict
from bisect import insort
import numpy as np
import random


class HashCircle:
    keys = []
    nodes = []
    key_list = []
    node_list = []
    item_list = []
    item_position = None
    key_node_map = None
    node_key_count = None

    def __init__(self, keys, nodes):
        self.keys = keys
        self.nodes = nodes
        self.item_position = defaultdict(int)
        self.key_node_map = defaultdict(str)
        self.node_key_count = defaultdict(int)
        self.init_nodes(nodes)
        self.init_keys(keys)

    def init_nodes(self, nodes):
        for i in nodes:
            node_hash = int(hashlib.md5(i.encode('utf-8')).hexdigest(), 16)
            self.item_position[node_hash] = i
            insort(self.node_list, node_hash)
            insort(self.item_list, node_hash)

    def init_keys(self, keys):
        for i in keys:
            key_hash = int(hashlib.md5(np.int32(i)).hexdigest(), 16)
            self.item_position[key_hash] = i
            insort(self.key_list, key_hash)
            insort(self.item_list, key_hash)

    def generate_map(self):

        # Need to assign every key the next greater node hash as the cache server for the key
        node_index = 0
        for i in self.key_list:

            node_hash = self.node_list[node_index]

            if i <= node_hash:
                self.key_node_map[self.item_position[i]] = self.item_position[node_hash]
                self.node_key_count[self.item_position[node_hash]] += 1
            else:
                if node_index == len(self.node_list) - 1:
                    self.key_node_map[self.item_position[i]] = self.item_position[self.node_list[0]]
                    self.node_key_count[self.item_position[self.node_list[0]]] += 1
                else:
                    while node_hash < i:
                        node_index += 1
                        node_hash = self.node_list[node_index]

                    self.key_node_map[self.item_position[i]] = self.item_position[node_hash]
                    self.node_key_count[self.item_position[node_hash]] += 1

        self.print_status()

    def print_status(self):
        print("Keys")
        for i in self.key_list:
            print(i, self.item_position[i])

        print()
        print("Nodes")
        for i in self.node_list:
            print(i, self.item_position[i])

        print()
        print("Key to Node map")
        print(self.key_node_map)

        print()
        print("Node Key count")
        for i in self.node_key_count.keys():
            print(i , self.node_key_count[i])

def generate_random(size, max):
    l = []

    for i in range(size):
        l.append(random.randint(1, max))

    return l


if __name__ == '__main__':
    keys = generate_random(1000, 3500)
    nodes = ['s1', 's2', 's3', 's4', 's5']

    h = HashCircle(keys, nodes)
    h.generate_map()
