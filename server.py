# pylint: skip-file
import osmnx as ox
import numpy as np
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import re
import json
import random
ox.config(log_console=False, use_cache=True)
import time
import zmq
from datetime import datetime
from threading import Timer

class RepeatingTimer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


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
        data[str(start_node)] = {"neighbor_cams" :[]}  
        #print(list(G.neighbors(start_node)))
        stack.append(start_node)
        while len(stack) != 0:
            node = stack.pop()
            if node not in visited:
                visited.append(node)
                #print(list(G.neighbors(node)))
                print("NODe " + str(node))
                custom_neighbors = list(G.neighbors(node))
                print(custom_neighbors)
                for neighbor in custom_neighbors:
                    #print(neighbor)
                    if neighbor in camera_nodes.values():
                        camera_id = list(camera_nodes.keys())[list(camera_nodes.values()).index(neighbor)]
                        camera = list(filter(lambda list_camera: list_camera['id'] == camera_id, cameras))[0]
                        #print(camera)
                        if "is_active" not in camera or "is_active" in camera and camera["is_active"] is not False:
                            parents[str(neighbor)] = str(node)
                            data[str(start_node)]["neighbor_cams"].append({"cam_id" : neighbor, "route": backtrace_route(parents, str(neighbor), str(start_node))})
                        else:
                            parents[str(neighbor)] = str(node)
                            stack.append(neighbor)   

                            #print(custom_neighbors)
                    elif neighbor not in stack and neighbor not in visited:
                        parents[str(neighbor)] = str(node)
                        stack.append(neighbor)         
    #print("Parents : {}".format(json.dumps(parents, indent=4, sort_keys=True)))

    labels = [list(camera_nodes.keys())[list(camera_nodes.values()).index(node)] if node in camera_nodes.values() else "" for node in G.nodes]
    nc = ['r' if node in camera_nodes.values() else 'b' for node in G.nodes]
    route_list = [neighbor_cam["route"] for neighbor_cam in data[str(start_node)]["neighbor_cams"]]
    ox.plot_graph_routes(G,routes=route_list, node_color=nc,node_zorder=3, orig_dest_node_color = ['r', 'k']*len(route_list))
    print(camera_nodes.values())
    

    

    return data

def add_camera_to_network(camera):
    print("Received join request from: %s" % camera["id"])
    if camera["id"] not in camera_nodes:
        nearest_node = ox.get_nearest_node(G, (float(camera["latitude"]), float(camera["longitude"])))
        print("Nearest node on map: {}".format(nearest_node))
        camera_nodes[camera["id"]] = nearest_node
        cameras.append(camera)
        return {"response" : "{} added successfully".format(camera["id"])}
    else:
        return {"response" : "{} already part of network".format(camera["id"])}


def get_neighbor_cams(camera):
    print("Received neighbor request from: %s" % camera["id"])
    connected_edges = [(u,v,k) for u,v,k in G.edges if v == camera_nodes[camera["id"]]]
    #print("Connected edges: {}".format(connected_edges))
    neighbor_cams = dfs(G,connected_edges, camera_nodes)
    


    return {"response" : neighbor_cams}
def alive_check(camera):
    index_of_camera = cameras.index(list(filter(lambda list_camera: list_camera['id'] == camera['id'],cameras))[0])
    cameras[index_of_camera]["last_heartbeat_check"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return cameras[index_of_camera]
def check_for_alive_cameras():
    for camera in cameras:
        if "last_heartbeat_check" in camera:
            duration_since_last_heartbeat = datetime.now() - datetime.strptime(camera["last_heartbeat_check"], "%Y-%m-%d %H:%M:%S")
            if duration_since_last_heartbeat.seconds > 10:
                camera["is_active"] = False
                print("{} DIED".format(camera["id"]))
            else:
                camera["is_active"] = True
                print("{} ALIVE".format(camera["id"]))


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

G = ox.graph_from_point((33.775259139909664, -84.39705848693849), distance = 500, network_type='drive')

camera_nodes = {}
cameras = []


t = RepeatingTimer(5.0, check_for_alive_cameras)
t.start()




while True:
    #receive join request from camera
    message = socket.recv_json()
    if message["request_type"] == "JOIN":
        response = add_camera_to_network(message["data"])
        socket.send_json(response)
    elif message["request_type"] == "GET_NEIGHBOR_CAMS":
        response = get_neighbor_cams(message["data"])
        socket.send_json(response)
    elif message["request_type"] == "ALIVE":
        response = alive_check(message["data"])
        socket.send_json(response)
    else:
        socket.send_json({"response" : "Invalid request"})
    

