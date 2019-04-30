class Camera:
    def __init__(self, id, latitude, longitude):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
    
    def join_network(self, socket):
        socket.send_json({"request_type" : "JOIN", "data" : self.get_json_object()})
        return socket.recv_json()
    
    def get_neighbor_cams(self, socket):
        socket.send_json({"request_type" : "GET_NEIGHBOR_CAMS", "data" : self.get_json_object()})
        return socket.recv_json()
    
    def send_heartbeat(self, socket):
        socket.send_json({"request_type" : "ALIVE", "data" : self.get_json_object()})
        return socket.recv_json()
        
    def get_json_object(self):
        dict = {
            "id" : self.id,
            "latitude" : self.latitude,
            "longitude" : self.longitude
        }
        return dict

    