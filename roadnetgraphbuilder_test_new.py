import csv
import geopandas as gpd
import osmnx as ox
import networkx as nx
from  shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import logging
import pickle
from rtree import index
import pandas as pd

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
            # get the roadId or roadName to the edge
            #roadID = line.FID
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
                self.G.add_node(start_edge_index, x=start_point[0], y=start_point[1], pos=start_node_key, nodeid= start_edge_index)
                self.node_dict[start_node_key] = start_edge_index

            # is there any end node existed
            end_node_key = (end_point[0], end_point[1])
            if end_node_key in self.node_dict:
                end_edge_index = self.node_dict[end_node_key]
                logging.info("found a existed end point : %s", end_edge_index)
            else:
                # existing_end_nodes
                end_edge_index = i + 1
                self.G.add_node(end_edge_index, x=end_point[0], y=end_point[1], pos=end_node_key, nodeid = end_edge_index)
                self.node_dict[end_node_key] = end_edge_index

            #initial the start index of the next loop
            i=i+2
            #add the edge from aboved two nodes
            #self.G.add_edge(start_edge_index, end_edge_index, length=line.Shape_Leng, roadname=line.OSM_NAME)
            self.G.add_edge(start_edge_index, end_edge_index, length=line.Shape_Leng, roadname=line.osm_name,startnode=start_edge_index,endnode=end_edge_index)
            #if the road is the bidirection way, so add the reverse road to the graph
            #if (line.oneway == 'B'):
            #    self.G.add_edge(end_edge_index, start_edge_index, length=line.Shape_Leng)
            #    logging.info("found a bidirection edge : %s | %s ---- %s", end_edge_index, start_edge_index, line.oneway)
        #return
        #logging.info(self.node_dict)


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

    def save_graph_to_file(self, saveurl):
        nx.write_gml(self.G, saveurl)
        # save to binary data using pickle
        #with open('../result/graph1.pkl', 'wb') as f:
        #    pickle.dump(self.G, f)
        # print the graph data
        logging.info(self.G)

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
        self.G = nx.read_gml('./result/graph_dissolvedname1.gml')
        logging.info(self.G)
        duplicate_edges = self.check_duplicate_edges()
        logging.info(duplicate_edges)

    def load_saved_binary_graph(self):
        #load the binary graph data
        with open('./result/graph1.pkl', 'rb') as f:
            self.G = pickle.load(f)
            logging.info(self.G)

    def check_saved_index(self):
        idx = index.Index('./data/rtree_index')
        print(idx)


    def check_duplicate_edges(self):
        # Get all edges in the graph
        edges = list(self.G.edges(data=True))
        # Create a set to store unique edges
        edge_set = set()

        # List to store duplicate edges
        duplicate_edges = []

        # Check each edge
        for edge in edges:
            # Get the nodes of the edge (without considering the direction)
            edge_nodes =(edge[0], edge[1])

            # If the edge has been seen before, it's a duplicate
            if edge_nodes in edge_set:
                duplicate_edges.append(edge)
            else:
                edge_set.add(edge_nodes)

        return duplicate_edges

    def export_Graph_Nodes_to_CSV(self):
        with open("./result/nodes_data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # write the header
            writer.writerow(["ID", "Label", "x", "y","nodeid"])  # 替换"Attribute1"和"Attribute2"为你的节点属性列名

            # write the node data
            for node_id, node_data in self.G.nodes(data=True):
                node_label = node_data.get("label", "")
                x = node_data.get("x", "")
                y = node_data.get("y", "")
                nodeid = node_data.get("nodeid","")
                writer.writerow([node_id, node_label, x, y, nodeid])

        logging.info("All the nodes have been exported to the CSV file.")

    
    def export_Graph_edges_to_shapefile(self):
        edges_data = []
        for u, v, data in self.G.edges(data=True):
            geom = LineString([Point(self.G.nodes[u]["x"], self.G.nodes[u]["y"]),Point(self.G.nodes[v]["x"], self.G.nodes[v]["y"])])
            edges_data.append((geom,data))
        # convert the edge data to GeoDataFrame
        edges_gdf = gpd.GeoDataFrame(edges_data, columns=['geometry','attributes'], crs = 'EPSG:6583')
        #convert the attributes to a new DataFrame and joined to the original DataFrame(the pd.Series can create the new attributes table)
        edges_gdf = edges_gdf.join(edges_gdf['attributes'].apply(pd.Series))
        #then delete the old attributes
        edges_gdf = edges_gdf.drop(columns='attributes')
        #save the GeoDataFrame to a shapefile
        edges_gdf.to_file("./result/Road_edges_shapefile.shp")
        logging.info("All the edges have been exported to the Shapefile.")

if __name__ == '__main__':
    #load the shapefile data and convert to the graph data, saved to a GML file
    #model = RoadnetGraphBuilder("./data/testdata.shp")
    model = RoadnetGraphBuilder("./data/testdata_dissolve_name.shp")
    #model = RoadnetGraphBuilder("./data/roadnet_dissolved_by_name.shp")
    #model.convert_shapefile_to_graph()
    #model.calculate_shortest_path(120,3)

    #load the saved graph data from GML file
    model.load_saved_graph()

    #check the index
    #model.check_saved_index()

    #export nodes to CSV
    #model.export_Graph_Nodes_to_CSV()

    #export edges to shapefile
    model.export_Graph_edges_to_shapefile()