#import socketserver
import socket
import pickle
import json
import bge

#server = None
HOST, PORT = 'localhost', 9999

### Helpers ###
def _parser(js):
    response = {'state': 200, 'message': 'OK'}
    # Initial check on type and target
    if not js:
        response['state'] = 404
        response['error'] = 'Invalid json received'
        return response
    try:
        js['type']
    except (KeyError):
        response['state'] = 404
        response['error'] = 'Missing "type" command in json'
        return response
    try:
        js['target']
    except (KeyError):
        response['state'] = 404
        response['error'] = (
            'Missing "target" result for %s command in json' % js['type'])
        return response
    # Screenshot command handling
    if js['type'].upper() == 'SCREEN':
        print("EXECUTE SCREENSHOT IN LOCATION %s" % (
            "//" + js['target'] + ".png"))
        return response
    # Depth command handling
    elif js['type'].upper() == 'VIEW':
        if js['target'].upper() == "COLOR":
            print("DISABLING DEPTH VIEW")
        elif js['target'].upper() == "DEPTH":
            print("ENABLING DEPTH VIEW")
        else:
            response['state'] = 500
            response['message'] = 'Unkwonw depth bound: must be "0" or "1"'
            return response
    # Moving an object using direct object selection
    elif js['type'].upper() == 'MOVE_OBJ':
        try:
            js['object']
        except (KeyError):
            response['state'] = 500
            response['message'] = 'Object not defined'
            return response
        if not _check_list(js['target'], 3):
            response['state'] = 500
            response[
                'message'] = 'Wrong target (error in vector). Must be [Px, Py, Az]'
            return response
        print("MOVING OBJECT %d IN X = %f, Y = %f, AZ = %f" % (
            js['object'], js['target'][0],  js['target'][1],  js['target'][2]))
    # Moving an object using selection on the screen
    elif js['type'].upper() == 'MOVE_XY':
        try:
            js['object']
        except (KeyError):
            response['state'] = 500
            response['message'] = 'Object not defined'
            return response
        if not _check_list(js['object'], 2):
            response['state'] = 500
            response[
                'message'] = 'Wrong object selection. Must be [X, Y] as pixels on screen'
            return response
        if not _check_list(js['target'], 3):
            response['state'] = 500
            response[
                'message'] = 'Wrong target (error in vector). Must be [Px, Py, Az]'
            return response
        print("MOVING OBJECT [%d, %d] IN X = %f, Y = %f, AZ = %f" % (
            js['object'][0], js['object'][1], js['target'][0],  js['target'][1],  js['target'][2]))
    else:
        response['state'] = 404
        response['error'] = (
            'Unknown "type" = %s command in json' % js['type'])
        return response
    return response

def _check_list(obj, size):
    if not isinstance(obj, list):
        return False
    if not len(obj) == size:
        return False
    return True


### UDP Handler for Server connections ###
#class UDPHandler(socketserver.BaseRequestHandler):
#    def handle(self):
#        response = {'response': 'ok'}
#        data = self.request[0].strip()
#        socket = self.request[1]
#        print("{} wrote:".format(self.client_address[0]))
#        # print(data)
#        response = _parser(json.loads(data.decode()))
#        socket.sendto((json.dumps(response)).encode(), self.client_address)

#def _server():
    #own = (bge.logic.getCurrentController()).owner
    #if 'init' not in own:
    #    own['init'] = True
    #    HOST, PORT = "localhost", 9999
    #    server = socketserver.UDPServer((HOST, PORT), UDPHandler)
    #server.serve_forever()
#    HOST, PORT = "localhost", 9999
#    server = socketserver.UDPServer((HOST, PORT), UDPHandler)
#    server.timeout = 10
#    server.handle_request()

class Server:
    def __init__(self, host = 'localhost', port = 9999):
        self.addr = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(False)
        self.socket.bind(self.addr)

    def handle(self, addr, data):
        response = {'response': 'ok'}
        # print(data)
        response = _parser(json.loads(data.decode()))
        print(response)
#        self.socket.sendto((json.dumps(response)).encode())

    def receive(self):
        while True:
            try:
                data, addr = self.socket.recvfrom(1024)
                self.handle(addr, data)
            except socket.error:
                break
server = Server()
def serve():
    server.receive()
