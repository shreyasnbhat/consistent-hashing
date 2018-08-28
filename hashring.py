import hashlib
from collections import defaultdict
from bisect import insort
import numpy as np
import plotly.graph_objs as go
import plotly
from helper import *


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
        self.item_position = defaultdict(int)
        self.key_node_map = defaultdict(str)
        self.node_key_count = defaultdict(int)
        self.init_nodes(nodes)
        self.init_keys(keys)

    def init_nodes(self, nodes):
        for i in nodes:
            self.add_node(i)

    def init_keys(self, keys):
        for i in keys:
            key_hash = int(hashlib.md5(np.int32(i)).hexdigest(), 16)
            self.item_position[key_hash] = i
            insort(self.key_list, key_hash)
            insort(self.item_list, key_hash)

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            node_hash = int(hashlib.md5(node.encode('utf-8')).hexdigest(), 16)
            self.item_position[node_hash] = node
            insort(self.node_list, node_hash)
            insort(self.item_list, node_hash)
            self.generate_map()

    def generate_map(self):

        # Need to assign every key the next greater node hash as the cache server for the key
        node_index = 0
        remappings = 0
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

    def plot_all(self,radius):

        x_key = []
        y_key = []

        x_node = []
        y_node = []
        hover_labels = []

        for i in self.key_list:
            a, b = hash_to_coordinates(i,0,0,radius)
            x_key.append(a)
            y_key.append(b)

        for i in self.node_list:
            a, b = hash_to_coordinates(i,0,0,radius)
            x_node.append(a)
            y_node.append(b)
            hover_labels.append(self.item_position[i])

        trace1 = go.Scattergl(
            x=x_key,
            y=y_key,
            xaxis='x',
            yaxis='y',
            name='Keys',
            mode='markers',
            marker=dict(
                color='#00897B',
                size=10,
                line=dict(width=0.3)
            )
        )

        trace2 = go.Scattergl(
            x=x_node,
            y=y_node,
            xaxis='x',
            yaxis='y',
            text=hover_labels,
            textfont=dict(
                family='sans serif',
                size=18,
                color='#1f77b4'
            ),
            mode='markers',
            name='Nodes',
            marker=dict(
                color='#D84315',
                size=15,
                line=dict(width=0.3)
            )
        )

        x_count = []
        y_count = []
        for i in self.node_key_count.keys():
            x_count.append(i)
            y_count.append(self.node_key_count[i])

        trace3 = go.Bar(
            name='Key Distribution',
            x=x_count,
            y=y_count,
            xaxis='x2',
            yaxis='y2',
            marker=dict(
                color='#EF5350'
            )
        )

        data = [trace1, trace2, trace3]

        layout = go.Layout(
            title='Consistent Hashing Plots',
            font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
            xaxis=dict(
                domain=[0, 0.45],
                range=[-(radius+1), (radius+1)],
            ),
            yaxis=dict(
                domain=[0, 1],
                range=[-(radius+1), (radius+1)]
            ),
            xaxis2=dict(
                domain=[0.55, 1],
            ),
            yaxis2=dict(
                domain=[0, 1],
                anchor = 'x2'
            ),
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            width=1900,
            height=800,
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
            bargap=0.15
        )

        fig = {
            'data': data,
            'layout': layout,
        }

        plotly.offline.plot(fig, auto_open=True)
        print("Done")
