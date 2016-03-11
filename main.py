"""
This module is an usage example of the kruskal and kruskal_viz modules.

"""

import kruskal


if __name__ == '__main__':
    graph = set((
        (1, 'A', 'S'),
        (5, 'A', 'B'),
        (6, 'A', 'C'),
        (3, 'S', 'C'),
        (2, 'C', 'D'),
        (3, 'B', 'D'),
        (2, 'E', 'B'),
        (4, 'E', 'D'),
    ))
    print('GRAPH:', graph, '\n')

    clusterized, cc = kruskal.clustering(graph, 3)

    print('KRUSKAL (clustering):', clusterized)
    print('KRUSKAL (complete)  :', kruskal.minimum_spanning_tree(graph))
    print('CONNECTED COMPONENTS:', cc)
    print('CONNECTED COMPONENTS (as list of set):', tuple(cc.values()))
