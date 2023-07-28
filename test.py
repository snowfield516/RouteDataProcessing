import networkx as nx
import matplotlib.pyplot as plt

# 创建一个简单的图形
G = nx.Graph()
G.add_node(1, pos=(40.7128, -74.0060))  # 添加一个节点，指定经纬度坐标
G.add_node(2, pos=(40.7589, -73.9851))
G.add_node(3, pos=(40.7915, -73.9647))
G.add_edge(1, 2)
G.add_edge(2, 3)
nx.write_gml(G, 'result/graphtest.gml')
print(G)
# 绘制图形
pos = nx.get_node_attributes(G, 'pos')  # 获取节点的坐标属性
nx.draw_networkx_nodes(G, pos, node_size=100, node_color='r')
nx.draw_networkx_edges(G, pos)
plt.show()