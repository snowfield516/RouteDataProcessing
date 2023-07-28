import unittest
import os
from roadnetgraphbuilder_test_new import RoadnetGraphBuilder
import networkx as nx
import pathlib
from pathlib import Path

class TestRoadnetGraphBuilder(unittest.TestCase):
    def test_convert_shapefile_to_graph(self):

        # get current file's FUll path
        current_file_path = Path(__file__).resolve()
        # Get the current path
        current_dir = current_file_path.parent
        # Get the parent path
        parent_dir = current_dir.parent

        #print(pathlib.Path(path).resolve())
        # create a RoadnetGraphBuilder Instance
        model = RoadnetGraphBuilder(Path(parent_dir) / "data" / "testdata_dissolve_name.shp")

        # call convert_shapefile_to_graph function
        model.convert_shapefile_to_graph()
        model.save_graph_to_file(Path(parent_dir) / "result" / "graph_dissolvedname1.gml")
        # check whether there is a netgraph
        self.assertIsInstance(model.G, nx.MultiDiGraph)

        # check the number of the nodes and edges
        # self.assertEqual(len(model.G.nodes), expected_number_of_nodes)
        # self.assertEqual(len(model.G.edges), expected_number_of_edges)

        # check whether there is a graph file
        self.assertTrue(os.path.exists(Path(parent_dir) /"result"/"graph_dissolvedname1.gml"))
        self.assertTrue(os.path.exists(Path(parent_dir) /"result"/"graph1.pkl"))

        # other check


if __name__ == '__main__':
    unittest.main()
