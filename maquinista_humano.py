#---------------------------------------------------------------------------------------------------------
# bibliotecas

import pygame # usada para gerar e manipular as imagens
import sys # usada simplismente para interromper todo o programa
import time # usada para calcular o tempo de execução do game
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
# constantes

LARGURA_TELA = 1200
ALTURA_TELA = 350

FUNDO_IMG = pygame.image.load('imgs/trem bala fundo.jpg')
TREM_BALA_IMG = pygame.image.load('imgs/trem bala.png')

COMPRIMENTO_TREM = TREM_BALA_IMG.get_width()
ALTURA_TREM = TREM_BALA_IMG.get_height()

pygame.font.init()
FONT = pygame.font.SysFont('arial', 25)
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
# classes

class trem_bala:

    # x, y -> posições inicias do trem
    def __init__(self, x):
        self.img = TREM_BALA_IMG
        self.comprimento = COMPRIMENTO_TREM
        self.altura = ALTURA_TREM
        self.x = x
        self.y = ALTURA_TELA - self.altura - 10
        self.velocidade = 1

    def desenhar(self,tela):
        tela.blit(self.img, (self.x, self.y))

    def  andar_frente(self):
        # andar pra frente é incrementar a posição inicial em que o trem é desenhado na tela
        self.x += self.velocidade
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
# funções

def desenhar_tela(tela, trem_bala, texto_tempo):

    # blit -  "bit block transfer" (transferência de blocos de bits)
    # cópia de uma região de pixels de uma imagem para outra
    # (0,0) -> onde "começa"
    tela.blit(FUNDO_IMG, (0,0))

    trem_bala.desenhar(tela)
    tela.blit(texto_tempo, (LARGURA_TELA - texto_tempo.get_width() - 10, 10) )

    # atualiza a tela
    pygame.display.update()

def main():

    # define a tela do jogo com as dimensões passadas
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

    trem_bala1 = trem_bala(0)

    tempo_inicial = time.time()
    tempo_atual = tempo_inicial
    tempo_decorrido = tempo_atual - tempo_inicial
    while True:

        # verifica se cliquei no X para fechar o jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # encerra todo o código
                sys.exit()

        # Keys é um vetor que guardara o estado de todas as teclas permitidas de serem analisadas
        # esse estado será 1 ou 0, para está sendo pressionada ou não está sendo pressionada
        keys = pygame.key.get_pressed()
        
        # variável controle para permitir o trem andar pra frente
        permitido_andar_frente = 1

        # caso o estado da tecla "d" seja 1, então ela está sendo pressionada, logo, podemos avançar
        if keys[pygame.K_d]:

            # caso ao avançar pra frente, o trem passe a tela, então ele já está no limite da tela.
            if trem_bala1.x + trem_bala1.comprimento + trem_bala1.velocidade > LARGURA_TELA:
                 # então ele não pode avançar mais
                 permitido_andar_frente = 0

            # se for permitido avançar, seja feliz     
            if permitido_andar_frente == 1:
                trem_bala1.andar_frente()    
        
        if trem_bala1.x + trem_bala1.comprimento < LARGURA_TELA:
            tempo_atual = time.time()

        tempo_decorrido = tempo_atual - tempo_inicial
        texto_tempo = FONT.render(f"{tempo_decorrido:.3f}s", 1, (0,0,0))

        # toda vez desenhamos a tela, porque pode ter mudado algo
        desenhar_tela(tela, trem_bala1, texto_tempo)
#---------------------------------------------------------------------------------------------------------

main()
