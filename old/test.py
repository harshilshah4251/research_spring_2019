import osmnx as ox
import numpy as np
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import re
import json


#creating a graph
#simplify graph 
G = ox.graph_from_point((33.775259139909664, -84.39705848693849), distance = 500, network_type='drive')
#fig, ax = ox.plot_graph(G,show=True, close=False, 
                         #edge_color='black')
ox.plot_graph(G)

# gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

# gdf_u_v = gdf_edges[['u','v', 'osmid']]
# #print(gdf_edges)
# networkx_edges = [tuple(edge) for edge in gdf_u_v.values]
# print("Network edges : {}".format(networkx_edges))

# networkx_graph = nx.MultiDiGraph()
# #networkx_graph = nx.read_graphml("graphml.xml")
# networkx_graph.add_edges_from(networkx_edges, id = networkx_edges[2])
# #print("# of edges : {}".format(len(networkx_graph.edges)))
# pos=nx.spring_layout(networkx_graph)
# nx.draw(networkx_graph, pos = pos,  node_size = 5, node_color = "blue")
# plt.show()

# num_cameras = 3
# #generate random camera locations. only works for straight lines
# random_indices = np.arange(len(networkx_edges))
# np.random.shuffle(random_indices)
# random_edges_indices = random_indices[:num_cameras]

# #generate random cam ids
# rand_to_generate = 3 * num_cameras
# random_indices = np.arange(1000, 9999)
# np.random.shuffle(random_indices)
# rand_ids = random_indices[:rand_to_generate]
# j = 0 #for assiging ids to cam and edges
# for i in range(num_cameras):
#     random_edge_index = random_edges_indices[i]
#     random_edge = gdf_edges[random_edge_index:random_edge_index + 1][:]
#     # line = random_edge['geometry'].bounds
#     # line_start_x = line['minx']
#     # line_start_y = line['miny']
#     # line_end_x = line['maxx']
#     # line_end_y = line['maxy']
#     # slope = (line_end_y - line_start_y) / (line_end_x - line_start_x)
#     # random_x = (line_end_x - line_start_x) * np.random.uniform(0, 1) + line_start_x
#     # random_point = [random_x, (slope * (random_x - line_start_x)) + line_start_y]
#     #print(random_edge)
#     u_node = int(random_edge['u'])
#     v_node = int(random_edge['v'])
#     print("U : {}, V : {}".format(u_node, v_node))
#     networkx_graph.remove_edge(u_node, v_node)
#     # cam_id = str(np.random.randint(1000, 9999))
#     cam_id = rand_ids[j]
#     new_edge_1_id = rand_ids[j+1]
#     new_edge_2_id = rand_ids[j+2]
#     networkx_graph.add_node("cam"+str(cam_id))
#     networkx_graph.add_edge(u_node, "cam"+str(cam_id), key="cam_edge"+str(new_edge_1_id))
#     networkx_graph.add_edge("cam"+str(cam_id), v_node, key="cam_edge"+str(new_edge_2_id))
#     j+=3

# #do coloring
# color_map = []
# cam_labels = {}
# for node in list(networkx_graph.nodes):
#     if re.search("cam", str(node)):
#         color_map.append("red")
#         cam_labels[node] = node
#     else:
#         color_map.append("blue")

# print("# of edges : {}".format(len(networkx_graph.edges)))
# pos =  nx.fruchterman_reingold_layout(networkx_graph)
# nx.draw(networkx_graph, node_size = 10, pos =pos, node_color = color_map, with_labels = False)
# nx.draw_networkx_labels(networkx_graph, pos=pos, labels = cam_labels,font_size=10,font_color='r')
# plt.show()
# print("Network edges : {}".format(networkx_graph.edges))

# #nx.write_graphml_lxml(networkx_graph, "graphml.xml")
# #print json
# graph_json = {}
# graph_json["edges"] = []
# for edge in list(networkx_graph.edges):
#     json_edge = {}
#     json_edge["u"] = str(edge[0])
#     json_edge["v"] = str(edge[1])
#     json_edge["id"] = str(edge[2])
#     graph_json["edges"].append(json_edge)


# with open('graph.json', 'w') as graph_json_file:
#     json.dump(graph_json, graph_json_file, indent=4)





# G = nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
# G.add_path([0,1,2])
# print(G.edges())
# G.remove_node(1)
# G.edges()

# G = nx.MultiDiGraph()
# G.add_edges_from([(1, 2), (1, 3), (1, 4)])  # key_list returned
# print(G.edges)
# G.remove_edge(1, 2) 

# # print(G.edges)



# print(gdf_nodes)
# networkx_graph.add_nodes_from(networkx_nodes)
# print(gdf_edges.head()['geometry'][1])
# fig, ax = ox.plot_graph(G,show=False, close=False, 
#                          edge_color='black')


# print("Random point : {}".format(random_point))
# ax.scatter(random_point[0], random_point[1], c='red', s=50)

# print("line_start_x : {} \n line_start_y : {} \n line_end_x : {} \n line_end_y : {}".format(line_start_x, line_start_y, line_end_x, line_end_y))