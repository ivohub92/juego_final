import pygame, sys
from constantes import *
from data.menu.boton import Boton
from game import *

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("data/menu/Background.png")



def obtener_fuente(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def ingresar_puntaje():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = obtener_fuente(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Boton(image=None, pos=(640, 460), 
                            text_input="REGRESAR", font=obtener_fuente(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.cambiarColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkClick(OPTIONS_MOUSE_POS):
                    menu()

        pygame.display.update()

def puntajes_altos():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = obtener_fuente(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Boton(image=None, pos=(640, 460), 
                            text_input="REGRESAR", font=obtener_fuente(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.cambiarColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkClick(OPTIONS_MOUSE_POS):
                    menu()

        pygame.display.update()

def menu_inicio(display):

    while True:
        display.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXTO = obtener_fuente(100).render("MENU PRINCIPAL", True, "#b68f40")
        MENU_RECT = MENU_TEXTO.get_rect(center=(640, 100))

        BOTON_JUGAR = Boton(image=pygame.image.load("data/menu/Play Rect.png"), pos=(640, 250), 
                            text_input="JUGAR", font=obtener_fuente(75), base_color="#d7fcd4", hovering_color="White")
        BOTON_OPCIONES = Boton(image=pygame.image.load("data/menu/Options Rect.png"), pos=(640, 400), 
                            text_input="PUNTAJES ALTOS", font=obtener_fuente(75), base_color="#d7fcd4", hovering_color="White")
        BOTON_SALIR = Boton(image=pygame.image.load("data/menu/Quit Rect.png"), pos=(640, 550), 
                            text_input="SALIR", font=obtener_fuente(75), base_color="#d7fcd4", hovering_color="White")

        display.blit(MENU_TEXTO, MENU_RECT)

        for botones in [BOTON_JUGAR, BOTON_OPCIONES, BOTON_SALIR]:
            botones.cambiarColor(MENU_MOUSE_POS)
            botones.update(display)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BOTON_JUGAR.checkClick(MENU_MOUSE_POS):
                    Juego.run()
                if BOTON_OPCIONES.checkClick(MENU_MOUSE_POS):
                    puntajes_altos()
                if BOTON_SALIR.checkClick(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

menu()