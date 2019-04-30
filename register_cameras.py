# pylint: skip-file

import osmnx as ox
import numpy as np
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import re
import json
import random
ox.config(log_console=True, use_cache=True)
import time
import zmq
from camera import Camera
from threading import Timer



context = zmq.Context()


#  Socket to talk to server
print("Connecting to the server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

cameras = []

with open("data/cameras_test.json") as camera_file:
    cameras_data = list(json.load(camera_file))

for camera_data in cameras_data:
    camera = Camera(camera_data["id"], camera_data["latitude"], camera_data["longitude"])
    cameras.append(camera)
    print(camera.join_network(socket))
    # neighbor_cams = socket.recv_json()
    # print("Cameras notified: {}".format(json.dumps(neighbor_cams, indent=4, sort_keys=True)))
    # message = socket.recv_json()
    # print(message)

# response = cameras[0].get_neighbor_cams(socket)
# print("Cameras notified: {}".format(response))
count = 0



def camera_heartbeat_ticks():
    global count
    #this is hardcoded for testing purposes. You can change this to have all
    # cameras send heartbeat to the server at certain time intervals.
    if count % 2 == 1:
        cameras[0].send_heartbeat(socket)
        cameras[2].send_heartbeat(socket)
        cameras[3].send_heartbeat(socket)
    if count % 2 == 0:
        cameras[0].send_heartbeat(socket)
        cameras[1].send_heartbeat(socket)
        cameras[2].send_heartbeat(socket)
        cameras[3].send_heartbeat(socket)
    response = cameras[0].get_neighbor_cams(socket)
    print("-"*100)
    print("Cameras notified: {}".format(response))
    count += 1


    #last = 2

    #if count > 2:
        #print(cameras[34].get_neighbor_cams(socket))
        # print(cameras[7].get_neighbor_cams(socket))
        # print(cameras[8].get_neighbor_cams(socket))
        #last = 1
    #     if count == 5:
    #         response = cameras[0].get_neighbor_cams(socket)
    #         print("-"*100)
    #         print("Cameras notified: {}".format(response))
    # if count >= 10:
    #     last = 2
    #     if count == 13:
    #         response = cameras[0].get_neighbor_cams(socket)
    #         print("-"*100)
    #         print("Cameras notified: {}".format(response))
    # for camera in cameras:
    #     camera = camera.send_heartbeat(socket)
        
        #print(camera)


class RepeatingTimer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


t = RepeatingTimer(5.0, camera_heartbeat_ticks)
t.start() # every 5 seconds, call camera_heartbeat_tick

# later
#t.cancel() 







#  Do 10 requests, waiting each time for a response
# for request in range(10):
#     print("Sending request %s …" % request)
#     socket.send(b"Hello")

#     #  Get the reply.
#     message = socket.recv()
#     print("Received reply %s [ %s ]" % (request, message))
