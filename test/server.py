import json
import socket

DATA_FIXED_LENGTH

class Server:
    # Creates a new server with a socket non blocking
    def __init__(host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(False)
        self.socket.bind((host,port))

    def __del__():
        self.socket.close()

    def receive():
        while True
