import pygame
import sys
import copy
from AA.configuracoes import *
from AA.Pacman import *
from AA.Fantasma import *

pygame.init()
vec = pygame.math.Vector2

class Programa:
    def __init__(self):
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))  # Criacao da janela (dimensoes)
        self.clock = pygame.time.Clock()  # Define o clock pro fps
        self.executando = True
        self.state = 'tela de inicio'  # Quando começa o programa, aparece a tela de inicio #28
        pygame.display.set_caption("Pac Man by: Rita Chen & Vitor Queiroz")  # Titulo do programa
        self.icon = pygame.image.load("imagens/pacman_32px.png")
        pygame.display.set_icon(self.icon)  # Coloca na janela o desenho do pacman (no cabeçalho)
        self.largura_quadradoGrid = LARGURA_LAB // COLS
        self.altura_quadradoGrid = ALTURA_LAB // ROWS
        self.paredes = []
        self.moedas = []
        self.fantasmas = []
        self.jogador_posicao = None
        self.fantasma_posicao = []
        self.recorde = 0
        self.load()
        self.jogador = Pacman(self, vec(self.jogador_posicao))
        self.cria_inimigos()
        self.passei = 0

    def run(self):
        while self.executando: #enquanto o programa estiver executando...
            if self.state == 'tela de inicio': #se estiver na tela inicial (antes de jogar)
                self.telaInicio_eventos()
                self.telaInicio_atualiza()
                self.telaInicio_desenha()
            elif self.state == 'jogando': #se estiver na tela de jogo
                self.jogo_eventos()
                self.jogo_atualiza()
                self.jogo_desenha()
            elif self.state == 'game over': #se estiver na tela de jogo
                self.gameover_eventos()
                self.gameover_atualiza()
                self.gameover_desenha()
            else:
                self.executando = False
            self.clock.tick(FPS)
        pygame.quit()  # fecha o programa
        sys.exit()

    def escreve_texto(self, texto, janela, posicao, tamanhoFonte, cor, nomeFonte, centralizado=False): # Escreve texto na tela
        fonte = pygame.font.SysFont(nomeFonte, tamanhoFonte)
        text = fonte.render(texto, False, cor)
        text_size = text.get_size()
        #Para centralizar o texto na tela
        if centralizado:
            posicao[0] = posicao[0] - text_size[0]//2
            posicao[1] = posicao[1] - text_size[1]//2
        janela.blit(text, posicao)

    def load(self):
        self.inicio = pygame.image.load('imagens/tela_inicio.png')
        self.aperta_jogar = pygame.image.load('imagens/tela_inicio_aperta.png')
        self.background = pygame.image.load('imagens/labirinto.png')
        self.perdeu = pygame.image.load('imagens/tela_perdeu.png')
        self.aperta_jogar_dnv = pygame.image.load('imagens/tela_perdeu_aperta.png')
        self.vidaImg = pygame.image.load("imagens/pacman_vida.png")
        #self.background = pygame.transform.scale(self.background, (LARGURA_LAB, ALTURA_LAB)) #transforma o background de forma a caber na janel

        #faz leitura das coisas existentes
        with open("coisas.txt", 'r') as arquivo:
            for indice_y, linha in enumerate(arquivo):
                for indice_x, objeto in enumerate(linha):
                    if objeto == 'P':
                        self.paredes.append(vec(indice_x, indice_y)) #passa as coordenadas de cada parede para a lista paredes
                    elif objeto == 'M':
                        self.moedas.append(vec(indice_x, indice_y)) #passa as coordenadas de cada moeda para a lista moedas
                    elif objeto == 'J':
                        self.jogador_posicao = [indice_x, indice_y] #passa as coordenadas de cada moeda para a lista moedas
                    elif objeto in ["1", "2", "3", "4"]:
                        self.fantasma_posicao.append(vec(indice_x, indice_y)) #passa as coordenadas de inicio dos inimigos
                    #elif objeto == 'D': #onde estao as portas para os inimigos saírem
                        #colocar as coordenadas para q o pacman não entre e que os inimigos saiam o mais rapido possivel de la dentro
        arquivo.close()
        with open("recorde.txt", 'r') as arquivo:
            self.recorde = int(arquivo.read())
            #print(int(valor))
        arquivo.close()

    def cria_inimigos(self):
        #cria um inimigo em cada posição
        for indice_x, posicao in enumerate(self.fantasma_posicao):
            self.fantasmas.append(Fantasma(self, vec(posicao), indice_x))

    def desenha_grid(self): #matriz de posicoes para demarcar onde o jogador poderá andar, paredes, moedas..
        for x in range(LARGURA//self.largura_quadradoGrid):
            pygame.draw.line(self.janela, CINZA, (x*self.largura_quadradoGrid, 0), (x*self.largura_quadradoGrid, ALTURA))
        for x in range(ALTURA//self.altura_quadradoGrid):
            pygame.draw.line(self.janela, CINZA, (0, x*self.altura_quadradoGrid), (LARGURA, x*self.altura_quadradoGrid))
        #for parede in self.paredes:
            #pygame.draw.rect(self.background, AQUAMARINE, (parede.x*self.largura_quadradoGrid, parede.y*self.altura_quadradoGrid,
                                                            #self.largura_quadradoGrid, self.altura_quadradoGrid))
        #for moeda in self.moedas:
            #pygame.draw.rect(self.background, LARANJA, (moeda.x*self.largura_quadradoGrid, moeda.y*self.altura_quadradoGrid,
                                                            #self.largura_quadradoGrid, self.altura_quadradoGrid))

    def reset(self):
        if int(self.recorde) < self.jogador.pontuacao:
            with open("recorde.txt", 'w') as arquivo:
                arquivo.write(str(self.jogador.pontuacao))
            arquivo.close()

        with open("recorde.txt", 'r') as arquivo:
            self.recorde = int(arquivo.read())
        arquivo.close()
        self.jogador.vidas = 3
        self.jogador.pontuacao = 0
        self.jogador.grid_pos = vec(self.jogador.starting_pos)
        self.jogador.pix_pos = self.jogador.get_pix_pos()
        self.jogador.direcao *= 0
        for fantasma in self.fantasmas:
            fantasma.grid_pos = vec(fantasma.starting_pos)
            fantasma.pix_pos = fantasma.get_pix_pos()
            fantasma.direcao *= 0

        self.moedas = []
        with open("coisas.txt", 'r') as arquivo:
            for indice_y, linha  in enumerate(arquivo):
                for indice_x, objeto in enumerate(linha):
                    if objeto == 'M':
                        self.moedas.append(vec(indice_x, indice_y))
        arquivo.close()
        self.state = "jogando"

    def telaInicio_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Se apertar o X, encerra o programa
                self.executando = False
            else:
                #print(pygame.mouse.get_pos())
                if pygame.mouse.get_pos()[0] >= 160 and pygame.mouse.get_pos()[0] <= 343:
                    if pygame.mouse.get_pos()[1] >= 328 and pygame.mouse.get_pos()[1] <= 442: #arrumar
                        self.passei = 1
                else:
                    self.passei = 0
                if evento.type == pygame.MOUSEBUTTONDOWN and self.passei == 1:
                    self.state = 'jogando'

    def telaInicio_atualiza(self):
        pass

    def telaInicio_desenha(self): #O que vai ter na tela de inicio
        self.janela.fill(PRETO)
        if self.passei == 0:
            self.janela.blit(self.inicio, (0, 0))
        else:
            self.janela.blit(self.aperta_jogar, (0, 0))

        pygame.display.update()

    def jogo_eventos(self):
        for evento in pygame.event.get():
            up = 0
            down = 0
            left = 0
            right = 0
            if evento.type == pygame.QUIT:  # Se apertar o X, encerra o programa
                self.executando = False
            if evento.type == pygame.KEYDOWN:
                for parede in self.paredes: #se o proximo mov bater numa parede, nao deixar movimentar
                    if [int(self.jogador.get_grid_posX()), int(self.jogador.get_grid_posY() - 1)] != [int(parede[0]), int(parede[1])]:
                        up += 1
                    if up == len(self.paredes) and (evento.key == pygame.K_UP or evento.key == pygame.K_w):
                        self.jogador.move(vec(0,-1))
                        self.jogador.angulo = 90

                    if [int(self.jogador.get_grid_posX()), int(self.jogador.get_grid_posY() + 1)] != [int(parede[0]), int(parede[1])]:
                        down += 1
                    if down == len(self.paredes) and (evento.key == pygame.K_DOWN or evento.key == pygame.K_s):
                        self.jogador.angulo = 270
                        self.jogador.move(vec(0, 1))

                    if [int(self.jogador.get_grid_posX() - 1), int(self.jogador.get_grid_posY())] != [int(parede[0]), int(parede[1])]:
                        left += 1
                    if left == len(self.paredes) and (evento.key == pygame.K_LEFT or evento.key == pygame.K_a):
                        self.jogador.angulo = 180
                        self.jogador.move(vec(-1, 0))

                    if [int(self.jogador.get_grid_posX() + 1), int(self.jogador.get_grid_posY())] != [int(parede[0]), int(parede[1])]:
                        right += 1
                    if right == len(self.paredes) and (evento.key == pygame.K_RIGHT or evento.key == pygame.K_d):
                        self.jogador.angulo = 0
                        self.jogador.move(vec(1, 0))

    def jogo_atualiza(self):
        self.jogador.atualiza()
        for fantasma in self.fantasmas:
            fantasma.atualiza()

        for fantasma in self.fantasmas:
            if fantasma.grid_pos == self.jogador.grid_pos:
                self.perde_vida()

    def jogo_desenha(self):
        self.janela.fill(PRETO)
        self.janela.blit(self.background, (ESPACOS_JOGO//2, ESPACOS_JOGO//2))
        self.desenha_moedas()
        #self.desenha_grid()
        self.escreve_texto('SCORE: {}'.format(self.jogador.pontuacao), self.janela, [10,2], TAMANHO_FONTEJOGO, BRANCO, FONTE, centralizado=False)
        self.escreve_texto('HIGH SCORE: {}'.format(self.recorde), self.janela, [LARGURA-160, 2], TAMANHO_FONTEJOGO, BRANCO, FONTE, centralizado=False)
        self.jogador.desenha()
        for fantasma in self.fantasmas:
            fantasma.desenha()
        for i in range(self.jogador.vidas):
            self.janela.blit(self.vidaImg, (20+20*i, ALTURA-25))
        pygame.display.update()

    def perde_vida(self):
        self.jogador.vidas -= 1
        if self.jogador.vidas == 0:
            self.state = "game over"
        else:
            self.jogador.grid_pos = vec(self.jogador.starting_pos)
            self.jogador.pix_pos = self.jogador.get_pix_pos()
            self.jogador.direcao *= 0
            for fantasma in self.fantasmas:
                fantasma.grid_pos = vec(fantasma.starting_pos)
                fantasma.pix_pos = fantasma.get_pix_pos()
                fantasma.direcao *= 0
                fantasma.pix_pos.x += 11
                fantasma.pix_pos.y += 10

    def desenha_moedas(self):
        for moeda in self.moedas:
            pygame.draw.circle(self.janela, AMARELO, (int(ESPACOS_JOGO//2 + self.largura_quadradoGrid//2 + moeda.x*self.largura_quadradoGrid),
                                                          int(ESPACOS_JOGO//2 + self.altura_quadradoGrid//2 + moeda.y*self.altura_quadradoGrid)), 4)

    def gameover_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Se apertar o X, encerra o programa
                self.executando = False
            else:
                if pygame.mouse.get_pos()[0] >= 107 and pygame.mouse.get_pos()[0] <= 494:
                    if pygame.mouse.get_pos()[1] >= 365 and pygame.mouse.get_pos()[1] <= 575: #arrumar
                        self.passei = 1
                else:
                    self.passei = 0
                if evento.type == pygame.MOUSEBUTTONDOWN and self.passei == 1:
                    self.reset()

    def gameover_atualiza(self):
        pass

    def gameover_desenha(self): #O que vai ter na tela de inicio
        self.janela.fill(PRETO)
        if self.passei == 0:
            self.janela.blit(self.perdeu, (0, 0))
        else:
            self.janela.blit(self.aperta_jogar_dnv, (0, 0))

        pygame.display.update()