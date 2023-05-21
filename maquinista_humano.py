#---------------------------------------------------------------------------------------------------------
# bibliotecas

import pygame # usada para gerar e manipular as imagens
import sys # usada simplismente para interromper todo o programa
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
# constantes

LARGURA_TELA = 1200
ALTURA_TELA = 350

FUNDO_IMG = pygame.image.load('imgs/trem bala fundo.jpg')
TREM_BALA_IMG = pygame.image.load('imgs/trem bala.png')

COMPRIMENTO_TREM = TREM_BALA_IMG.get_width()
ALTURA_TREM = TREM_BALA_IMG.get_height()
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
# funções

def desenhar_tela(tela):

    # blit -  "bit block transfer" (transferência de blocos de bits)
    # cópia de uma região de pixels de uma imagem para outra
    tela.blit(FUNDO_IMG, (0,0))
    tela.blit(TREM_BALA_IMG, (LARGURA_TELA - COMPRIMENTO_TREM, ALTURA_TELA - ALTURA_TREM - 10))

    # atualiza a tela
    pygame.display.update()

def main():

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        desenhar_tela(tela)
#---------------------------------------------------------------------------------------------------------

main()
