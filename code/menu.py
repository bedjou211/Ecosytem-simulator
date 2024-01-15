import pygame, sys
from button import Button
from curve import *
from Config_pour_testpygames import *
from jeu2_0 import Monde_pygame
from jeu2_0 import partie
class Menu:
    def __init__(self):
        self.screen= pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN),pygame.RESIZABLE)
        self.n = pygame.display.set_caption("Écosysteme")
        self.gb = pygame.image.load("../ressource/images/backg.png")

    def get_font(self,size): 
        return pygame.font.Font("../ressource/font/SIXTY.TTF", size)

    def play(self):
        partie() 
    def courbe(self):
        variations_pop()
    def main_menu(self):
        while True:
            self.screen.blit(self.gb, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(75).render("Simulation", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("../ressource/images/button.png"), pos=(640, 250), 
                                text_input="Demarer", font=self.get_font(30), base_color="#d7fcd4", hovering_color="#2a4d42")
            COURBE_BUTTON = Button(image=pygame.image.load("../ressource/images/button.png"), pos=(640, 400), 
                                text_input="Courbe", font=self.get_font(30), base_color="#d7fcd4", hovering_color="#2a4d42")
            QUIT_BUTTON = Button(image=pygame.image.load("../ressource/images/button.png"), pos=(640, 550), 
                                text_input="Quit", font=self.get_font(30), base_color="#d7fcd4", hovering_color="#2a4d42")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, COURBE_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play()
                    if COURBE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.courbe()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

    

if __name__ == '__main__':
    pygame.init()
    menu = Menu()
    menu.main_menu()
    pygame.quit()
