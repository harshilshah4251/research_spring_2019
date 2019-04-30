import osmnx as ox
import numpy as np
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import re
import json
import random
from IPython.display import IFrame
ox.config(log_console=True, use_cache=True)
import time



def backtrace_route(parents, start, end):
    route = []
    currentNode = start
    count = 0
    while currentNode != end and count < 20:
        route.append(int(currentNode))
        currentNode = parents[currentNode]
        count += 1
    route.append(int(currentNode))
    route.reverse()
    #print("Route:{}".format(route))
    return route

def dfs(graph, vehicles, camera_nodes):
    data = {}
    for vehicle in vehicles:
        #print(vehicle)
        visited = []
        stack = []
        parents = {}
        start_node = list(filter(lambda edge: edge == vehicle, graph.edges))[0][1]
        data[str(start_node)] = {"notified_cams" :[], "route": []}  
        #print(start_node)
        stack.append(start_node)
        while len(stack) != 0:
            node = stack.pop()
            if node not in visited:
                visited.append(node)
                for neighbor in list(G.neighbors(node)):
                    if neighbor in camera_nodes:
                        parents[str(neighbor)] = str(node)
                        data[str(start_node)]["route"].append(backtrace_route(parents, str(neighbor), str(start_node)))
                        data[str(start_node)]["notified_cams"].append(neighbor)
                    elif neighbor not in stack and neighbor not in visited:
                        parents[str(neighbor)] = str(node)
                        stack.append(neighbor)         
    #print("Parents : {}".format(json.dumps(parents, indent=4, sort_keys=True)))
    return data




start_time = time.time()
G = ox.graph_from_point((33.775259139909664, -84.39705848693849), distance = 500, network_type='drive')

# for k,v in G.nodes(data=True):
#     if 'highway' in v and (v["highway"] == "traffic_signals" or v["highway"] == "stop"):
#         v["cam_id"]="cam_" + str(random.randint(1000, 9999))


 

#ox.plot_graph(G)
#print(nx.get_node_attributes(G, list(G.nodes)[0]))

with open("data/cameras.json") as camera_file:
    cameras = json.load(camera_file)

camera_nodes = []
nc=[]

for camera in list(cameras):
    camera_nodes.append(ox.get_nearest_node(G, (float(camera["latitude"]), float(camera["longitude"]))))

for k, v in G.nodes(data=True):
    if k in camera_nodes:
        nc.append('r')
        v["cam_id"] = "cam_"+str(random.randint(1000, 9999))
    else:
        nc.append('b')
    print(v)

#nx.draw(G, node_size = 10, node_color = nc, alpha = 0.5, with_labels = False)

# ox.plot_graph(G, node_color=nc)
# #print(G.edges)
# print("Before removal : " + str(len(G.edges)))


# #remove reverse edges
edges_to_remove = []
already_removed = []
for edge in G.edges:
    u = edge[0]
    v = edge[1]
    for edge in G.edges:
        new_u = edge[0]
        new_v = edge[1]
        if u == new_v and v == new_u and (u, v) not in edges_to_remove:
            edges_to_remove.append((new_u, new_v))


#G.remove_edges_from(edges_to_remove)
# ox.plot_graph(G, node_color=nc)

# #print("After reverse removal : " + str(len(G.edges)))




# #select edge at random for vehicle
#vehicle_edge = random.choice(list(G.edges))
#print("Random vehicle edge : {}".format(vehicle_edge))

vehicles = []
for edge in list(G.edges):
    vehicles.append(edge)

print(vehicles)
ec = ['k' if edge in vehicles else 'b' for edge in G.edges]
notified_cams = dfs(G,vehicles , camera_nodes)
print("Cameras notified: {}".format(json.dumps(notified_cams, indent=4, sort_keys=True)))
route_list=[]
for vehicle, data in notified_cams.items():
    route_list = data["route"]
    ox.plot_graph_routes(G,routes=route_list, node_color=nc, edge_color=ec, node_zorder=3, orig_dest_node_color = ['r', 'k']*len(route_list))
print("--- %s seconds ---" % (time.time() - start_time))
