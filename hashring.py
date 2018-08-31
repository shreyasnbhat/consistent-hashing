import hashlib
from collections import defaultdict
from bisect import insort
import numpy as np
from helper import *


class History:
    nodes = 0
    keys = 0
    remapped = 0

    def __init__(self, nodes, keys, remapped):
        self.nodes = nodes
        self.keys = keys
        self.remapped = remapped

    def get_data(self):
        return self.keys/self.nodes , self.remapped


class HashCircle:
    keys = []
    nodes = []
    key_list = []
    node_list = []
    item_list = []
    item_position = None
    key_node_map = None
    node_key_count = None
    node_key_count_grouped = None
    node_weight = 1
    node_prefix_length = 1
    remap_history = []
    api_access = False

    def __init__(self, keys, nodes, node_prefix_length, node_weight):
        self.item_position = defaultdict(int)
        self.key_node_map = defaultdict(str)
        self.node_key_count = defaultdict(int)
        self.node_key_count_grouped = defaultdict(int)
        self.node_prefix_length = node_prefix_length
        self.init_nodes(nodes)
        self.init_keys(keys)
        self.node_weight = node_weight
        self.keys = keys

    def init_nodes(self, nodes):
        for i in nodes:
            self.add_weighted_node(i)

    def init_keys(self, keys):
        for i in keys:
            key_hash = int(hashlib.md5(np.int32(i)).hexdigest(), 16)
            self.item_position[key_hash] = i
            insort(self.key_list, key_hash)
            insort(self.item_list, key_hash)

    def add_history(self, w_nodes):
        remapped_keys = 0
        for i in w_nodes:
            remapped_keys += self.node_key_count[i]
        number_of_nodes = len(self.nodes) / self.node_weight
        hist = History(number_of_nodes, len(self.keys), remapped_keys)
        self.remap_history.append(hist.get_data())

    def add_weighted_node(self, node, weight, regenerate=False):
        w_nodes = [node + '-' + str(i) for i in range(weight)]
        for i in range(weight):
            self.add_node(w_nodes[i], regenerate)

        if regenerate:
            self.generate_map()

        if self.api_access:
            self.add_history(w_nodes)

    def add_node(self, node, regenerated):
        if node not in self.nodes:
            self.nodes.append(node)
            node_hash = int(hashlib.md5(node.encode('utf-8')).hexdigest(), 16)
            self.item_position[node_hash] = node
            insort(self.node_list, node_hash)
            insort(self.item_list, node_hash)

            if not regenerated:
                self.generate_map()

    def remove_weighted_node(self, node, weight, regenerate=False):
        w_nodes = [node + '-' + str(i) for i in range(weight)]

        if self.api_access:
            self.add_history(w_nodes)

        for i in range(weight):
            self.remove_node(w_nodes[i], regenerate)

        if regenerate:
            self.generate_map()


    def remove_node(self, node, regenerated):
        if node in self.nodes:
            self.nodes.remove(node)
            node_hash = int(hashlib.md5(node.encode('utf-8')).hexdigest(), 16)
            self.node_list.remove(node_hash)
            self.item_list.remove(node_hash)
            del self.item_position[node_hash]

            if not regenerated:
                self.generate_map()

    def generate_map(self):

        self.key_node_map.clear()
        self.node_key_count.clear()
        self.node_key_count_grouped.clear()

        # Need to assign every key the next greater node hash as the cache server for the key
        node_index = 0
        for i in self.key_list:

            node_hash = self.node_list[node_index]

            if i <= node_hash:
                self.key_node_map[self.item_position[i]] = self.item_position[node_hash]
                self.node_key_count[self.item_position[node_hash]] += 1
                self.node_key_count_grouped[self.get_node_group(node_hash)] += 1
            else:
                if node_index == len(self.node_list) - 1:
                    self.key_node_map[self.item_position[i]] = self.item_position[self.node_list[0]]
                    self.node_key_count[self.item_position[self.node_list[0]]] += 1
                    self.node_key_count_grouped[self.get_node_group(self.node_list[0])] += 1
                else:
                    while node_hash < i:
                        if node_index < len(self.node_list) - 1:
                            node_index += 1
                            node_hash = self.node_list[node_index]
                        else:
                            node_index = 0
                            node_hash = self.node_list[node_index]
                            break

                    self.key_node_map[self.item_position[i]] = self.item_position[node_hash]
                    self.node_key_count[self.item_position[node_hash]] += 1

                    self.node_key_count_grouped[self.get_node_group(node_hash)] += 1

        print(self.node_key_count_grouped)
        # self.print_status()

    def get_node_group(self, node_hash):
        node_group_split = self.item_position[node_hash].split('-')
        node_group = node_group_split[0] + '-' + node_group_split[1]
        return node_group

    def print_status(self, verbose=False):

        if verbose:
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
            print(i, self.node_key_count[i])

    def plot_requirements(self, radius):

        x_key = []
        y_key = []

        x_node = []
        y_node = []
        hover_labels = []

        for i in self.key_list:
            a, b = hash_to_coordinates(i, 0, 0, radius)
            x_key.append(a)
            y_key.append(b)

        for i in self.node_list:
            a, b = hash_to_coordinates(i, 0, 0, radius)
            x_node.append(a)
            y_node.append(b)
            hover_labels.append(self.item_position[i])

        x_count = []
        y_count = []
        temp_sort = []

        for i in self.node_key_count_grouped.keys():
            temp_sort.append((i, self.node_key_count_grouped[i]))
        temp_sort.sort(key=lambda x: int(x[0].split('-')[1]))

        for i in temp_sort:
            x_count.append(i[0])
            y_count.append(i[1])

        return x_key, y_key, x_node, y_node, hover_labels, x_count, y_count

    def plot_all(self, radius):

        x_key, y_key, x_node, y_node, hover_labels, x_count, y_count = self.plot_requirements(radius)

        trace1 = dict(
            type='scatter',
            x=x_key,
            y=y_key,
            xaxis='x',
            yaxis='y',
            name='Keys',
            textfont=dict(
                family='sans serif',
                size=18,
                color='#263238'
            ),
            mode='markers',
            marker=dict(
                color='#00897B',
                size=10,
                line=dict(width=0.3)
            )
        )

        trace2 = dict(
            type='scatter',
            x=x_node,
            y=y_node,
            xaxis='x',
            yaxis='y',
            text=hover_labels,
            textfont=dict(
                family='sans serif',
                size=18,
                color='#263238'
            ),
            mode='markers',
            name='Nodes',
            marker=dict(
                color='#D84315',
                size=15,
                line=dict(width=0.3)
            )
        )

        trace3 = dict(
            type='bar',
            name='Key Distribution',
            x=x_count,
            y=y_count,
            xaxis='x2',
            textfont=dict(
                family='sans serif',
                size=18,
                color='#263238'
            ),
            yaxis='y2',
            marker=dict(
                color='#EF5350'
            )
        )

        data = [trace1, trace2, trace3]

        annotations = []
        direction = True
        for i in range(len(self.node_list)):
            x = x_node[i]
            y = y_node[i]
            label = hover_labels[i]

            ax, ay = get_annotation_position(self.node_list[i], radius, direction)
            direction = not direction

            annotation_text_split = label.split('-')
            annotation_text = annotation_text_split[0] + '-' + annotation_text_split[1]

            node_annotation = dict(
                x=x,
                y=y,
                xref='x',
                yref='y',
                axref='x',
                ayref='y',
                text=annotation_text,
                showarrow=True,
                arrowhead=7,
                ax=ax,
                ay=ay,
                font=dict(
                    family='Courier New, monospace',
                    size=16,
                    color='#263238'
                ),
                bordercolor='#FF6F00',
                borderwidth=2,
                borderpad=4,
                bgcolor='#FFA000',
                opacity=0.8
            )

            if len(self.node_list) / self.node_weight < 8:
                annotations.append(node_annotation)

        layout = dict(
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(family='Courier New, monospace', size=18, color='#263238'),
            xaxis=dict(
                domain=[0, 0.45],
                range=[-(radius + 1), (radius + 1)],
            ),
            yaxis=dict(
                domain=[0, 1],
                range=[-(radius + 1), (radius + 1)]
            ),
            xaxis2=dict(
                title="Node names",
                domain=[0.55, 1],
            ),
            yaxis2=dict(
                title="Node Key counts",
                domain=[0, 1],
                anchor='x2'
            ),
            legend=dict(
                x=1.0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            annotations=annotations,
            shapes=[dict(
                type='circle',
                xref='x',
                yref='y',
                x0=-radius,
                y0=-radius,
                x1=radius,
                y1=radius,
                line=dict(
                    color='rgba(50, 171, 96, 1)')
            )],
            bargap=0.15,
        )

        fig = {
            'data': data,
            'layout': layout,
        }

        return fig
