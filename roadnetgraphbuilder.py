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

    def convertShapetoGraphdata(self):
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
            #for n,d in G.nodes(data=True):
            #    print((d['x'],d['y']))
            #existing_start_nodes = [n for n, d in G.nodes(data=True) if(true) print(str(n)+"|"+str(d))]

            #using a function to check whether the node existed
            existing_start_nodes = self.isAnyNodeExist(start_point[0], start_point[1])
            #existing_start_nodes = [n for n, d in G.nodes(data=True) if (start_point[0], start_point[1]) == (d['x'], d['y'])]
            # is there any start node existed
            if existing_start_nodes:
                #if existed， use the index of the first node as the edge's start node
                # print("found a existed start point : " + str(existing_start_nodes))
                logging.info("found a existed start point : %s", existing_start_nodes)
                start_edge_index = existing_start_nodes[0]
            else:
                #existing_end_nodes
                start_edge_index = i
                #add the start node to the graph
                self.G.add_node(start_edge_index, x=start_point[0], y=start_point[1], pos=(start_point[0],start_point[1]))

            #is there any end node existed
            existing_end_nodes = self.isAnyNodeExist(end_point[0], end_point[1])
            #existing_end_nodes = [n for n, d in self.G.nodes(data=True) if (end_point[0], end_point[1]) == (d['x'], d['y'])]
            if existing_end_nodes:
                #if existed， use the index of the fist node as the edge's end node
                # print("found a existed end point : " + str(existing_end_nodes))
                logging.info("found a existed end point : %s ", existing_end_nodes)
                end_edge_index = existing_end_nodes[0]
            else:
                # get the end index of the line
                end_edge_index = i + 1
                #add the end node to the graph
                self.G.add_node(end_edge_index, x=end_point[0], y=end_point[1], pos=(end_point[0],end_point[1]))
            #initial the start index of the next loop
            i=i+2
            #add the edge from aboved two nodes
            self.G.add_edge(start_edge_index, end_edge_index, length=line.Shape_Leng, roadname=line.OSM_NAME)
            #if the road is the bidirection way, so add the reverse road to the graph
            if (line.oneway == 'B'):
                self.G.add_edge(end_edge_index, start_edge_index, length=line.Shape_Leng)
                logging.info("found a bidirection edge : %s | %s ---- %s", end_edge_index, start_edge_index, line.oneway)
        #return
        nx.write_gml(self.G, 'result/graphresult.gml')
        #print the graph data
        logging.info(self.G)
        pos = nx.get_node_attributes(self.G,'pos')  # 确定节点的布局
        nx.draw_networkx_nodes(self.G, pos)
        nx.draw_networkx_edges(self.G, pos)
        #nx.draw_networkx_labels(G, pos)
        plt.show()



    def isAnyNodeExist(self,x,y):
        existednode = [n for n, d in self.G.nodes(data=True) if (x, y) == (d['x'], d['y'])]
        return existednode


if __name__ == '__main__':
    model = RoadnetGraphBuilder("./data/testdata.shp")
    model.convertShapetoGraphdata()