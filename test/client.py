import socket
import sys
import json

HOST, PORT = "localhost", 9999
data_list = [
  json.dumps({"a": "4"}),
  json.dumps({"type": "screen"}),
  json.dumps({"type": "screen", "target": "filename"}),                # correct
  json.dumps({"type": "view"}),
  json.dumps({"type": "view", "target": "depth"}),                     # correct
  json.dumps({"type": "view", "target": "color"}),                     # correct
  json.dumps({"type": "view", "target": "lksdnl"}),
  json.dumps({"type": "move_xy", "target": "lksdnl"}),
  json.dumps({"type": "move_xy", "target": [1,2,3]}),                  # correct
  json.dumps({"type": "move_xy", "target": [1,2,3], "object": 4}),
  json.dumps({"type": "move_xy", "target": [1,2,3], "object": [4,5]}), # correct
  json.dumps({"type": "move_obj", "target": "lksdnl"}),
  json.dumps({"type": "move_obj", "target": [1,2,3], "object": 4})      # correct
]
# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
for data in data_list:
    #print(data)
    sock.sendto(bytes(data, "utf-8"), (HOST, PORT))
    received = str(sock.recvfrom(1024), "utf-8")
    print("Received: {}".format(received))
