#---------------------------------------------------------------------------------------------------------
# bibliotecas

import pygame # usada para gerar e manipular as imagens
import sys # usada simplismente para interromper todo o programa
import time # usada para calcular o tempo de execução do game
import random # usada para calcular aleatoriamente os pesos e o bias
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
# constantes

LARGURA_TELA = 1200
ALTURA_TELA = 350

FUNDO_IMG = pygame.image.load('imgs/trem bala fundo.jpg')
TREM_BALA_IMG = pygame.image.load('imgs/trem bala.png')

COMPRIMENTO_TREM = TREM_BALA_IMG.get_width()
ALTURA_TREM = TREM_BALA_IMG.get_height()

QUANTIDADE_TRENS = 2

TENPO_LIMITE = 5

PESO_MINIMO = -30
PESO_MAXIMO = 30
TAXA_MUTACAO_PESOS = 10
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
# classes

class trem_bala:

    # x, y -> posições inicias do trem
    def __init__(self, x, numero, geracao):
        self.img = TREM_BALA_IMG
        self.comprimento = COMPRIMENTO_TREM
        self.altura = ALTURA_TREM
        self.x = x
        self.y = ALTURA_TELA - self.altura - 10
        self.velocidade = 1
        self.numero = numero
        self.geracao = geracao
        self.inputs = []
        self.pesos = []
        self.bias = 0
        self.output = 0

    def desenhar(self,tela):
        tela.blit(self.img, (self.x, self.y))

    def  andar_frente(self):
        # andar pra frente é incrementar a posição inicial em que o trem é desenhado na tela
        self.x += self.velocidade
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
# funções

def desenhar_tela(tela, trens):

    # blit -  "bit block transfer" (transferência de blocos de bits)
    # cópia de uma região de pixels de uma imagem para outra
    # (0,0) -> onde "começa"
    tela.blit(FUNDO_IMG, (0,0))

    for i in range(len(trens)):
        trens[i].desenhar(tela)

    # atualiza a tela
    pygame.display.update()

def rodar_jogo(tela, trens):

    while True:

        # verifica se cliquei no X para fechar o jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # encerra todo o código
                sys.exit()

        for i in range(len(trens)):


            # Keys é um vetor que guardara o estado de todas as teclas permitidas de serem analisadas
            # esse estado será 1 ou 0, para está sendo pressionada ou não está sendo pressionada
            keys = pygame.key.get_pressed()
            
            # variável controle para permitir o trem andar pra frente
            permitido_andar_frente = 1

            # caso o estado da tecla "d" seja 1, então ela está sendo pressionada, logo, podemos avançar
            if keys[pygame.K_d]:

                # caso ao avançar pra frente, o trem passe a tela, então ele já está no limite da tela.
                if trens[i].x + trens[i].comprimento + trens[i].velocidade > LARGURA_TELA:
                    # então ele não pode avançar mais
                    permitido_andar_frente = 0

                # se for permitido avançar, seja feliz     
                if permitido_andar_frente == 1:
                    trens[i].andar_frente()

        # toda vez desenhamos a tela, porque pode ter mudado algo
        desenhar_tela(tela, trens)

def inicializar_jogo():

    # tempo inicial do jogo
    tempo_inicial = time.time()

    # define a tela do jogo com as dimensões passadas
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

    # vetor que receberá todos os trens
    trens = []

    # o tempo atual e o restante precisou serem craidos fora da iteração, pois eles devem ser os mesmos
    # para cada trem
    tempo_atual = time.time()
    tempo_restante = TENPO_LIMITE - tempo_atual

    # a distância inicial é a mesma para todos os trens
    distancia_inicial = LARGURA_TELA - COMPRIMENTO_TREM

     # criando os trens da primeira geração
    for i in range(QUANTIDADE_TRENS):

        # inicializa um vetor vazio para receber os inputs a serem alocados nos trens
        inputs = [0,0]

        # inicializa um vetor vazio para receber os pesos a serem alocados nos trens
        pesos = []

        # todos começam no ponto inicial x = 0
        # o número do trem vai ser i+1 = {1,2,...}
        # os trens inciais são da geração 1
        trem = trem_bala(0,i+1,1)

        inputs[0] = tempo_restante
        inputs[1] = distancia_inicial
        trem.inputs = inputs

        # para cada input deve haver um peso
        # inicialmente eles são gerados aleatoriamente
        for j in range(len(inputs)):
            peso = random.randint(PESO_MINIMO, PESO_MAXIMO)
            pesos.append(peso)

        trem.pesos = pesos

        trens.append(trem)

    rodar_jogo(tela, trens)

        

def main():

    inicializar_jogo()
#---------------------------------------------------------------------------------------------------------

main()
