import osmnx as ox
import numpy as np
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import re
import json



def dfs(graph, vehicles):
    visited = []
    stack = []
    notify_cams = []
    for vehicle in vehicles:
        start_node = list(filter(lambda edge: edge[2] == vehicle["edge_id"], graph.edges))[0][1]
        stack.append(start_node)
        while len(stack) != 0:
            node = stack.pop()
            if node not in visited:
                visited.append(node)
                for neighbor in list(networkx_graph.neighbors(node)):
                    if re.search("cam", neighbor):
                        notify_cams.append(neighbor)
                    else:
                        stack.append(neighbor)
                    

    print(notify_cams)
        

        



with open("graph.json") as graph_file:
    graph_data = json.load(graph_file)


networkx_graph = nx.MultiDiGraph()
networkx_edges = [tuple([edge["u"], edge["v"], edge["id"]]) for edge in graph_data["edges"]]
networkx_graph.add_edges_from(networkx_edges, id = networkx_edges[2])



#vehicle
vehicles = graph_data["vehicles"]

for vehicle in vehicles:
    vehicle_edge = vehicle["edge_id"]



#do coloring
node_color_map = []
edge_color_map = ["black"] * len(list(networkx_graph.edges))
cam_labels = {}
for node in list(networkx_graph.nodes):
    if re.search("cam", str(node)):
        node_color_map.append("red")
        cam_labels[node] = node
    else:
        node_color_map.append("blue")
        cam_labels[node] = node


for vehicle in vehicles:
    for index, edge in enumerate(list(networkx_graph.edges)):
        if edge[2] == vehicle["edge_id"]:
            edge_color_map[index] = "orange"
            break

#print(edge_color_map)
#print("# of edges : {}".format(len(networkx_graph.edges)))
pos =  nx.circular_layout(networkx_graph)
# nx.draw(networkx_graph, node_size = 10, pos = pos, node_color = node_color_map, edge_color=edge_color_map, alpha = 0.5, with_labels = False)
# nx.draw_networkx_labels(networkx_graph, pos=pos, labels = cam_labels,font_size=10,font_color='r')
#print(networkx_graph.nodes)
#ox.plot_graph(networkx_graph)
#plt.show()
#dfs(networkx_graph, vehicles)



    







#print("Network edges : {}".format(networkx_graph.edges))

