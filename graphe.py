class GrapheLs:
    def __init__(self):
        #self.sommets = sommets
        self.dict = dict()

    def ajouter_noeud(self,n):
        self.dict[n] = {}

    def ajouter_arete(self, x, y, dist):
        if x in self.dict:
            self.dict[x][y] = dist

        else:
            self.dict[x] = {y: dist}

    def parcours_profondeur(self, sommet, marques=None):
        if not marques:
            marques = []
        marques.append(sommet)
        #print(sommet)
        for sommet_voisin in self.dict[sommet]:
            if sommet_voisin[0] not in marques:
                self.parcours_profondeur(sommet_voisin[0], marques)

    def parcours_largeur(self, sommet):
        visite = []
        file = [sommet]
        while file:
            noeud = file.pop(0)
            if noeud not in visite:
                visite.append(noeud)
                #print(noeud)
                if self.dict[noeud]:
                    file.extend(self.dict[noeud]["node"])


class Noeud:
    def __init__(self, value, coords, links = []):
        self.value = value
        self.is_visited = False
        self.coords = coords
        self.links = links

    def parcours_largeur(self, func = lambda node, retval: retval + node.value, base_retval_value =0):
        visite = []
        file = [self]
        return_value = base_retval_value
        while file:
            node = file.pop(0)
            return_value = func(node, return_value)
            for neighbor_and_dist in self.links:
                if not neighbor_and_dist[0].is_visited:
                    file.append(neighbor_and_dist[0])
            node.is_visited = True
        return return_value
    

class Graphe:
    def __init__(self, noeud: Noeud):
        self.racine = noeud
        self.liste_noeuds = self.racine.parcours_largeur(lambda node, retval: retval+[node], [])

    def parcours_largeur(self, noeud = None, func = lambda node, retval: retval + node.value, base_retval_value =0):
        if not noeud:
            noeud = self.racine
        self.__init__(noeud)
        return self.racine.parcours_largeur(func, base_retval_value)
    

        