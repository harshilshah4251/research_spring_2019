## Overview
This code implements the automatic static camera topology reorganization algorithm. 

## How this works?
- Start the server using `python3 server.py`.
- Add the camera data of the cameras that must be added to network to [cameras.json](data/cameras.json).
- Run [register_cameras.py](register_cameras.py) to register each camera to the network. Run `python3 register_cameras.py`
- The default map used is the Georgia Tech's map. This can be changed in the [server.py](server.py) file.
- The map is converted into a simplified graph and the registered cameras are basically the nearest nodes on that graph. 
- [server.py](server.py) file contains methods to get neighbor cameras for a given camera, check if the camera is active based on the last heartbeat signal, and register camera to the network.
- [register_cameras.py](register_cameras.py) contains code that reads the cameras from [cameras.json](data/cameras.json) and send heartbeat signal at certain time interval.

## How to interpret the graph?

- Red colored nodes denote the cameras that were added to the network and Blue colored nodes denote the intersection on the road.
- The red highlighted path denotes the path to the neighboring cameras from the selected camera that need to be notified of the vehicle.
- If the neighboring camera becomes inactive, the camera topology will be dynamically changed to find the new neighbors and update the red highlighted path.
- To verify this, use the [cameras_test.json](data/cameras_test.json) file as an input in the [register_cameras.py](register_cameras.py) and run the unchanged version of the code.
- One problem with the code right now is that when the map window is shown on the screen, the background process that sends heartbeat signal to the server stops. Because of this reason, the user needs to close the window and let it reopen automatically to show the updated map after topology change.



