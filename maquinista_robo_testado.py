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

TENPO_LIMITE = 5

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
        self.inputs = []
        self.pesos = []
        self.bias = 0
        self.output = 0
        self.tempo_decorrido = 0

    def desenhar(self,tela):
        tela.blit(self.img, (self.x, self.y))

    def  andar_frente(self):
        # andar pra frente é incrementar a posição inicial em que o trem é desenhado na tela
        self.x += self.velocidade

    def calcular_output(self):
        # zero o output para poder calcular um novo
        self.output = 0

        # produto vetorial dos inputs com os outputs
        for i in range(len(self.inputs)):
            self.output += self.inputs[i] * self.pesos[i]
        # adiciona o bias só no final, após o produto vetorial estar completo    
        self.output += self.bias
        #lembrando que será uma "reta multidimensional" ax + b (a: pesos, x: inputs, b: bias)
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
# funções

def desenhar_tela(tela, trem, texto_tempo):

    # blit -  "bit block transfer" (transferência de blocos de bits)
    # cópia de uma região de pixels de uma imagem para outra
    # (0,0) -> onde "começa"
    tela.blit(FUNDO_IMG, (0,0))

    tela.blit(texto_tempo, (LARGURA_TELA - texto_tempo.get_width() - 10, 10) )

    trem.desenhar(tela)

    # atualiza a tela
    pygame.display.update()

def rodar_jogo(tela, trem):

    tempo_inicial = time.time()
    while True:

        # verifica se cliquei no X para fechar o jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # encerra todo o código
                sys.exit()

        permitido_andar_frente = 1
        trem.calcular_output()
        if trem.output > 0:

            # caso ao avançar pra frente, o trem passe a tela, então ele já está no limite da tela.
            if trem.x + trem.comprimento + trem.velocidade > LARGURA_TELA:
                # então ele não pode avançar mais
                permitido_andar_frente = 0

            # se for permitido avançar, seja feliz     
            if permitido_andar_frente == 1:
                trem.andar_frente()

        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - tempo_inicial
        texto_tempo = FONT.render(f"{tempo_decorrido:.3f}s", 1, (0,0,0))
        tempo_restante = TENPO_LIMITE - tempo_decorrido

        trem.inputs[0] = tempo_restante

        distancia_fim = LARGURA_TELA - trem.x + trem.comprimento
        trem.inputs[1] = distancia_fim

         # se acabar o tempo ou o trem chegar ao final, 
         # guarda o tempo decorrido,
         # mostra os dados,
         # encerra o programa
        
        trem.tempo_decorrido = tempo_decorrido

        if tempo_restante < 0 or trem.x + trem.comprimento == LARGURA_TELA:

            #trem.tempo_decorrido = tempo_decorrido
            print('------------------------------------------------------------')
            print(f'tempo decorrido: {trem.tempo_decorrido}')
            print('------------------------------------------------------------')

            sys.exit()

        desenhar_tela(tela, trem, texto_tempo)

def inicializar_jogo():

    # define a tela do jogo com as dimensões passadas
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

    # na inicialização dos trens, considero que todos tem o tempo limite para completar a tarefa
    tempo_restante = TENPO_LIMITE - 0

    # a distância inicial é a mesma para todos os trens
    distancia_inicial = LARGURA_TELA - COMPRIMENTO_TREM

    # criando os trem

    # inicializa um vetor para receber os inputs a serem alocados nos trens
    inputs = [0,0]

    # pesos iguais aos do melhor trem 
    pesos = [-15, 12]

    # começa no ponto inicial x = 0
    trem = trem_bala(0)

    inputs[0] = tempo_restante
    inputs[1] = distancia_inicial
    trem.inputs = inputs

    trem.pesos = pesos

    # bias do melhor trem
    bias = 14

    trem.bias = bias

    rodar_jogo(tela, trem)      

def main():

    inicializar_jogo()
#---------------------------------------------------------------------------------------------------------

main()
