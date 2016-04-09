# Server

import bge
import socket
import json

### State Machine ###


class StateMachine:
    def __init__(self, default_state):
        self.states       = {} # questo sara da eliminare
        self.active_state = default_state
        self.next_state   = self.active_state

    def set(self, name, value):
        self.states[name] = value # questo sara da sostituire

    def get(self, name):
        return self.states[name] # questo sara da sostituite

    def activate(self):
        if self.next_state != self.active_state:
            self.active_state.exit(self, param)
            self.active_state = self.next_state
            self.active_state.enter(self, param)

    def execute(self, param):
        self.active_state.loop(self, param)

class State:
    def __init__(self, name):
        self.name = name

    def name(self):
        return self.name

    def enter(self, sm, param):
        return

    def loop(self, sm, param):
        return

    def exit(self, sm, param):
        return

# State machine particular
class Wait(State):
    def __init__(self):
        State.__init__(self, 'wait')

    def loop(self, sm, param):
        e_x = sm.get('x_fin') - sm.get('x_pos')
        e_y = sm.get('y_fin') - sm.get('y_pos')
        if (e_x**2 + e_y**2) > 0.01:
            sm.next_state = sm.terms['move']

class Move(State):
    def __init__(self):
        State.__init__(self, 'move')

    def loop(self, sm, param):
        e_x = sm.get('x_fin') - sm.get('x_pos')
        e_y = sm.get('y_fin') - sm.get('y_pos')
        sm.move_x(e_x)
        sm.move_y(e_y)
        if (e_x**2 + e_y**2) < 0.01: # POSITION ERROR
            sm.next_state = sm.terms['wait']

class Grab(State):
    def __init__(self):
        State.__init__(self, 'grab')

    def enter(self, sm, param):
        sm.set('Target', targets_dist())
        sm.next_state = sm.terms('wait')

class Ungrab(State):
    def __init__(self):
        State.__init__(self, 'ungrab')

    def enter(self, sm, param):
        sm.ungrasp()
        sm.next_state = sm.terms('wait')

class MyStateMachine(StateMachine):
    def __init__(self):
        self.terms = {
          'wait': Wait(),
          'move': Move(),
          'grab': Grab(),
          'ungrab': Ungrab()
        }
        self.scene = bge.logic.getCurrentScene()
        self.ref = self.scene.objects['Robot']
        self.get('x_pos')
        self.get('y_pos')
        self.set('x_fin', self.get('x_pos'))
        self.set('y_fin', self.get('y_pos'))
        self.set('Target', '')
        self.set('Grasp', False)
        self.active_state = self.terms['wait']
        self.next_state = self.active_state

    def set(self, name, val):
        self.ref[name] = val

    def get(self, name):
        return self.ref[name]

    def move_dir(self, no, err):
        move = (1 if err >= 0 else -1) * 0.1
        if self.get('Target') != '':
            obj = self.scene.objects[self.get('Target')]
            if obj['solved'] == 0:
                obj.worldPosition[no] += move
        self.ref.worldPosition[no] += move

    def move_x(self, err):
        self.move_dir(0, err)

    def move_y(self, err):
        self.move_dir(1, err)

    def grasp(self):
        set('Grasp', True)

    def ungrasp(self):
        set('Grasp', False)
        set('Target', '')

    def execute(self, param):
        self.set('x_pos', self.ref.worldPosition[0])
        self.set('y_pos', self.ref.worldPosition[1])
        self.ref['state_name'] = self.active_state.name
        self.active_state.loop(self, param)

## Handler method
def _position(val, sm):
    if not isinstance(val, list): return False
    if len(val) != 2: return False
    scene = bge.logic.getCurrentScene()
    robot = scene.objects["Robot"]
    robot['x_fin'] = val[0]
    robot['y_fin'] = val[1]
    return True

def _screenshot(val, sm):
    if not isinstance(val, str): return False
    print("Making screenshot in %s" % val)
    bge.render.makeScreenshot("//" + val)
    return True

def _grasp(val, sm):
    if val == 0:
        sm.next_state = sm.terms['grab']
    else:
        sm.next_state = sm.terms['ungrab']
    return True

## Parser method
def _parser(js, sm):
    if 'com' not in js:
        return "Err: missing com"
    if 'val' not in js:
        return "Err: missing val"
    com = js['com']
    val = js['val']
    ret = True
    #############################
    if com == 'position':
        ret = _position(val, sm)
    elif com == 'screenshot':
        ret = _screenshot(val, sm)
    elif com == 'grasp':
        ret = _grasp(val, sm)
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
    def __init__(self,state_machine, host='localhost', port=9999):
        self.addr = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(False)
        self.socket.bind(self.addr)
        self.sm = state_machine

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
        return _parser(_json, self.sm)

#####################################
# Actually executed commands every frame
state_machine = MyStateMachine()
server = Server(state_machine)

def serve():
    state_machine.execute({})
    server.receive()
