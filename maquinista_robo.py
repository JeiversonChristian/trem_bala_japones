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

QUANTIDADE_TRENS = 5

TENPO_LIMITE = 5

PESO_MINIMO = -30
PESO_MAXIMO = 30
TAXA_MUTACAO_PESOS = 10

BIAS_MINIMO = -15
BIAS_MAXIMO = 15
TAXA_MUTACAO_BIAS = 5

MAX_GERACOES = 5

pygame.font.init()
FONT = pygame.font.SysFont('arial', 25)
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
        self.tempo_decorrido = 0

    def desenhar(self,tela):
        tela.blit(self.img, (self.x, self.y))
        texto_tempo_trem = FONT.render(f"{self.tempo_decorrido:.3f}s", 1, (0,0,0))
        tela.blit(texto_tempo_trem, (self.x + COMPRIMENTO_TREM - texto_tempo_trem.get_width(), self.y -  texto_tempo_trem.get_height()) )

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

def desenhar_tela(tela, trens, texto_tempo):

    # blit -  "bit block transfer" (transferência de blocos de bits)
    # cópia de uma região de pixels de uma imagem para outra
    # (0,0) -> onde "começa"
    tela.blit(FUNDO_IMG, (0,0))

    tela.blit(texto_tempo, (LARGURA_TELA - texto_tempo.get_width() - 10, 10) )

    for i in range(len(trens)):
        trens[i].desenhar(tela)

    # atualiza a tela
    pygame.display.update()

def rodar_jogo(tela, trens, geracao):

    # vairavel para varrer todos os trens
    num_trem = 0

    # variável de controle para verificar quando muda de trem
    mudou_trem = True

    # variável que guadará o melhor trem de cada geração
    melhor_trem = trens[0]

    # o número da geração será atualizado depois, mas precisa ser definido aqui
    geracao = geracao

    while True:

        # verifica se cliquei no X para fechar o jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # encerra todo o código
                sys.exit()

        if mudou_trem == True:
            # cada trem tem o seu próprio tempo
            tempo_inicial = time.time()
            mudou_trem = False

        permitido_andar_frente = 1
        trens[num_trem].calcular_output()
        if trens[num_trem].output > 0:

            # caso ao avançar pra frente, o trem passe a tela, então ele já está no limite da tela.
            if trens[num_trem].x + trens[num_trem].comprimento + trens[num_trem].velocidade > LARGURA_TELA:
                # então ele não pode avançar mais
                permitido_andar_frente = 0

            # se for permitido avançar, seja feliz     
            if permitido_andar_frente == 1:
                trens[num_trem].andar_frente()

        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - tempo_inicial
        texto_tempo = FONT.render(f"{tempo_decorrido:.3f}s", 1, (0,0,0))
        tempo_restante = TENPO_LIMITE - tempo_decorrido

        trens[num_trem].inputs[0] = tempo_restante

        distancia_fim = LARGURA_TELA - trens[num_trem].x + trens[num_trem].comprimento
        trens[num_trem].inputs[1] = distancia_fim

        trens[num_trem].tempo_decorrido = tempo_decorrido

         # se acabar o tempo ou o trem chegar ao final, muda o trem
        if tempo_restante < 0 or trens[num_trem].x + trens[num_trem].comprimento == LARGURA_TELA:
            
            #trens[num_trem].tempo_decorrido = tempo_decorrido
            
            # guardar o melhor trem

            distancia_trem_atual = LARGURA_TELA - trens[num_trem].x + trens[num_trem].comprimento
            distancia_melhor_trem = LARGURA_TELA - melhor_trem.x + melhor_trem.comprimento

            if distancia_trem_atual <= distancia_melhor_trem and trens[num_trem].tempo_decorrido <= melhor_trem.tempo_decorrido:
                melhor_trem = trens[num_trem]

            num_trem += 1
            mudou_trem = True

        # quero que atualize a tela para cada trem, um de cada vez
        desenhar_tela(tela, trens, texto_tempo)

        if num_trem >= len(trens):

            print('------------------------------------------------------------')
            print(f'melhor trem da geração {geracao}')
            #print(f'geração originária: {melhor_trem.geracao}')
            print(f'número do trem: {melhor_trem.numero}')
            print(f'pesos do trem: {melhor_trem.pesos}')
            print(f'Bias do trem: {melhor_trem.bias}')
            print(f'tempo decorrido: {melhor_trem.tempo_decorrido}')
            print('------------------------------------------------------------')

            # mudar de geracao
            geracao += 1

            # limitando o número de gerações que serão criadas
            if geracao > MAX_GERACOES:
                sys.exit()

            # o número do melhor trem será 1, porque ele será o primeiro da próxima geração
            melhor_trem.numero = 1

            reinicializar_jogo(tela, geracao, melhor_trem)

