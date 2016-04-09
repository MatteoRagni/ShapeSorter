# State machine definition

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
        sm.set('Target', '')
        sm.set('Grasp', False)
        sm.next_state = sm.terms('wait')

class MyStateMachine(StateMachine):
    def __init__(self):
        self.terms = {
          'wait': Wait(),
          'move': Move(),
          'grab': Grab()
        }
        State.__init__(self, self.terms['wait'])
        self.set('x_pos', 0.0)
        self.set('y_pos', 0.0)
        self.set('x_end', 0.0)
        self.set('y_end', 0.0)
        self.set('Target', '')
        self.set('Grasp', False)

    def move_x(self, err):
        return

    def move_y(self, err):
        return

    def targets_dist(self):
        return


sm = MyStateMachine()
def execute():
    sm.execute({})
