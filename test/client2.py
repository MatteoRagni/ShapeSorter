# Orthographic view client test

import socket
import sys
import json

HOST, PORT = "localhost", 9999
data_list = [
  json.dumps({"a": "4"}),
  json.dumps({"com": "screenshot"}),
  json.dumps({"com": "screenshot", "val": "test_image"}),                # correct
  json.dumps({"com": "position", "val": "lksdnl"}),
  json.dumps({"com": "position", "val": [0,0,0,0]}),
  json.dumps({"com": "position", "val": [1,1]}),                       #
  json.dumps({"com": "grasp", "val": [1,2,3]}),
  json.dumps({"com": "grasp", "val": "fskdjn"}),
  json.dumps({"com": "grasp", "val": 0}),                              # correct
  json.dumps({"com": "grasp", "val": 1})                               # correct
]
# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
for data in data_list:
    print(data)
    sock.sendto(bytes(data, "utf-8"), (HOST, PORT))
    input("Press a key to continue...")
