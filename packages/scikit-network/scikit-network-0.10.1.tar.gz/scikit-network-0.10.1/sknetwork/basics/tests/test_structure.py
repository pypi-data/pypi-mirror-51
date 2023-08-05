# -*- coding: utf-8 -*-
# tests for metrics.py
""""tests for structure.py"""

import unittest

import numpy as np

from sknetwork.basics.structure import largest_connected_component, is_bipartite
from sknetwork.toy_graphs import star_wars_villains, rock_paper_scissors
from sknetwork.utils.adjacency_formats import bipartite2undirected


class TestStructure(unittest.TestCase):
    def setUp(self):
        self.adjacency = rock_paper_scissors()
        self.adjacency += self.adjacency.T
        self.biadjacency = star_wars_villains()
        self.undirected_bipartite = bipartite2undirected(self.biadjacency)

    def test_largest_cc(self):
        largest_cc, indices = largest_connected_component(self.adjacency, return_labels=True)
        self.assertAlmostEqual(np.linalg.norm(largest_cc.toarray() - np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])), 0)
        self.assertEqual(np.linalg.norm(indices - np.array([0, 1, 2])), 0)
        largest_cc, indices = largest_connected_component(self.biadjacency, return_labels=True)
        self.assertAlmostEqual(np.linalg.norm(largest_cc.toarray() - np.array([[1, 0, 1],
                                                                               [1, 0, 0],
                                                                               [1, 1, 1],
                                                                               [0, 1, 1]])), 0)
        self.assertEqual(np.linalg.norm(indices[0] - np.array([0, 1, 2, 3])), 0)
        self.assertEqual(np.linalg.norm(indices[1] - np.array([0, 1, 2])), 0)

    def test_is_bipartite(self):
        bipartite, biadjacency = is_bipartite(self.undirected_bipartite, return_biadjacency=True)
        self.assertEqual(bipartite, True)
        self.assertEqual(np.all(biadjacency.data == self.biadjacency.data), True)
