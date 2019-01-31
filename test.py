import unittest
import load_data
import make_graph
from functools import partial
import time
from flow import simulate_flow
from image_writer import ImageWriter


class TestLoad(unittest.TestCase):
    def test_data_format(self):
        data = load_data.load()
        self.assertGreater(len(data), 0, "Data should have rows")
        self.assertGreater(len(data[0]), 0, "Data should have columns")
        self.assertEqual(data.__class__, list,
                         "Data should be a list of lists")
        self.assertEqual(data[0].__class__, list, "Columns should be list")

    def validate_item_format(self, item):
        self.assertEqual(item.__class__, float, "Data items should be floats")
        self.assertGreater(item, -100, "Heights should be between above -100m")
        self.assertLess(item, 3000, "Data items should be below 3000m")

    def test_all_item_format(self):
        data = load_data.load()
        for i in data:
            for j in i:
                self.validate_item_format(j)

    def test_first_item_format(self):
        self.validate_item_format(load_data.load()[0][0])


class TestGraph(unittest.TestCase):
    def test_create_graph(self):
        data = load_data.load()
        graph = make_graph.convert_to_graph(data)
        self.assertEqual(
            len(graph), 4, "All items should be converted to graph")

    def test_graph_node_ordering(self):
        data = load_data.load()
        graph = make_graph.convert_to_graph(data)

        for i in range(len(graph) - 1):
            self.assertLessEqual(graph[i].altitude, graph[i + 1].altitude)

    def test_node_conversion(self):
        data = [[0.1, 0.2]]
        graph = make_graph.convert_to_graph(data)
        node = graph[1]

        self.assertEqual(node.altitude, 0.2)
        self.assertEqual(node.flow, 0.0)
        self.assertEqual(node.original_location, {(0, 1)})
        self.assertEqual(len(node.inflow), 0)
        self.assertEqual(len(node.outflow), 1)
        self.assertEqual(graph[0], next(iter(node.outflow)))

    def test_node_merging(self):
        data = [[0.1, 0.2], [0.1, 0.3]]
        graph = make_graph.convert_to_graph(data)
        self.assertEqual(len(graph), 3)

        node = graph[0]
        self.assertEqual(node.altitude, 0.1)
        self.assertEqual(node.flow, 0.0)
        self.assertEqual(node.original_location, {(0, 0), (1, 0)})
        self.assertItemsEqual(node.inflow, {graph[1], graph[2]})
        self.assertEqual(len(node.inflow), 2)
        self.assertEqual(len(node.outflow), 0)


class TestFlooding(unittest.TestCase):
    def is_border_location(self, size, x, y):
        return x == 0 or y == 0 or x == size-1 or y == size-1

    def any_border_location(self, locations, size):
        for i in locations:
            if self.is_border_location(size, *i):
                return True
        return False

    def test_border_exists_small(self):
        data = [[1, 2, 3], [1, 4, 3], [1, 2, 3]]
        graph = make_graph.convert_to_graph(data)
        for node in graph:
            node_touches_border = self.any_border_location(
                node.original_location, 3)
            self.assertEqual(node_touches_border, node.border)

    def test_border_exists_large(self):
        size = 50
        data = [list(range(size)) for i in range(size)]
        graph = make_graph.convert_to_graph(data)
        for node in graph:
            node_touches_border = self.any_border_location(
                node.original_location, size)
            self.assertEqual(node_touches_border, node.border)


class TestFlow(unittest.TestCase):
    def test_1d_flow(self):
        data = [[1, 2, 3]]
        graph = make_graph.convert_to_graph(data)
        writer = ImageWriter()
        simulate_flow(graph, writer)


if __name__ == '__main__':
    unittest.main()
