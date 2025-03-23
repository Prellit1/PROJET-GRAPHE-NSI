""" Fichier créé le 17/09/2024 pour le projet de TG NSI Pacman
    Fait par CAPONE ETHAN

"""

from base import *
    
def loadBG(file):
    """
    Entrée: String representant un fichier image
    Sortie: Surface contenant une image
    Role: renvoie une surface contenant l'arrière plan du menu contenant l'image File
    Version : 1.0
    """

    return pygame.image.load(file)
                        
    

OPT_Y = 400

class Option:
    def __init__(self, x, y, message, cell,id):
        
        self.cell = pygame.image.load(cell)
        self.x = x
        self.y = y
        self.rect = self.cell.get_rect().move(x,y)
        self.message = message
        self.id = id								#une option a un identifiant, une image associé et un  message au programme associé
        
        
    #Vérifie si il est séléctionné puis si il est appuyé et renvoie un message d'action du bouton (si appuyé sinon renvoie un message d'inaction)
    def update(self, selID, eHndl):
        """
        Entrée: selID: entier, eHndl: EventHandler
        Sortie: chaine de character
        Role : Renvoie une chaine de caractere correspondant à si une des variables dans eHndl est vrai et si selID est egal a un attribut de Option
        Version : 1.0
        """
        returnMessage = "OK"
        if selID == self.id:    # si il est selectionné 
            if eHndl.pressed.get(K_RETURN, False): #si Entrée est appuyé
                returnMessage = self.message
            
        return returnMessage
    
    #
    def render(self, fenetre):
        """
        Entrée: fenetre
        Role: permet d'afficher une représentation de l'objet sur l"ecran
        Version : 1.0
        """
        fenetre.blit(self.cell,self.rect)
    
class Menu:
    def __init__(self, lotsOfOptions, selectSprite, fenetre):
        self.options = lotsOfOptions
        self.select = 0
        self.lenOption = len(lotsOfOptions)
        self.window = fenetre
        self.image = pygame.image.load(selectSprite)
        self.rect = self.image.get_rect()
    
    
    #Entrée: le gereur d'évenement (pour les touches)
    #Pas de sortie
    #Role, modifier une variable de l'objet en fonction de la touche appuyé

    def handleKeys(self, eHndl):   #Gère les touches du menu
        """
        De: ETHAN CAPONE
        Entrée: le gereur d'évenement (pour les touches)
        Pas de sortie
        Role, modifier une variable de l'objet en fonction de la touche appuyé et de la longueur d'une liste d'objet d'une autre classe
        
        VERSION : 1.0"""

        if eHndl.pressed.get(K_RIGHT, False):
            self.select = self.select +1
            self.select %= self.lenOption
            
        if eHndl.pressed.get(K_LEFT, False):
            self.select = self.select +1
            self.select %= self.lenOption
       
    def handleOpt(self, eHndl):
        """
        Entrée: eHndl : EventHandler
        Sortie: String
        Role: Renvoie un message correspondant aux messages renvoyés par les appelles de la methode update des objets dans l'attributs options
        Version : 1.0
        """
        returnVal = "OK"
        
        for opt in self.options:
            value = opt.update(self.select, eHndl)
            
            if value != "OK":
                returnVal = value
            
            opt.render(self.window)
        return returnVal
            
            
    def renderSelect(self):
        """
        Role: affiche une icone sur l'ecran représentant la valeur de l'attribut options sélectionné
        Version : 1.0
        """
        self.rect.x = self.options[ self.select ].x - (self.rect.width + 4)
        self.rect.y = self.options[ self.select ].y
        self.window.blit(self.image,self.rect)
        
    def update(self, eHndl):
        """
        Entrée: eHndl : EventHandler
        Sortie : string
        Role: modifie l'attribut de selection en fonction d'un attribut de eHndl, affiche une représentation de la selection et renvoie le message donné par la methode handleOpt
        Version : 1.0
        """
        self.handleKeys(eHndl)
        returnVal = self.handleOpt(eHndl)
        self.renderSelect()
        
                
        return returnVal
                
                
        
        
        
    
    
    

    