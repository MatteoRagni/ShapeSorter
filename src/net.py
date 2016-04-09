# Server

import bge
import socket
import json

### Helpers ###

## Handler method
def _position(val):
    if not isinstance(val, list): return False
    if len(val) != 2: return False
    scene = bge.logic.getCurrentScene()
    robot = scene.objects["Robot"]
    robot['x_fin'] = val[0]
    robot['y_fin'] = val[1]
    return True

def _exec_move():
    scene = bge.logic.getCurrentScene()
    robot = scene.objects["Robot"]
    x_pos = robot['x_pos']
    y_pos = robot['y_pos']
    x_fin = robot['x_fin']
    y_fin = robot['y_fin']
    x_err = x_fin - x_pos
    y_err = y_fin - y_pos
    if (x_err**2 + y_err**2) > 1e-2:
        robot.worldPosition[0] += (1 if x_err >= 0 else -1) * 0.02
        robot.worldPosition[1] += (1 if y_err >= 0 else -1) * 0.02
        if robot['Target'] != '':
            target = scene.objects[robot['Target']]
            if target['solved'] == 0:
                target.worldPosition[0] = robot.worldPosition[0]
                target.worldPosition[1] = robot.worldPosition[1]

def _screenshot(val):
    if not isinstance(val, str): return False
    print("Making screenshot in %s" % val)
    bge.render.makeScreenshot("//" + val)
    return True

def _grasp(val):
    if val == 0:
        ((bge.logic.getCurrentController()).owner)['Grasp'] = False
        print("Releasing grasping")
    else:
        ((bge.logic.getCurrentController()).owner)['Grasp'] = True
        print("Trying grasping")
    return True

## Parser method
def _parser(js):
    if 'com' not in js:
        return "Err: missing com"
    if 'val' not in js:
        return "Err: missing val"
    com = js['com']
    val = js['val']
    ret = True
    #############################
    if com == 'position':
        ret = _position(val)
    elif com == 'screenshot':
        ret = _screenshot(val)
    elif com == 'grasp':
        ret = _grasp(val)
    else:
        return "Err: command unknown"
    #############################
    if ret:
        return "ok"
    else:
        return "Err: command %s: %s" % (com, json.dumps(val))

#################################
# Network class
class Server:
    def __init__(self, host='localhost', port=9999):
        self.addr = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(False)
        self.socket.bind(self.addr)

    def handle(self, addr, data):
        print("=" * 20)
        print("from %s: %s" % (addr,data))
        response = self.parser(data)
        print("Response:")
        print(response)
        #resp_text = json.dumps(response)
        #self.socket.sendto(resp_text.encode(), addr)
        return

    def receive(self):
        while True:
            try:
                data, addr = self.socket.recvfrom(1024)
                self.handle(addr, data.decode())
            except socket.error:
                break

    def parser(self, data):
        try:
            _json = json.loads(data)
        except json.decoder.JSONDecodeError:
            print("JSON data not valid")
            return None
        return _parser(_json)

#####################################
# Actually executed commands every frame
server = Server()

def serve(cont):
    cont.owner['x_pos'] = cont.owner.worldPosition[0]
    cont.owner['y_pos'] = cont.owner.worldPosition[1]
    server.receive()
    _exec_move()
