import pygame
from Config_pour_testpygames import *



#initialisation des composants
pygame.init()


#création fenêtre avec display > permet de gérer l'écran / tout ce qui concerne l'écran on passe par pygame.display
window = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))


#création booléen qui représente l'état de la fenêtre : true>ouverte

running = True


#Evenement de fermeture
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
        pygame.draw.rect(window, COULEURS["menu"], pygame.Rect(LARGEUR_GRILLE,0, LARGEUR_MENU, HAUTEUR_MENU))   
        pygame.draw.rect(window, COULEURS["fond"], pygame.Rect(0,0, LARGEUR_GRILLE, HAUTEUR_GRILLE))
    
        pixels = []
        
        for i in range(LIGNE):
            for j in range(COL):
                x = MARG + j*CASE
                y = MARG + i*CASE
                rectangle = pygame.Rect(x,y,CASE,CASE)
                pygame.draw.rect(window, COULEURS["bordure"], rectangle, 1)
    
      
    

    pygame.display.flip()





















