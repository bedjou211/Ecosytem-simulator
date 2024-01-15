import pygame, sys
from button import Button
from simulation import *

class Menu:
    
    def __init__(self,WIDTH_WIN,HEIGHT_WIN):
        self.WIDTH_WIN = WIDTH_WIN
        self.HEIGHT_WIN = HEIGHT_WIN
        self.screen= pygame.display.set_mode((self.WIDTH_WIN, self.HEIGHT_WIN),pygame.RESIZABLE)
        self.n = pygame.display.set_caption("Écosysteme")
        self.gb = pygame.image.load("images/backg.png")

    def get_font(self,size): 
        return pygame.font.Font("font/SIXTY.TTF", size)

    def play(self):
        while True:
            S = Simulation()
            PLAY_MOUSE_POS = pygame.mouse.get_pos()
            self.screen.fill("black")
            S.play()

            PLAY_PAUSE = Button(image=pygame.image.load("images/pause.png"), pos=(745, 50),text_input=None, font=self.get_font(0), base_color="White", hovering_color="Green")   #  PROBLEME SUR LE BUTTON et les textes ajouter un background video 
            PLAY_BACK = Button(image=pygame.image.load("images/back.png"), pos=(680, 50),text_input=None, font=self.get_font(0), base_color="White", hovering_color="Green")
            PLAY_PAUSE.update(self.screen)
            PLAY_BACK.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()
        
    def infos(self):
        while True:
            INFOS_MOUSE_POS = pygame.mouse.get_pos()

            self.screen.fill("white")

            INFOS_TEXT0 = self.get_font(30).render("Simulation d’écosystèmes Enonce : L objectif de ce projet est de réaliser une simulation de vie artificielle illustrant les ", True, "Black")
            INFOS_TEXT1 = self.get_font(30).render("équilibres dynamiques présents dans un écosystème où différentes entités participent à une chaîne alimentaire. ", True, "Black")
            INFOS_TEXT2 = self.get_font(30).render(" Il s’agira dans un premier temps de représenter de manière générique ces chaînes alimentaires (ou plus généralement  ", True, "Black")
            INFOS_TEXT3 = self.get_font(30).render("la notion de réseau tropique et d’un moteur simulant les interactions entre ces entités (cycles de reproduction et   ", True, "Black")
            INFOS_TEXT4 = self.get_font(30).render("de consommation) avec une interface graphique. Dans un second temps, il s’agira d’implémenter des fonctionnalités  ", True, "Black")
            INFOS_TEXT5 = self.get_font(30).render("permettant de perturber ou modifier dynamiquement l’écosystème. Une dernière partie du projet sera consacrée à ", True, "Black")
            INFOS_TEXT6 = self.get_font(30).render("un travail expérimental pour déterminer empiriquement les conditions permettant d’atteindre un équilibre ou non.", True, "Black")

            INFOS_RECT0 = INFOS_TEXT0.get_rect(center=(640, 60))
            self.screen.blit(INFOS_TEXT0, INFOS_RECT0)

            INFOS_RECT1 = INFOS_TEXT1.get_rect(center=(640, 100))
            self.screen.blit(INFOS_TEXT1, INFOS_RECT1)

            INFOS_RECT2 = INFOS_TEXT2.get_rect(center=(640, 140))
            self.screen.blit(INFOS_TEXT2, INFOS_RECT2)

            INFOS_RECT3 = INFOS_TEXT3.get_rect(center=(640, 180))
            self.screen.blit(INFOS_TEXT3, INFOS_RECT3)

            INFOS_RECT4 = INFOS_TEXT4.get_rect(center=(640, 220))
            self.screen.blit(INFOS_TEXT4, INFOS_RECT4)

            INFOS_RECT5 = INFOS_TEXT5.get_rect(center=(640, 260))
            self.screen.blit(INFOS_TEXT5, INFOS_RECT5)

            INFOS_RECT6 = INFOS_TEXT6.get_rect(center=(640, 300))
            self.screen.blit(INFOS_TEXT6, INFOS_RECT6)







            INFOS_BACK = Button(image=pygame.image.load("images/back.png"), pos=(640, 460), 
                                text_input=None, font=self.get_font(0), base_color="Black", hovering_color="Green")

            INFOS_BACK.changeColor(INFOS_MOUSE_POS)
            INFOS_BACK.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if INFOS_BACK.checkForInput(INFOS_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()

    def main_menu(self):
        while True:
            self.screen.blit(self.gb, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(75).render("Simulation", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("images/button.png"), pos=(640, 250), 
                                text_input="Demarer", font=self.get_font(30), base_color="#d7fcd4", hovering_color="#2a4d42")
            INFOS_BUTTON = Button(image=pygame.image.load("images/button.png"), pos=(640, 400), 
                                text_input="Infos", font=self.get_font(30), base_color="#d7fcd4", hovering_color="#2a4d42")
            QUIT_BUTTON = Button(image=pygame.image.load("images/button.png"), pos=(640, 550), 
                                text_input="Quit", font=self.get_font(30), base_color="#d7fcd4", hovering_color="#2a4d42")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, INFOS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play()
                    if INFOS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.infos()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    

if __name__ == '__main__':
    pygame.init()
    menu = Menu(1280, 720)
    menu.main_menu()
    pygame.quit()