def reinicializar_jogo(tela, geracao, melhor_trem):

    # vetor que receberá todos os trens
    trens = []

    # na inicialização dos trens, considero que todos tem o tempo limite para completar a tarefa
    tempo_restante = TENPO_LIMITE - 0

    # a distância inicial é a mesma para todos os trens
    distancia_inicial = LARGURA_TELA - COMPRIMENTO_TREM

    # os trens agora são da geração nova
    geracao = geracao

    # criando os trens da nova geração
    
    # o melhor trem da geração passada será o primeiro da nova geração
    melhor_trem.inputs[0] = tempo_restante
    melhor_trem.inputs[1] = distancia_inicial
    melhor_trem.x = 0
    trens.append(melhor_trem)

    for i in range(QUANTIDADE_TRENS -1):

        # inicializa um vetor para receber os inputs a serem alocados nos trens
        inputs = [0,0]

        # inicializa um vetor vazio para receber os pesos a serem alocados nos trens
        pesos = []

        # todos começam no ponto inicial x = 0
        # o número do trem vai ser i+1 = {2,3,...}, pois o 1 já é o melhor da geração passada
        trem = trem_bala(0,i+2,geracao)

        inputs[0] = tempo_restante
        inputs[1] = distancia_inicial
        trem.inputs = inputs

        # os pesos dos novos trens serão baseados nos pesos do melhor trem da geração passada
        # mas eles podem "mutar"
        for j in range(len(melhor_trem.pesos)):
            if random.randint(1,100) <= TAXA_MUTACAO_PESOS:
                peso = random.randint(PESO_MINIMO, PESO_MAXIMO)
                pesos.append(peso)
            else:
                peso = melhor_trem.pesos[j]
                pesos.append(peso)
        trem.pesos = pesos

        # gerando o bias de cada trem baseado no bias do melhor trem
        # mas ele também pode "mutar"
        if random.randint(1,100) <= TAXA_MUTACAO_BIAS:
            bias = random.randint(BIAS_MINIMO, BIAS_MAXIMO)
        else:
            bias = melhor_trem.bias
        trem.bias = bias

        trens.append(trem)

    rodar_jogo(tela, trens, geracao)

def inicializar_jogo():

    # define a tela do jogo com as dimensões passadas
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

    # vetor que receberá todos os trens
    trens = []

    # na inicialização dos trens, considero que todos tem o tempo limite para completar a tarefa
    tempo_restante = TENPO_LIMITE - 0

    # a distância inicial é a mesma para todos os trens
    distancia_inicial = LARGURA_TELA - COMPRIMENTO_TREM

    # os trens inciais são da geração 1
    geracao = 1

    # criando os trens da primeira geração
    for i in range(QUANTIDADE_TRENS):

        # inicializa um vetor para receber os inputs a serem alocados nos trens
        inputs = [0,0]

        # inicializa um vetor vazio para receber os pesos a serem alocados nos trens
        pesos = []

        # todos começam no ponto inicial x = 0
        # o número do trem vai ser i+1 = {1,2,...}
        trem = trem_bala(0,i+1,geracao)

        inputs[0] = tempo_restante
        inputs[1] = distancia_inicial
        trem.inputs = inputs

        # para cada input deve haver um peso
        # inicialmente eles são gerados aleatoriamente
        for j in range(len(inputs)):
            peso = random.randint(PESO_MINIMO, PESO_MAXIMO)
            pesos.append(peso)
        trem.pesos = pesos

        # gerando o bias inicial de cada trem
        bias = random.randint(BIAS_MINIMO, BIAS_MAXIMO)
        trem.bias = bias

        trens.append(trem)

    rodar_jogo(tela, trens, geracao)

        

def main():

    inicializar_jogo()
#---------------------------------------------------------------------------------------------------------

main()
