import pygame
import sys

LARGURA_TELA = 1200
ALTURA_TELA = 350

def desenhar_tela():
    pygame.display.update()

def main():

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        desenhar_tela()

main()