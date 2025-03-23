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


