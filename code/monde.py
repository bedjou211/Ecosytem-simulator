from classes import *
from grille import *
import random

class Monde:
    
    # Les mondes seront spécifiques aux versions du jeux
    
    def __init__(self,ligne,colonne):
        self.Lions = []
        self.lion_suivant = 1
        self.Terrain = Grille_console(ligne,colonne)
        self.Moutons = []
        self.mouton_suivant = 1
        
        self.Plantes = []
        self.points_eau = []

    # Méthode qui initialisera les lions
    def init_lions(self):                                                                 
        pass
    
    #définition de l'ctivité des moutons:
    def activite_moutons(self):
        pass

    #définition de l'activité des lions
    def activite_lions(self):
        pass

    #géneration des plantes
    def generer_plantes(self):
        pass

    def reguler(self):
        pass

            

            
                
        
