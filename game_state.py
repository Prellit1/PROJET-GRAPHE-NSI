class State:
    def __init__(self, *args):
        self.states = args

    def get_state(self, msg):
        """
        ENTREE  : L'objet, un string
        SORTIE  : une fonction
        ROLE    : cherche dans l'objet une fonction correspondant au string en parametre
        Version : 2025APR_01 
        """
        func = lambda *_: "Quit" 
        for state in self.states:
            if state[0] == msg:
                func = state[1]
        # j'aurais pu utiliser un dictionnaire
        return func