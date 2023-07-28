import geopandas as gpd
import osmnx as ox
import networkx as nx
from  shapely.geometry import Point
import matplotlib.pyplot as plt
import logging
import pickle
from rtree import index

class RoadnetGraphBuilder:

    def __init__(self, shapefileurl):
        self.shapefileurl = shapefileurl
        # define a MultiDiGraph
        self.G = nx.MultiDiGraph()
        # define a node dictionary to check the duplicated node point
        self.node_dict = {}
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def convert_shapefile_to_graph(self):
        """
        Convert shapefiles to graphics data.
        Reads data from the specified shapefile and creates a MultiDiGraph graph.
        From the line segments in the shapefile, build the nodes and edges of the graph and save the result to a file.
        """
        #create the geodataset from the shapefile
        gdf = gpd.read_file(self.shapefileurl)
        # initial the start index of the nodes
        i = 1
        # loop every line frome the dataset
        for line in gdf.itertuples(index=False):
            #print(line)
            #get the start node of the line
            start_point = line.geometry.coords[0]
            #get the end node of the line
            end_point = line.geometry.coords[-1]
            # get the essential informaiton of the line
            lineid = line.OBJECTID

            #get the start index of the line
            start_node_key = (start_point[0], start_point[1])
            if start_node_key in self.node_dict:
                start_edge_index = self.node_dict[start_node_key]
                logging.info("found a existed start point : %s", start_edge_index)
            else:
                start_edge_index = i
                self.G.add_node(start_edge_index, x=start_point[0], y=start_point[1], pos=start_node_key)
                self.node_dict[start_node_key] = start_edge_index

            # is there any end node existed
            end_node_key = (end_point[0], end_point[1])
            if end_node_key in self.node_dict:
                end_edge_index = self.node_dict[end_node_key]
                logging.info("found a existed start point : %s", end_edge_index)
            else:
                # existing_end_nodes
                end_edge_index = i + 1
                self.G.add_node(end_edge_index, x=end_point[0], y=end_point[1], pos=end_node_key)
                self.node_dict[end_node_key] = end_edge_index

            #initial the start index of the next loop
            i=i+2
            #add the edge from aboved two nodes
            #self.G.add_edge(start_edge_index, end_edge_index, length=line.Shape_Leng, roadname=line.OSM_NAME)
            self.G.add_edge(start_edge_index, end_edge_index, length=line.Shape_Leng, roadname=line.osm_name)
            #if the road is the bidirection way, so add the reverse road to the graph
            #if (line.oneway == 'B'):
            #    self.G.add_edge(end_edge_index, start_edge_index, length=line.Shape_Leng)
            #    logging.info("found a bidirection edge : %s | %s ---- %s", end_edge_index, start_edge_index, line.oneway)
        #return
        #logging.info(self.node_dict)
        nx.write_gml(self.G, 'result/graphresult.gml')
        #save to binary data
        with open('result/graph.pkl', 'wb') as f:
            pickle.dump(self.G, f)
        #print the graph data
        logging.info(self.G)

        #buid the nodes index
        #self.build_nodes_index()

        pos = nx.get_node_attributes(self.G,'pos')  # 确定节点的布局
        nx.draw_networkx_nodes(self.G, pos)
        nx.draw_networkx_edges(self.G, pos)
        nx.draw_networkx_labels(self.G, pos)
        plt.ion()
        #plt.show()
        #shortest_path = nx.shortest_path(self.G, source=120, target=3)
        #logging.info("The shortest path between start and end nodes are : %s ", shortest_path)

    def calculate_shortest_path(self, startnode, endnode):
        print("-----------call function----------")
        shortest_path = nx.shortest_path(self.G, source=startnode, target=endnode)
        logging.info("The shortest path between start and end nodes are : %s ", shortest_path)

    def build_nodes_index(self):
        # Create a new R-tree index and save it to a file
        p = index.Property()
        p.dat_extension = 'dat'
        p.idx_extension = 'idx'
        p.ifx_extension = 'ifx'
        p.filename = 'rtree_index'
        idx = index.Index('./data/rtree_index', properties=p)
        print("------create a index")
        # Add nodes to the index
        for n, d in self.G.nodes(data=True):
            # Assume 'coord' is a tuple (x, y)
            pos = d['pos']
            idx.insert(n, pos + pos)  # (x, y, x, y) is the bounding box

        # The index is automatically saved to 'rtree_index.dat'

        # Later, you can load the index from the file
        #idx = index.Index('rtree_index')

    def load_saved_graph(self):
        #self.G = nx.read_gml('./result/graphresult.gml')
        logging.info(self.G)

        with open('result/graph.pkl', 'rb') as f:
            self.G = pickle.load(f)
            logging.info(self.G)

    def check_saved_index(self):
        idx = index.Index('./data/rtree_index')
        print(idx)



if __name__ == '__main__':
    #load the shapefile data and convert to the graph data, saved to a GML file
    #model = RoadnetGraphBuilder("./data/testdata.shp")
    #model = RoadnetGraphBuilder("./data/testdata_large.shp")
    model = RoadnetGraphBuilder("./data/roadnet_dissolved_by_name.shp")
    model.convert_shapefile_to_graph()
    #model.calculate_shortest_path(120,3)

    #load the saved graph data from GML file
    #model.load_saved_graph()

    #check the index
    #model.check_saved_index()
