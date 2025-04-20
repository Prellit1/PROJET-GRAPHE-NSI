"""Module donnant des classes et fonctions utiles pour des graphes"""

class Noeud:
    def __init__(self, value, links=None):
        self.value = value
        #self.is_visited = False
        if not links:
            links = []
        self.links = links
        
    def node_linked(self, node):
        """
        ENTREE  : L'objet, un noeud
        SORTIE  : bool
        ROLE    : Renvoie vrai si l'objet a un lien avec l'autre noeud sinon faux
        Version : 2025APR_01 
        """
        for link in self.links:
            if link[0] == node:
                return True
        return False
    
    def parcours_largeur(self, func=lambda node, retval: retval + node.value,
                         base_retval_value=0):
        """
        ENTREE  : L'objet, une fonction (argument : Noeud, valeur retourné par le parcours) , une valeur
        SORTIE  : une valeur
        ROLE    : Pratique un parcours en largeur et applique une fonction a chaque noeud pour une valeur qui est renvoyer
        Version : 2025APR_01 
        """
        file = [self]
        visited = []
        return_value = base_retval_value
        while file:
            node = file.pop(0)
            if node not in visited:
                visited.append(node)
                return_value = func(node, return_value)
                #print(return_value)
                for neighbor_and_dist in node.links:
                    file.append(neighbor_and_dist[0])
        return return_value
    
    def parcours_profondeur_cycle(self, marques: list = None):
        """
        ENTREE  : L'objet, une liste
        SORTIE  : une valeur
        ROLE    : Pratique un parcours en profondeur et renvoie le nombre de cycle compté
        Version : 2025APR_01 
        """
        if not marques:
            marques = []
        marques.append(self)
        #print(sommet)
        cycle = 0
        for sommet_voisin in self.links:
            if sommet_voisin[0] not in marques:
                cycle += sommet_voisin[0].parcours_profondeur_cycle(marques)
            else: 
                cycle += 1
                
        return cycle

    def __repr__(self):
        return str(self.value) + " | " + str(id(self)) + " | " + str(type(self))
    
    
class Graphe:
    def __init__(self, noeud: Noeud):
        self.racine = noeud
        self.liste_noeuds = self.racine.parcours_largeur(lambda node, retval: (retval + [node]), [])

    def parcours_largeur(self, noeud=None,
                         func=lambda node, retval: retval + node.value,
                         base_retval_value=0):

        """
        ENTREE  : L'objet, un noeud (racine de base), une fonction (argument : Noeud, valeur retourné par le parcours) , une valeur
        SORTIE  : une valeur
        ROLE    : Pratique un parcours en largeur a partir du noeud et applique une fonction a chaque noeud pour une valeur qui est renvoyer
        Version : 2025APR_01 
        """              
        if not noeud:
            noeud = self.racine
        self.__init__(noeud)

        return_value = self.racine.parcours_largeur(func, base_retval_value)

        return return_value
    
    def taille(self):
        """
        ENTREE  : L'objet
        SORTIE  : une valeur
        ROLE    : compte le nombre de noeuds dans le graphe
        Version : 2025APR_01 
        """
        self.__init__(self.racine) # on mets a jour le graphe dans le cas ou certaines liaison de noeud sont modifiés
        return len(self.liste_noeuds)
    
    def parcours_profondeur_cycle(self, noeud=None):
        """
        ENTREE  : L'objet, un noeud (racine de base)
        SORTIE  : une valeur
        ROLE    : Pratique un parcours en profondeur a partir d'un noeud et renvoie le nombre de cycle compté
        Version : 2025APR_01 
        """

        if not noeud:
            noeud = self.racine
        self.__init__(noeud)

        retval = self.racine.parcours_profondeur_cycle()
        return retval
    
    def dijkstra(self, node = None):
        """
        ENTREE  : L'objet, un noeud (de base la racine)
        SORTIE  : deux dictionnaire
        ROLE    : Pratique l'algorithme de dijkstra et renvoie la distance et le chemin de chaque noeud a partir du noeud en parametre 
        Version : 2025APR_01 
        """
        if not node or node not in self.liste_noeuds:
            node = self.racine

        distance = {node : 0}
        non_visite = set(self.liste_noeuds)
        chemin = {node: []}

        while non_visite:
            courant = min(non_visite, key=lambda x : distance.get(x, float("inf")))
            non_visite.remove(courant)
            for voisin, poid in courant.links:
                if voisin in non_visite:
                    nouvelle_distance = distance[courant] + poid
                    if nouvelle_distance < distance.get(voisin, float("inf")):
                        chemin[voisin] = chemin[courant] + [courant]
                        distance[voisin] = nouvelle_distance
        for n in chemin:
            chemin[n] += [n]
        return distance, chemin
        
    
    def __repr__(self):
        return str(self.liste_noeuds)