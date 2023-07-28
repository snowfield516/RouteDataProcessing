import geopandas as gpd
import osmnx as ox
import networkx as nx
from shapely.geometry import Point
import matplotlib.pyplot as plt

gdf = gpd.read_file('data/testdata.shp')
#G = ox.graph_from_gdfs(gdf, gdf)
#define a nodes
#nodes = gpd.GeoDataFrame(columns=['geometry','lineid','x','y'])
G = nx.MultiDiGraph()
i = 0
for line in gdf.itertuples(index=False):
    #print(line)
    start_point = line.geometry.coords[0]
    end_point = line.geometry.coords[-1]
    lineid = line.OBJECTID
    start_edge_index = i
    G.add_node(start_edge_index, x=start_point[0], y=start_point[1])
    end_edge_index = i+1
    G.add_node(end_edge_index, x=end_point[0], y=end_point[1])
    i=i+2
    #G.add_edge(str(start_point), str(end_point), weight=line.Shape_Leng)

    G.add_edge(start_edge_index, end_edge_index, length=line.Shape_Leng)
    if (line.oneway == 'B'):
        G.add_edge(end_edge_index, start_edge_index, length=line.Shape_Leng)
        print(str(lineid) + '-----' + line.oneway)
    #nodes = nodes._append(gpd.GeoDataFrame({'geometry': [Point(start_point), Point(end_point)],'lineid':lineid},crs = gdf.crs ), ignore_index=True)
    #nodes['coords'] = nodes['geometry'].apply(lambda x: str(tuple(x.coords[:][0])))

    #nodes['x'] = nodes['geometry'].apply(lambda geom: geom.x)
    #nodes['y'] = nodes['geometry'].apply(lambda geom: geom.y)
    #nodes = nodes.drop(nodes.columns[0])

    #nodes = nodes.drop_duplicates(subset='coords')
    #nodes = nodes.drop(columns=nodes.columns[0])
    #nodes['dummy'] = 1  # 创建一个虚拟列
print(G)

nx.write_gml(G, 'result/graphB.gml')

#pos = nx.get_node_attributes(G,)  # 确定节点的布局
#nx.draw_networkx_nodes(G, pos)
#nx.draw_networkx_edges(G, pos)
#nx.draw_networkx_labels(G, pos)
plt.show()
#nodes = nodes.drop(columns=nodes.columns[0])
#print(nodes)
#G = ox.graph_from_gdfs(nodes, gdf)
#print(nodes)
#gdf.to_csv(path_or_buf='road.csv')
#nodes.to_csv(path_or_buf='test_delete.csv')
#print(G)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')