"""
This module defines the kruskal clustering algorithm.

The graph representation of the graph should be an iterable of edges,
where each edges should be a tuple (weight, source node, target node).

The main API of the module is:

    clustering(2), returning the minspan tree and clusters found in input graph
    minimum_spanning_tree(1), returning a minimum spanning tree for input graph

"""

from itertools import chain
from functools import partial
from collections import defaultdict


def minimum_spanning_tree(edges):
    """Return the set of edges composing the minimum spanning tree of given
    graph"""
    parent, rank, cc = {}, {}, {}
    for vertex in _vertices(edges):
        _make_set(vertex, parent=parent, rank=rank, cc=cc)
    find = partial(_find, parent=parent)

    minspantree = set()
    for edge in sorted(edges):
        weight, vertice1, vertice2 = edge
        if find(vertice1) != find(vertice2):
            _union(vertice1, vertice2, parent=parent, rank=rank)
            minspantree.add(edge)
    return minspantree


def clustering(edges:iter, nb_clusters:int=2):
    """Compute the nb_clusters clusters in the given graph, and returns the
    pair(a, b) where a is the set of edges making the clusters,
    and b the dict of connected components as {root: set of vertices}"""
    try:
        assert all(len(edge) == 3 for edge in edges)
    except AssertionError:
        raise ValueError('Given graph must be an iterable of 3-tuple, '
                         'defining an edge (weight, source node, target node).')
    # define data structures and union count to perform
    parent, rank, cc = {}, {}, {}
    vertices = _vertices(edges)
    nb_unions = len(vertices) - nb_clusters
    # functions currying
    union_returning_choosen = partial(_union_returning_choosen,
                                      parent=parent, rank=rank)
    find = partial(_find, parent=parent)

    for vertex in vertices:
        _make_set(vertex, parent=parent, rank=rank, cc=cc)

    minspantree = set()
    union_performed = 1
    for edge in sorted(edges):
        if union_performed > nb_unions:
            break
        weight, vertice1, vertice2 = edge
        root1 = find(vertice1)
        root2 = find(vertice2)
        if root1 != root2:
            union_result = union_returning_choosen(vertice1, vertice2)
            if union_result:
                choosen_root, unchoosen_root = union_result
                assert choosen_root in cc
                assert unchoosen_root in cc
                # union complexity: O(len(a) + len(b))
                cc[choosen_root] |= cc[unchoosen_root]  # a |= b <=> a = a | b où | est union des ensembles 
                del cc[unchoosen_root]
                assert find(vertice1) == find(vertice2)
            # this is possibly false: if union result if false, the edge
            # should not be added to the minspantree, and the union coundn't
            # be considered as performed
            minspantree.add(edge)
            union_performed += 1
    # endfor
    return minspantree, cc


def _union(vertice1, vertice2, parent:dict, rank:dict):
    """Perform the union of given vertices"""
    root1 = _find(vertice1, parent)
    root2 = _find(vertice2, parent)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
            if rank[root1] == rank[root2]: rank[root2] += 1

def _union_returning_choosen(vertice1, vertice2, parent:dict, rank:dict):
    """perform the union, then returns the pair (a, b) where a is the new root
    of the connected component, and b the node that is no longer a root."""
    root1 = _find(vertice1, parent)
    root2 = _find(vertice2, parent)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
            return root1, root2
        else:
            parent[root1] = root2
            if rank[root1] == rank[root2]:
                rank[root2] += 1
            return root2, root1


def _vertices(edges:set):
    """Return set of nodes found from given iterable of edges"""
    return set(chain(*((source, target) for _, source, target in edges)))

def _make_set(vertice, parent:dict, rank:dict, cc:dict):
    """Initialize given parent, rank and cc for given vertex"""
    parent[vertice] = vertice
    rank[vertice] = 0
    cc[vertice] = set([vertice])

def _find(vertice, parent:dict):
    """Find parent of given vertice in given parent dict"""
    if parent[vertice] != vertice:
        parent[vertice] = _find(parent[vertice], parent)
    return parent[vertice]
