# consistent-hashing
An attempt to analyze the claims put forward by consistent hashing.

A visualization of the hashring and the key distribution among nodes is presented.

<img src="https://raw.githubusercontent.com/shreyasnbhat/consistent-hashing/master/plot.png" alt="drawing" width="900px"/>
The plot describes a hashring with 50 keys and 10 nodes without any node weights.

#### Initial parameters
| Parameter   |      Value      |
|:------------|-------------:|
| Node Count  | 3 |
| Key Count   | 500 |
| Node Weight | 10 |

The plot describes a simple simulation with the above initial parameters. 5 nodes are added, 3 nodes a removed, 2 nodes are added and then finally 3 nodes are removed.

<img src="https://raw.githubusercontent.com/shreyasnbhat/consistent-hashing/master/history.png" alt="drawing" width="500px"/>

We can observe that the number of keys remapped hovers around the average remap metric i.e. `K/N` where `K` is the number of keys and `N` is the number of nodes.
