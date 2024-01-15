import random
from monde import *

class Jeu_console(Monde):
    
    def __init__(self,ligne,colonne):
        Monde.__init__(self,ligne,colonne)

        # initialisation d'un territoire(grille) (on est partie sur un monde ayant une taille d'au moins 25 x 25
        self.Terrain = Grille_console(ligne,colonne)
        
        # initialisation des plantes dans notre monde
        for _ in range(3):
            x,y = random.choice(self.Terrain.cases_libres())
            plante = random.choice([Plante("foin",2,x,y),Plante("marguerite",1,x,y)])
            self.Plantes.append(plante)
            self.Terrain.positionner_dans_grille(plante)
            

        # On initialise notre monde à 2 moutons puis on les laisse évoluer jusqu'à ce qu'ils atteignent 20 et puis on rajoute 3 lions
        for _ in range(2):
            x,y = random.choice(self.Terrain.cases_libres())
            mouton = Herbivore("mouton"+str(self.mouton_suivant),20,20,1,x,y)
            self.Moutons.append(mouton)
            self.Terrain.positionner_dans_grille(mouton)
            self.mouton_suivant += 1
        

        # initilialisation des points d'eau dans la grille
        for _ in range(8):
            point_eau = random.choice(self.Terrain.cases_libres())
            self.points_eau.append(point_eau)
            
        for eau in self.points_eau:
            x,y = eau
            self.Terrain.grille[x][y] = "E"     




    # Méthode qui initialisera les lions
    def init_lions(self):                                         
                                                      
        for _ in range(2):
            a,b = random.choice(self.Terrain.cases_libres())    
            lion = Carnivore("lion"+str(self.lion_suivant),25,25,1,a,b)
            self.Lions.append(lion)
            self.Terrain.positionner_dans_grille(lion)
            self.lion_suivant += 1 
        a,b = random.choice(self.Terrain.cases_libres())    
        lion = Carnivore("lion"+str(self.lion_suivant),25,25,2,a,b)
        self.Lions.append(lion)
        self.Terrain.positionner_dans_grille(lion)
        self.lion_suivant += 1         


    #définition de l'activité des moutons
    def activite_moutons(self):               

        for animal in self.Moutons:

            # s'il reste peu de plantes, on en rajoute d'autres
            if len(self.Plantes) == 3 :
                self.generer_plantes()

            # si l'animal a soif, il fait un choix d'un point d'eau et se positionne autour puis s'abreuve
            if animal.soif() and animal.niveau_energie <= 470:
                pt_eau = random.choice(self.points_eau)
                x,y = pt_eau
                self.Terrain.libere_case(animal)
                # on se rassure que la source d'eau n'est pas saturée
                if len(self.Terrain.cases_autour_libres(x,y)) != 0 :
                    self.Terrain.positionner_autour(animal,x,y)
                    animal.boire()

            # si l'animal a faim, il choisi une plante et la mange
            if animal.faim() and animal.niveau_energie <= 470 :
                plante = random.choice(self.Plantes)
                a,b = plante.position
                self.Terrain.deplace_vers(animal,a,b)
                animal.manger(plante)
                self.Plantes.remove(plante)
            
            
            # s'il est peut se reproduire, il donne naissance à un nouvel etre qui naitra dans une case autour de lui
            xpos,ypos = animal.position
            
            if animal.peut_dupliquer() and len(self.Terrain.cases_autour_libres(xpos,ypos)) != 0:
                x,y = animal.position
                x,y = random.choice(self.Terrain.cases_autour_libres(x,y))
                new_mouton = Herbivore("mouton"+str(self.mouton_suivant),10,10,random.choice([1,2,1,1,1,2]),x,y)
                self.Moutons.append(new_mouton) #rajout d'un nouveau mouton au sexe aléatoire
                self.Terrain.positionner_dans_grille(new_mouton)
                self.mouton_suivant +=1
                animal.niveau_energie -= 150   # énergie dissipée lors de la duplication
            animal.dissipations()

            # si les moutons ont atteint le nombre de 20, on rajoute 3 lions
            if len(self.Moutons)<=40 and len(self.Moutons) >= 20 and len(self.Lions)==0:
                self.init_lions()
            animal.age += 1

            # en cas de  mort, l'animal est retiré de la grille et de la liste des moutons
            if animal.mort():
                self.Moutons.remove(animal)
                self.Terrain.libere_case(animal)


            # Le principe d'activité précédent s'appliquera aux lions sauf que cette fois-ci, leur proies seront les moutons

                
    def activite_lions(self):   

        for animal in self.Lions:
            if animal.soif() and animal.niveau_energie < 480 :        
                x,y = random.choice(self.points_eau)
                self.Terrain.libere_case(animal)
                if len(self.Terrain.cases_autour_libres(x,y)) != 0 :
                    self.Terrain.positionner_autour(animal,x,y)
                    animal.boire()
                    
            #pour qu'un lion mange, il faudra qu'il existe des moutons
            if animal.faim() and len(self.Moutons)>0 and animal.niveau_energie < 470:        
                mouton = random.choice(self.Moutons)
                
                # un lion ne mangera un animal que si son energie est inférieur à 460 sur 500
                if mouton.niveau_energie <= 490:
                    a,b = mouton.position
                    animal.manger(mouton)             
                    self.Terrain.deplace_vers(animal,a,b)
                    self.Moutons.remove(mouton)
            xpos,ypos = animal.position
            if animal.peut_dupliquer() and len(self.Terrain.cases_autour_libres(xpos,ypos)) != 0 and len(self.Moutons) > len(self.Lions) + 30:
                x,y = animal.position
                x,y = random.choice(self.Terrain.cases_autour_libres(x,y))
                new_lion = Carnivore("lion"+str(self.lion_suivant),10,10,random.choice([1,2,1,1,1,2]),x,y)
                self.Lions.append(new_lion) #rajout d'un nouveau mouton au sexe aléatoire
                self.Terrain.positionner_dans_grille(new_lion)              
                self.lion_suivant +=1
                animal.niveau_energie -= 130  # énergie dissipée lors de la duplication
            animal.age += 1
            animal.dissipations()
            animal.test_est_vieux()

            
            if animal.mort():
                self.Lions.remove(animal)
                self.Terrain.libere_case(animal)

            #self.reguler()
            
    def generer_plantes(self):
        for i in range(4):
            if len(self.Terrain.cases_libres()) != 0 :
                x,y = random.choice(self.Terrain.cases_libres())
                plante = random.choice([Plante('foin',2,x,y),Plante('marguerite',1,x,y)])
                self.Plantes.append(plante)
                self.Terrain.positionner_dans_grille(plante)

    def reguler(self):
        if len(self.Moutons) <= len(self.Lions) + 10 and len(self.Lions) >= 3 :
            for _ in range(3):
                lion = random.choice(self.Lions)
                self.Lions.remove(lion)
                self.Terrain.libere_case(lion)

def partie_console():        
    monde = Jeu_console(25,25)
    monde.Terrain.affiche()
    continuer = input("etape suivante (O/N)")
    
    while continuer == "O":
        monde.activite_moutons()
        monde.activite_lions()
        monde.Terrain.affiche()
        print("nombre Moutons {}".format(len(monde.Moutons)))
        print("nombre Lion {} ".format(len(monde.Lions)))
        continuer = input("etape suivante (O/N)")
        
    
