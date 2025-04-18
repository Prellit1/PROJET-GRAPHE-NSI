class State:
    def __init__(self, *args):
        self.states = args

    def get_state(self, msg):
        func = lambda *_: "Quit" 
        for state in self.states:
            if state[0] == msg:
                func = state[1]
        return func