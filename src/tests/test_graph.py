import unittest

from data_structures.location_graph import LocationGraph
from utils.load_data import load_data


class TestGraph(unittest.TestCase):
    def all_connections_both_directions(self, graph):
        for node in graph.ascending():
            for i in node.links.inflow():
                self.assertTrue(node in i.links.outflow())
            for i in node.links.outflow():
                self.assertTrue(node in i.links.inflow())

    def test_create_graph(self):
        graph = LocationGraph(load_data())
        self.assertEqual(len(graph), 4, "All items should be converted to graph")
        self.all_connections_both_directions(graph)

    def test_graph_node_ordering(self):
        graph = LocationGraph(load_data())
        node_list = list(graph.ascending())
        for i in range(len(node_list) - 1):
            self.assertLessEqual(node_list[i].altitude, node_list[i + 1].altitude)

    def test_node_conversion(self):
        graph = LocationGraph([[0.1, 0.2]])
        node = graph.highest

        self.assertEqual(node.altitude, 0.2)
        self.assertEqual(node.flow, 0.0)
        self.assertEqual(node.position, {(0, 1)})
        self.assertEqual(len(list(node.links.inflow())), 0)
        self.assertEqual(len(list(node.links.outflow())), 1)
        self.assertEqual(graph.lowest, next(iter(node.links.outflow())))
        self.all_connections_both_directions(graph)

    def test_node_merging(self):
        graph = LocationGraph([[0.1, 0.2], [0.1, 0.3]])
        self.all_connections_both_directions(graph)
        self.assertEqual(len(graph), 3)

        node = graph.lowest
        self.assertEqual(node.altitude, 0.1)
        self.assertEqual(node.flow, 0.0)
        self.assertEqual(node.position, {(0, 0), (1, 0)})
        self.assertEqual(node.inflow, {node.next, node.next.next})
        self.assertEqual(len(node.inflow), 2)
        self.assertEqual(len(node.outflow), 0)

    def test_multiple_merged_points(self):
        graph = LocationGraph([[2, 2, 2], [2, 1, 2], [2, 2, 2]])
        self.all_connections_both_directions(graph)
        self.assertEqual(len(graph), 2)
        self.assertEqual(graph.highest.starting_location, (1, 1))
        self.assertEqual(graph.lowest.starting_location, (0, 0))
