#Objet animal

import pygame

from config import *
class Animal(pygame.sprite.Sprite):
    def __init__(self,nom_animal,degre_de_faim,degre_de_soif,sexe,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.nom = nom_animal
        self.degre_de_faim = degre_de_faim  #niveau de famine (0 à 100)
        self.degre_de_soif = degre_de_soif  #niveau de soif(0 à 100)
        self.vivant = True                  #etat de l'animal(vivant ou mort)
        self.niveau_energie = 250          #l'énergie de l'animal(0 à 500)
        self.sexe = sexe      # sexe pour la reproduction (1 femele et 2 masculin)
        self.age = 0              #utilisation de l'age pour programmer la mort d'un carnivore après une péridode vie
                                  # et pour donner un age à partir du quel un animal pourra se reproduire

        self.position = (x,y)
        
    def __repr__(self):                     # représentation d'un animal
        return self.nom
        
    def boire(self):                        # l'animal bois de l'eau
        self.degre_de_soif += 20
        self.niveau_energie += 45

    def soif(self):
        return self.degre_de_soif < 25  #un animal a soif si son degré de soif est inférieur à 25
    
    def faim(self):
        return self.degre_de_faim < 25  #pareillement pour la famine
    
    def mort(self):
        return self.niveau_energie <= 0 or self.degre_de_faim <= 0 or self.vivant==False   # Un animal devra morrir si son degré de soif ou de faim ou d'energie est à 0
                                                                 # Un animal mourra également s'il a été mangé(herbivore)
                                                                 # Pour un prédateur il mourra après une période d'activité
                                           
    def dissiper_energie(self):
        self.niveau_energie -= 100    # Dissipation de l'energie chez l'animal
    
    def dissiper_eau(self):
        self.degre_de_soif -= 12      # Dissipation d'eau chez cun animal

    def dissiper_aliments(self):      # Dissipation des aliments  
        self.degre_de_faim -= 12
    
    def peut_dupliquer(self):
        pass
        
    def dissipations(self):                                # foctions des dissipations des aliments , eau et energie
        self.dissiper_energie()
        self.dissiper_eau()
        self.dissiper_aliments()
    
#Objet plante
class Plante(pygame.sprite.Sprite):
    def __init__(self,nom_plante,taille,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.nom = nom_plante
        self.taille = taille                # 2 catégories de plantes 
        self.position = (x,y)
        self.image = pygame.image.load('../ressource/images/vert.png')
        self.rect = self.image.get_rect()
        x_,y_ = positions[(x,y)]
        self.rect = self.rect.move(x_,y_)
    def __repr__(self):
        return self.nom




#Objet Herbivore
class Herbivore(Animal):
    def __init__(self,nom_herbivore,degre_de_faim,degre_de_soif,sexe,x,y):
        Animal.__init__(self,nom_herbivore,degre_de_faim,degre_de_soif,sexe,x,y)
        self.image = pygame.image.load('../ressource/images/blanc.png')
        self.rect = self.image.get_rect()
        x_,y_ = positions[(x,y)]
        self.rect = self.rect.move(x_,y_)
    
    def manger(self,plante):
        if(isinstance(plante,Plante)):           # ne mange que des plantes
            if plante.taille == 1 :              # (taille entre 1 et 2) la taille d'un d'une plante définira l'apport énergetique chez l'herbivore 
                self.degre_de_faim += 10
                self.niveau_energie += 80 
            elif plante.taille == 2 :
                self.degre_de_faim += 15
                self.niveau_energie += 120
        else:
            return self.nom_animal + " est un herbivore donc ne mange que des herbes"

    def peut_dupliquer(self):         
        return self.niveau_energie >= 320 and self.sexe == 1  and self.age >= 5  # un herbivore se dupliquera si son sexe est feminin
                                                                                 #et son niveau d'energie est supérieur 300

                                                                                          
#Objet Carnivore
class Carnivore(Animal):
    def __init__(self,nom_carnivore,degre_de_faim,degre_de_soif,sexe,x,y):
        Animal.__init__(self,nom_carnivore,degre_de_faim,degre_de_soif,sexe,x,y)
        self.niveau_energie = 300
        self.image = pygame.image.load('../ressource/images/rouge.png')
        x_, y_ = positions[(x,y)]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x_,y_)
        
    def manger(self,herbivore):
        if isinstance(herbivore,Herbivore):  #Un carnivore ne va manger que des herbivores
            self.degre_de_faim += 25
            self.niveau_energie += 150
            herbivore.vivant = False
        else :
            return self.nom_animal + " est un carnivore donc ne mange que de la viande"

    def test_est_vieux(self):                                                          #programmation de la mort d'un carnivore après une période de vie
        if self.sexe == 1 and self.age == 17:                                          #le sexe feminin aura une durrée de vie plus longue (15 contre 10 pour le male)
            self.vivant = False
        else:
            if self.sexe == 2 and self.age == 12:
                self.vivant = False
            
    def peut_dupliquer(self):         
        return self.niveau_energie >= 315 and self.sexe == 1 and self.age >= 5   #un carnivore se dupliquera si son niveau d'energie est supérieur 320

    def dissiper_energie(self):
        self.niveau_energie -= 95

class Eau(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.position = (x,y)
        self.image = pygame.image.load('../ressource/images/bleu.png')
        self.rect = self.image.get_rect()
        x_,y_ = positions[(x,y)]
        self.rect = self.rect.move(x_,y_)

    def __repr__(self):
        return "eau"
        

""" Elements inactifs """
mouto = Herbivore(" ",0,0,0,0,0)
lio = Carnivore(" ",0,0,0,0,0)
plant = Plante(" ",1,0,0)
eau = Eau(0,0)

mouto.rect = pygame.Rect(x_legend +20,y_legend+7,30,30)
lio.rect = pygame.Rect(x_legend +20,y_legend+27,30,30)
plant.rect = pygame.Rect(x_legend +20,y_legend+47,30,30)
eau.rect = pygame.Rect(x_legend +20,y_legend+67,30,30)

legends = pygame.sprite.Group()
for elem in [mouto,lio,plant,eau]:
    legends.add(elem)


