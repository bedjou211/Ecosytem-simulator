import random
import pygame

from classes import *


class Grille_console:
        def __init__(self,ligne,colonne):
                self.ligne = ligne
                self.colonne = colonne
                self.grille = [["_"]*colonne for _ in range(ligne)]

        def affiche(self):
                for i in range(self.ligne):
                        for j in range(self.colonne):
                                if isinstance(self.grille[i][j],Herbivore):
                                        print("M",end=" ")
                                elif isinstance(self.grille[i][j],Plante)and self.grille[i][j].taille == 1:
                                        print("h1",end=" ")
                                elif isinstance(self.grille[i][j],Plante) and self.grille[i][j].taille==2:
                                        print("h2",end=" ")
                                elif isinstance(self.grille[i][j],Carnivore):
                                        print("L",end=" ")      
                                elif isinstance(self.grille[i][j],Eau):
                                        print("E",end=" ")
                                else :
                                        print(self.grille[i][j],end=" ")
                        print()

        def cases_libres(self):
                cases = []
                for i in range(self.ligne):
                        for j in range(self.colonne):
                                if self.grille[i][j] == "_":
                                        cases.append((i,j))
                return cases

        def positionner_dans_grille(self,elem):
                i,j = elem.position
                self.grille[i][j] = elem

        def cases_autour_libres(self,i,j):
                return [(x,y) for (x,y) in self.cases_libres() if x in [i,i-1,i+1] and y in [j,j-1,j+1]]

        def libere_case(self,elem):
                x,y = elem.position
                self.grille[x][y] = "_"

        def positionner_autour(self,elem,x,y):
                a,b = random.choice(self.cases_autour_libres(x,y))
                self.libere_case(elem)
                elem.position = (a,b)
                self.positionner_dans_grille(elem)

        def deplace_vers(self,elem,x,y):
                self.libere_case(elem)
                elem.position = (x,y)
                self.positionner_dans_grille(elem)
                
        def test_libre(self,x,y):
                return self.grille[x][y] == "_"


def nb_occu(a,b,liste):
        return len([x for x in liste if x==(a,b)])
"""class Grille_Interface:

        def __init__(self):
                self.WIDTH_WIN = WIDTH_WIN
                
                
            def grid(self,WIDTH_WIN,screen):
                i = 0
                while i < WIDTH_WIN:
                    u = 0
                    while u < WIDTH_WIN: 
                        pygame.draw.rect(screen, self.GREEN, pygame.Rect(u,i,40,40)) #50 c'est la largeur d'une seule case
                        u = u + 41
                    i = i + 41
        
        
"""
