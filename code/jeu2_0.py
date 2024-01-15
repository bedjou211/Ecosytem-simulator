from classes import *
from monde import *
from grille import *
import sys
from config import * 
import math
from decimal import Decimal
import pygame.mixer

class Monde_pygame(Monde):
    def __init__(self,ligne,colonne):
        Monde.__init__(self,ligne,colonne)
        self.screen = pygame.display.set_mode((L_fenetre,H_fenetre))
        self.pixels = []
        self.Plantes_ = pygame.sprite.Group()
        self.points_eau_ = pygame.sprite.Group()
        self.Moutons_ = pygame.sprite.Group()
        self.Lions_ = pygame.sprite.Group()
        
        #initialisation de la grille en background
        self.sprites = self.Plantes +  self.Moutons + self.Lions
        
        # Lors du deplacement d'un animal cet attribut conservera les cases prises par celui-ci
        self.piste_deja = []
        
        self.boutons = []
        
        self.bouts = pygame.sprite.Group()
        self.DELAY = 5
        self.pause_play = False
        
        #initialisation de la grille en interface
        i = 63
        for _ in range(ligne):
            j = 4
            for c in range(colonne):
                rect = pygame.Rect(j,i,10,10)
                pygame.draw.rect(self.screen,(80,41,35),rect)
                self.pixels.append((j,i))
                j += 11
            i += 11
        self.positions = {a:pixel for a,pixel in zip(self.Terrain.cases_libres(),self.pixels)}

        #initialisaton des sources d'eau
        self.sources = [(8,5),(20,20),(45,7),(8,35),(45,45)]
        for centre in self.sources:
            x,y = centre
            eau = Eau(x,y)
            self.points_eau.append(eau)
            self.points_eau_.add(eau)
            self.Terrain.positionner_dans_grille(eau)
            for point in self.Terrain.cases_autour_libres(x,y):
                x,y = point
                eau = Eau(x,y)
                self.points_eau.append(eau)
                self.points_eau_.add(eau)
                self.Terrain.positionner_dans_grille(eau)

        # initialisation des plantes dans le monde
        for _ in range(6):
            x,y = random.choice(self.Terrain.cases_libres())
            plante = random.choice([Plante("foin",2,x,y),Plante("marguerite",1,x,y)])
            self.Terrain.positionner_dans_grille(plante)
            self.Plantes_.add(plante)
            self.Plantes.append(plante)

        # On initialise notre monde à 2 moutons puis on les laisse évouluer
        for _ in range(2):
            x,y = random.choice(self.Terrain.cases_libres())
            mouton = Herbivore("mouton"+str(self.mouton_suivant),20,20,1,x,y)
            self.Moutons_.add(mouton)
            self.Moutons.append(mouton)
            self.Terrain.positionner_dans_grille(mouton)
            self.mouton_suivant += 1

    # Mise à jour de la section statistiques
    def mise_jour_stat(self):
        pygame.draw.rect(self.screen,COULEURS["fond1"],pygame.Rect(x_stat + 80,y_stat + 75,50,30))
        pygame.draw.rect(self.screen,COULEURS["fond1"],pygame.Rect(x_stat + 200,y_stat + 75,50,30))
        nb1 = len(self.Moutons)
        nb2 = len(self.Lions)
        np1 = str(nb1)
        np2 = str(nb2)
        text1 = self.get_font(20).render(np1,True,"green")
        text2 = self.get_font(20).render(np2,True,"red")
        self.screen.blit(text1,(x_stat+93,y_stat+79))
        self.screen.blit(text2,(x_stat+213,y_stat+79))

    # méthode pour accélerer la vitesse du jeu
    def accelerer(self):
        self.DELAY -= 2
        if self.DELAY <= 0 :
            self.DELAY = 0
            
    # Mettre le jeu en pause
    def pause(self):
        self.pause_play = not self.pause_play
    
    def ralentir(self):
        self.DELAY += 2

    def get_font(self,size): 
        return pygame.font.Font("../ressource/font/SIXTY.TTF", size)

    # interaction du jeu avec l'utilisateur et pertubation de l'évolution de la simulation
    def interaction(self):
        self.screen.blit(vitess,(x_infos+20,y_infos+H_infos+20))
        plus1 = Bouton(1,x_infos+100,y_infos+H_infos+20)
        moins1 = Bouton(0,x_infos+200,y_infos+H_infos+20)
        
        self.screen.blit(ad_mout,(x_infos+20,y_infos+H_infos+60))
        plus2 = Bouton(1,x_infos+170,y_infos+H_infos+60)
    
        self.screen.blit(ad_lion,(x_infos+20,y_infos+H_infos+100))
        plus3 = Bouton(1,x_infos+200,y_infos+H_infos+100)

        self.screen.blit(pause_game,(x_infos+20,y_infos+H_infos+140))
        pause1 = Bouton(2,x_infos+200,y_infos+H_infos+140)

        self.boutons = [plus1,plus2,plus3,moins1,pause1]
        for bout in self.boutons:
            self.bouts.add(bout)
            self.bouts.draw(self.screen)
        
    # mise à jour de la section pour les informations sur un élement de la simualtion
    def mise_jour_infos(self,elem):
        pygame.draw.rect(self.screen,"#edd3b6",(x_infos+5,y_infos+30,L_infos,H_infos-30))
        pygame.draw.rect(self.screen,COULEURS["menu"],(x_infos+5,y_infos,L_infos,H_infos),2)
        nom = self.get_font(20).render("N o m : "+elem.nom,True,"brown")
        if isinstance(elem,Animal):
            age = self.get_font(20).render("A g e : "+str(elem.age),True,"brown")
            sex = self.get_font(20).render("S e x e : "+str(elem.sexe),True,"brown")
            energie = self.get_font(20).render("E n e r g i e : "+str(elem.niveau_energie),True,"brown")
        else:
            age = self.get_font(20).render("A g e : - - -",True,"brown")
            sex = self.get_font(20).render("S e x e : - - - ",True,"brown")
            energie = self.get_font(20).render("E n e r g i e : - - - ",True,"brown")
        self.screen.blit(nom,(x_infos+20,y_infos+60))
        self.screen.blit(age,(x_infos+20,y_infos+100))
        self.screen.blit(sex,(x_infos+20,y_infos+140))
        self.screen.blit(energie,(x_infos+20,y_infos+180))

    # test d'un clic sur un animal ou une plante pour afficher ses inforamtions
    def test_clic(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for elem in self.sprites :
                    if elem.rect.collidepoint(event.pos):
                        self.mise_jour_infos(elem)                
                if self.boutons[0].rect.collidepoint(event.pos):
                    self.accelerer()
                elif self.boutons[1].rect.collidepoint(event.pos):
                    self.rajj_mout()
                elif self.boutons[2].rect.collidepoint(event.pos):
                    self.rajj_lion()
                elif self.boutons[3].rect.collidepoint(event.pos):
                    self.ralentir()
                elif self.boutons[4].rect.collidepoint(event.pos):
                    self.pause()
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

    # pertubation du jeu par l'utilisateur en rajoutant un mouton
    def rajj_mout(self):
        x,y = random.choice(self.Terrain.cases_libres())
        mouton = Herbivore("mouton"+str(self.mouton_suivant),10,10,random.choice([1,2]),x,y)
        self.Moutons_.add(mouton)
        self.Moutons.append(mouton)
        self.Terrain.positionner_dans_grille(mouton)
        self.mise_jour_stat()
        self.mouton_suivant += 1
        
    def rajj_lion(self):
        x,y = random.choice(self.Terrain.cases_libres())
        lion = Carnivore("lion"+str(self.lion_suivant),10,10,random.choice([1,2]),x,y)
        self.Lions_.add(lion)
        self.Lions.append(lion)
        self.Terrain.positionner_dans_grille(lion)
        self.mise_jour_stat()
        self.lion_suivant += 1

    # après déplacement d'un animal, cette liste devra etre vider pour etre utilisé par l'animal suivant
    def vider(self):
            self.piste_deja = []
            
    # Méthode d'initialisation des lions
    def init_lions(self):
        for _ in range(3):
            a,b = random.choice(self.Terrain.cases_libres())    
            lion = Carnivore("lion"+str(self.lion_suivant),25,25,1,a,b)
            self.Lions.append(lion)
            self.Lions_.add(lion)
            self.Terrain.positionner_dans_grille(lion)
            self.lion_suivant += 1 
    
    #mise_jour du jeu au cours du deplacement d'un animal

    def mise_jour(self,animal,a,b):
        self.interaction()
        if not self.pause_play :
            self.Terrain.libere_case(animal)
            x,y = animal.position
            self.piste_deja.append((x,y))
            x_,y_ = self.positions[(x,y)]
            rect = pygame.Rect(x_,y_,10,10)
            animal.position = (a,b)
            a_,b_ = self.positions[(a,b)]
            animal.rect = pygame.Rect(a_,b_,10,10)
            self.Terrain.positionner_dans_grille(animal)
            pygame.draw.rect(self.screen,(80,41,35),rect)
            self.sprites = self.Plantes +  self.Moutons + self.Lions
        self.test_clic()
        self.mise_jour_stat()
        
    # méthode pour faire bouger un animal d'une case en fonction de sa destination quand il a soif
    def bouge_pour_boire(self,animal,x,y):
            if not self.Terrain.test_libre(x,y):
                a,b = animal.position
                n_x,n_y = random.choice(self.Terrain.cases_autour_libres(a,b))
                libre = [x for x in self.Terrain.cases_autour_libres(a,b) if x not in self.piste_deja]
                while (len(libre) !=0 and (n_x,n_y) in self.piste_deja) or (n_x,n_y) == (x,y):
                    libre = [x for x in self.Terrain.cases_autour_libres(a,b) if x not in self.piste_deja]
                    n_x,n_y = random.choice(libre)
                self.mise_jour(animal,n_x,n_y)
            else:
                self.mise_jour(animal,x,y)
        

    def bouge_pour_manger(self,animal,x,y):
        if not self.Terrain.test_libre(x,y):
            elem = self.Terrain.grille[x][y]
            test_1 = isinstance(animal,Herbivore) and not isinstance(elem,Plante)
            test_2 = isinstance(animal,Carnivore) and not isinstance(elem,Herbivore)
            if test_1 or test_2:    
                a,b = animal.position
                n_x,n_y = random.choice(self.Terrain.cases_autour_libres(a,b))
                libre = [x for x in self.Terrain.cases_autour_libres(a,b) if x not in self.piste_deja]
                while (len(libre) != 0 and (n_x,n_y) in self.piste_deja) or (n_x,n_y) == (x,y):
                    libre = [x for x in self.Terrain.cases_autour_libres(a,b) if x not in self.piste_deja]
                    n_x,n_y = random.choice(libre)
                    
                self.mise_jour(animal,n_x,n_y)
            else:
                self.mise_jour(animal,x,y)
        else:
            self.mise_jour(animal,x,y)
                    


    #test de collision entre les animaux pour vérifier qu'un animal a manger
    def test_collision(self,animal):
        collision = False
        if isinstance(animal,Herbivore):
            for herbe in self.Plantes_:
                if pygame.sprite.collide_rect(animal,herbe):
                    self.Plantes.remove(herbe)
                    herbe.kill()
                    self.Terrain.libere_case(herbe)
                    collision = True
        else :
            for mouton in self.Moutons_:
                if pygame.sprite.collide_rect(animal,mouton):
                    self.Moutons.remove(mouton)
                    mouton.kill()
                    self.Terrain.libere_case(mouton)
                    collision = True
        return collision
        
                
            
    #déplacement des animaux pour boire et manger
    def deplace_pour_boire(self,animal,a,b):
        x,y = animal.position
        while not(x == a and y == b):        
            if x<a and y<b :
                self.bouge_pour_boire(animal,x+1,y+1)
            elif x<a and y==b:
                self.bouge_pour_boire(animal,x+1,y)
            elif x<a and y>b:
                self.bouge_pour_boire(animal,x+1,y-1)
            elif x>a and y<b:
                self.bouge_pour_boire(animal,x-1,y+1)
            elif x>a and y==b:
                self.bouge_pour_boire(animal,x-1,y)
            elif x>a and y>b:
                self.bouge_pour_boire(animal,x-1,y-1)
            elif x==a and y>b:
                self.bouge_pour_boire(animal,x,y-1)
            elif x==a and y<b:
                self.bouge_pour_boire(animal,x,y+1)
            if nb_occu(x,y,self.piste_deja) == 10 or self.DELAY == 0:
                self.mise_jour(animal,a,b)
            #col = self.test_collision(animal)
            x,y = animal.position
            self.Plantes_.draw(self.screen)
            self.Lions_.draw(self.screen)
            self.Moutons_.draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(self.DELAY)
        self.Terrain.positionner_dans_grille(animal)

    def deplace_pour_manger(self,animal,a,b):
        x,y = animal.position
        col = False
        while not( (x == a and y == b) or col):
            x,y = animal.position
            if x<a and y<b :
                self.bouge_pour_manger(animal,x+1,y+1)
            if x<a and y==b:
                self.bouge_pour_manger(animal,x+1,y)
            if x<a and y>b:
                self.bouge_pour_manger(animal,x+1,y-1)
            if x>a and y<b:
                self.bouge_pour_manger(animal,x-1,y+1)
            if x>a and y==b:
                self.bouge_pour_manger(animal,x-1,y)
            if x>a and y>b:
                self.bouge_pour_manger(animal,x-1,y-1)
            if x==a and y>b:
                self.bouge_pour_manger(animal,x,y-1)
            if x==a and y<b:
                self.bouge_pour_manger(animal,x,y+1)
            if nb_occu(x,y,self.piste_deja) == 10 or self.DELAY == 0:
                self.mise_jour(animal,a,b)
            self.Plantes_.draw(self.screen)
            self.Lions_.draw(self.screen)
            self.Moutons_.draw(self.screen)
            pygame.display.flip()
            col = self.test_collision(animal)
            pygame.time.delay(self.DELAY)
        self.Terrain.positionner_dans_grille(animal)

    # regéneration des plantes
    def generer_plantes(self):
        for _ in range(15):
            x,y = random.choice(self.Terrain.cases_libres())
            plante = random.choice([Plante('foin',2,x,y),Plante('marguerite',1,x,y)])
            self.Plantes_.add(plante)
            self.Plantes.append(plante)
            self.Terrain.positionner_dans_grille(plante)
            self.Plantes_.draw(self.screen)
            self.Plantes_.update()            

    # régulation du monde
    def reguler(self):
        if len(self.Moutons) <= len(self.Lions) + 13 and len(self.Lions) >=3 :
            for _ in range(3):
                lion = random.choice(self.Lions)
                lion.kill()
                x,y = lion.position
                x_,y_ = self.positions[(x,y)]
                self.Lions.remove(lion)
                self.Terrain.libere_case(lion)
                rect = pygame.Rect(x_,y_,10,10)
                pygame.draw.rect(self.screen,(80,41,35),rect)
                

    #définition de l'activité des moutons
    def activite_moutons(self):               
        for animal in self.Moutons:
            # s'il reste peu de plantes, on en rajoute d'autres
            if len(self.Plantes) <= 12 :
                self.generer_plantes()
            # si l'animal a soif, il fait un choix d'un point d'eau et se positionne autour puis s'abreuve
            if animal.soif() and animal.niveau_energie <= 470:
                pt_eau = random.choice(self.points_eau)
                a,b = pt_eau.position
                while len(self.Terrain.cases_autour_libres(a,b)) == 0:
                    pt_eau = random.choice(self.points_eau)
                    a,b = pt_eau.position
                a,b = random.choice(self.Terrain.cases_autour_libres(a,b))
                # on se rassure que la source d'eau n'est pas saturée
                self.deplace_pour_boire(animal,a,b)
                self.vider()
                animal.boire()

            # si l'animal a faim, il choisi une plante et la mange
            if animal.faim() and animal.niveau_energie <= 470 :
                plante = random.choice(self.Plantes)
                a,b = plante.position
                self.deplace_pour_manger(animal,a,b)
                self.vider()
                animal.manger(plante)
            
            # s'il est peut se reproduire, il donne naissance à un nouvel etre qui naitra dans une case autour de lui
            xpos,ypos = animal.position
            
            if animal.peut_dupliquer() and len(self.Terrain.cases_autour_libres(xpos,ypos)) != 0 and len(self.Moutons) < len(self.Lions) + 100:
                x,y = animal.position
                x,y = random.choice(self.Terrain.cases_autour_libres(x,y))
                new_mouton = Herbivore("mouton"+str(self.mouton_suivant),10,10,random.choice([1,2,1,1,1,2]),x,y)
                self.Moutons_.add(new_mouton) #rajout d'un nouveau mouton au sexe aléatoire
                self.Moutons.append(new_mouton)
                self.Terrain.positionner_dans_grille(new_mouton)
                self.mouton_suivant +=1
                animal.niveau_energie -= 150   # énergie dissipée lors de la duplication
            animal.dissipations()


            # en cas de  mort, l'animal est retiré de la grille et de la liste des moutons
            if animal.mort():
                x,y = animal.position
                x_,y_ = self.positions[(x,y)]
                animal.kill()
                self.Moutons.remove(animal)
                self.Terrain.libere_case(animal)
                rect = pygame.Rect(x_,y_,10,10)
                pygame.draw.rect(self.screen,(80,41,35),rect)

            animal.age += 1


            # Le principe d'activité précédent s'appliquera aux lions sauf que cette fois-ci, leur proies seront les moutons

        self.mise_jour_stat()        
    def activite_lions(self):   

        for animal in self.Lions:
            if animal.soif() and animal.niveau_energie <= 480:
                pt_eau = random.choice(self.points_eau)
                a,b = pt_eau.position
                while len(self.Terrain.cases_autour_libres(a,b)) == 0:
                    pt_eau = random.choice(self.points_eau)
                    a,b = pt_eau.position
                a,b = random.choice(self.Terrain.cases_autour_libres(a,b))
                self.deplace_pour_boire(animal,a,b)
                self.vider()
                animal.boire()

            #pour qu'un lion mange, il faudra qu'il existe des moutons
            if animal.faim() and len(self.Moutons)>0 and animal.niveau_energie < 470:        
                mouton = random.choice(self.Moutons)
                
                # un lion ne mangera un animal que si son energie est inférieur à 460 sur 500
                if mouton.niveau_energie <= 490:
                    x,y = mouton.position
                    self.deplace_pour_manger(animal,x,y)
                    self.vider()
                    animal.manger(mouton)
            xpos,ypos = animal.position
            if animal.peut_dupliquer() and len(self.Terrain.cases_autour_libres(xpos,ypos)) != 0 and len(self.Moutons) > len(self.Lions) + 30:
                x,y = animal.position
                x,y = random.choice(self.Terrain.cases_autour_libres(x,y))
                new_lion = Carnivore("lion"+str(self.lion_suivant),10,10,random.choice([1,2,1,1,1,2]),x,y)
                self.Lions_.add(new_lion) #rajout d'un nouveau mouton au sexe aléatoire
                self.Lions.append(new_lion)
                self.Terrain.positionner_dans_grille(new_lion)              
                self.lion_suivant +=1
                animal.niveau_energie -= 130  # énergie dissipée lors de la duplication
            animal.age += 1
            animal.dissipations()
            animal.test_est_vieux()

            
            if animal.mort():
                x,y = animal.position
                x_,y_ = self.positions[(x,y)]
                animal.kill()
                self.Lions.remove(animal)
                self.Terrain.libere_case(animal)
                rect = pygame.Rect(x_,y_,10,10)
                pygame.draw.rect(self.screen,(80,41,35),rect)
            self.mise_jour_stat()
            self.reguler()
def partie():
    monde = Monde_pygame(50,50)
    pygame.init()
    #pygame.mixer.init()
    #son = pygame.mixer.music.load('../ressource/son/son1.wav')
    #pygame.mixer.music.play(10, 0.0)
    running = True
    while running:
        pygame.draw.rect(monde.screen,COULEURS["menu"],(x_stat,y_stat,L_stat,H_stat))
        monde.screen.blit(baniere,(0,0))
        monde.screen.blit(stat,(x_stat + 5 ,y_stat))
        monde.screen.blit(infos,(x_infos + 5,y_infos))
        monde.screen.blit(mouton,(x_stat + 30,y_stat + 75))
        monde.screen.blit(lion,(x_stat + 150, y_stat + 75))

        pygame.draw.rect(monde.screen,"#1a000d",pygame.Rect(x_legend,y_legend,L_legend,H_legend))
        pygame.draw.rect(monde.screen,COULEURS["fond1"],pygame.Rect(x_stat + 80,y_stat + 75,50,30))
        pygame.draw.rect(monde.screen,COULEURS["fond1"],pygame.Rect(x_stat + 200,y_stat + 75,50,30))
        pygame.draw.rect(monde.screen,COULEURS["fond"],(x_monde,y_monde,L_monde+7,H_monde+4),4)
        pygame.draw.rect(monde.screen,COULEURS["menu"],(x_infos+5,y_infos,L_infos,H_infos),2)
        pygame.draw.rect(monde.screen,"#a49ca0",(x_infos+5,y_infos+H_infos+1,L_ajj,H_ajj))
        monde.bouts.draw(monde.screen)
        legends.draw(monde.screen)
        monde.screen.blit(text1,(x_legend +70,y_legend+6))
        monde.screen.blit(text2,(x_legend +70,y_legend+26))
        monde.screen.blit(text3,(x_legend +70,y_legend+46))
        monde.screen.blit(text4,(x_legend +70,y_legend+66))
        monde.mise_jour_stat()    
        monde.activite_moutons()
        # si les moutons ont atteint le nombre de 20, on rajoute 3 lions
        if len(monde.Moutons)<=40 and len(monde.Moutons) >= 20 and len(monde.Lions)==0:
            monde.init_lions()
        monde.activite_lions()
        for group in [monde.Plantes_,monde.Lions_,monde.Moutons_,monde.points_eau_]:
            group.draw(monde.screen)
            group.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
            pygame.display.flip()




    

        

        
        
            
