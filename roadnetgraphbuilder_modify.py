import geopandas as gpd
import osmnx as ox
import networkx as nx
from shapely.geometry import Point
import matplotlib.pyplot as plt
import logging

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
        将 shapefile 转换为图形数据。
        从指定的 shapefile 中读取数据，并创建一个 MultiDiGraph 图。
        根据 shapefile 中的线段，构建图的节点和边，并将结果保存到文件。
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
            self.G.add_edge(start_edge_index, end_edge_index, length=line.Shape_Leng, roadname=line.OSM_NAME)
            #if the road is the bidirection way, so add the reverse road to the graph
            if (line.oneway == 'B'):
                self.G.add_edge(end_edge_index, start_edge_index, length=line.Shape_Leng)
                logging.info("found a bidirection edge : %s | %s ---- %s", end_edge_index, start_edge_index, line.oneway)
        #return
        logging.info(self.node_dict)
        nx.write_gml(self.G, 'result/graphresult.gml')
        #print the graph data
        logging.info(self.G)
        pos = nx.get_node_attributes(self.G,'pos')  # 确定节点的布局
        nx.draw_networkx_nodes(self.G, pos)
        nx.draw_networkx_edges(self.G, pos)
        #nx.draw_networkx_labels(G, pos)
        plt.show()



if __name__ == '__main__':
    model = RoadnetGraphBuilder("./data/testdata.shp")
    model.convert_shapefile_to_graph()