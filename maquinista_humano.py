import pygame
import sys

LARGURA_TELA = 1200
ALTURA_TELA = 350

FUNDO_IMG = pygame.image.load('imgs/trem bala fundo.jpg')

def desenhar_tela(tela):

    tela.blit(FUNDO_IMG, (0,0))
    pygame.display.update()

def main():

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        desenhar_tela(tela)

main()