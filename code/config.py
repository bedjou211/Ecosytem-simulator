import pygame
import sys


""" POSITIONS DU MONDE ."""
pygame.init()

pixels = []
cases = []
ligne = 50
colonne = 50
i = 63
i_ = 0

for _ in range(ligne):
    j = 4
    j_ = 0
    for __ in range(colonne-1,colonne*2):
        pixels.append((j,i))
        cases.append((i_,j_))
        j += 11
        j_ += 1
    i += 11
    i_ += 1
positions = {a:pixel for a,pixel in zip(cases,pixels)}


""" images de description de la fenetre """



#self.window = pygame.display.set_mode((L_fenetre,H_fenetre))
baniere = pygame.image.load('../ressource/images/titre.png')
stat = pygame.image.load('../ressource/images/stat.png')
infos = pygame.image.load('../ressource/images/infos.png')
lion = pygame.image.load('../ressource/images/lion.png')
mouton = pygame.image.load('../ressource/images/mouton.png')
lion = pygame.image.load('../ressource/images/lion.png')
plus = pygame.image.load("../ressource/images/plus.png")
moins = pygame.image.load("../ressource/images/moins.png")
pauseplay = pygame.image.load("../ressource/images/pause.png")
def get_font(size): 
    return pygame.font.Font("../ressource/font/SIXTY.TTF", size)


vitess = get_font(20).render("Vitesse",True,"brown")
ad_mout = get_font(20).render("Ajouter 1 mouton",True,"brown")
ad_lion = get_font(20).render("Ajourter 1 lion",True,"brown")
pause_game = get_font(20).render("Faire une pause/jouer",True,"brown")

text1 = get_font(15).render("M o u t o n",True,"brown")
text2 = get_font(15).render("L i o n",True,"brown")
text3 = get_font(15).render("P l a n t e",True,"brown")
text4 = get_font(15).render("E a u",True,"brown")
        
class Bouton(pygame.sprite.Sprite):
    def __init__(self,typ,x,y):
        pygame.sprite.Sprite.__init__(self)
        if typ == 1 :
            self.image = plus
        elif typ == 0 :
            self.image = moins
        else :
            self.image = pauseplay
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x,y)


"""CONFIGURATION MONDE"""
CASE = 10
COL = 50
LIGNE = 50
MARG = 1

H_baniere = 50

L_monde = COL*(CASE+1) + 1
H_monde = LIGNE*(CASE+1) + 5
x_monde = 0
y_monde = 58

L_stat = 315
H_stat = 150
x_stat = L_monde + 2
y_stat = y_monde 

L_infos = L_stat
H_infos = 300
x_infos = x_stat
y_infos = y_stat + H_stat

L_ajj = L_stat
H_ajj = 175


H_legend = 80
L_legend = int(L_monde/2)
x_legend = 140
y_legend = y_monde + H_monde + 5

H_fenetre = H_baniere + H_monde + 100
L_fenetre = L_monde + L_stat


COULEURS = {"fond":pygame.Color("cyan"), "menu":pygame.Color("#a0068c"),"bordure":pygame.Color("pink"),"fond1":pygame.Color("white")}

""" animaux pour la légende """


