import pygame
import sys
from AA.configuracoes import *
from AA.Pacman import *

pygame.init()
vec = pygame.math.Vector2

class Programa:
    def __init__(self):
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))  # Criacao da janela (dimensoes)
        pygame.display.set_caption("Pac Man by: Rita Chen & Vitor Queiroz")  # Titulo do programa
        icon = pygame.image.load("imagens/pacman_32px.png")
        pygame.display.set_icon(icon)  # Coloca na janela o desenho do pacman (no cabeçalho)
        self.clock = pygame.time.Clock()  # Define o clock pro fps
        self.executando = True
        self.state = 'tela de inicio' #Quando começa o programa, aparece a tela de inicio
        self.largura_quadradoGrid = LARGURA_LAB // 28
        self.altura_quadradoGrid = ALTURA_LAB // 30
        self.jogador = Pacman(self, POSICAO_INICIAL_PACMAN)

        self.load()

    def run(self):
        while self.executando: #enquanto o programa estiver executando...
            if self.state == 'tela de inicio': #se estiver na tela inicial (antes de jogar)
                self.telaInicio_eventos()
                self.telaInicio_atualiza()
                self.telaInicio_desenha()
            if self.state == 'jogando': #se estiver na tela de jogo
                self.jogo_eventos()
                self.jogo_atualiza()
                self.jogo_desenha()
            self.clock.tick(FPS)
        pygame.quit()  # fecha o programa
        sys.exit()

    def escreve_texto(self, texto, janela, posicao, tamanhoFonte, cor, nomeFonte, centralizado=False): # Escreve texto na tela
        fonte = pygame.font.SysFont(nomeFonte, tamanhoFonte)
        text = fonte.render(texto, False, cor)
        text_size = text.get_size()
        #Para centralizar o texto na tela
        if centralizado:
            posicao[0] = posicao[0]-text_size[0]//2
            posicao[1] = posicao[1] - text_size[1]//2
        janela.blit(text, posicao)

    def load(self):
        self.background = pygame.image.load('imagens/labirinto.png')
        self.background = pygame.transform.scale(self.background, (LARGURA_LAB, ALTURA_LAB)) #transforma o background de forma a caber na janela

    def draw_grid(self): #matriz de posicoes para demarcar onde o jogador poderá andar, paredes, moedas..
        for x in range(LARGURA//self.largura_quadradoGrid):
            pygame.draw.line(self.background, BRANCO, (x*self.largura_quadradoGrid, 0), (x*self.largura_quadradoGrid, ALTURA))
        for x in range(ALTURA//self.altura_quadradoGrid):
            pygame.draw.line(self.background, BRANCO, (0, x*self.altura_quadradoGrid), (LARGURA, x*self.altura_quadradoGrid))

    def telaInicio_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Se apertar o X, encerra o programa
                self.executando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE: # Se apertar o espaço, começa o jogo
                    self.state = 'jogando'

    def telaInicio_atualiza(self):
        pass

    def telaInicio_desenha(self): #O que vai ter na tela de inicio
        self.janela.fill(PRETO)
        self.escreve_texto('HIGH SCORE', self.janela, [LARGURA//2-200, 10],
                           TAMANHO_FONTE, (BRANCO), FONTE, centralizado = False)
        self.escreve_texto('PUSH SPACE BAR', self.janela, [LARGURA//2, ALTURA//2 - 50], TAMANHO_FONTE,
                           (LARANJA), FONTE, centralizado = True)
        self.escreve_texto('1 PLAYER ONLY', self.janela, [LARGURA // 2, ALTURA // 2], TAMANHO_FONTE,
                           (AZUL), FONTE, centralizado = True)
        self.escreve_texto('GAME BY: RITA CHEN & VITOR QUEIROZ', self.janela, [LARGURA // 2, ALTURA // 2 + 250], TAMANHO_FONTE,
                           (AQUAMARINE), FONTE, centralizado = True)
        pygame.display.update()

    def jogo_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Se apertar o X, encerra o programa
                self.executando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.jogador.move(vec(0,-1))
                    self.jogador.angulo = 90
                elif evento.key == pygame.K_DOWN:
                    self.jogador.angulo = 270
                    self.jogador.move(vec(0, 1))
                elif evento.key == pygame.K_LEFT:
                    self.jogador.angulo = 180
                    self.jogador.move(vec(-1, 0))
                elif evento.key == pygame.K_RIGHT:
                    self.jogador.angulo = 0
                    self.jogador.move(vec(1, 0))

    def jogo_atualiza(self):
        pass
        self.jogador.atualiza()

    def jogo_desenha(self):
        self.janela.fill(PRETO)
        self.janela.blit(self.background, (ESPACOS_JOGO//2, ESPACOS_JOGO//2))
        self.draw_grid()
        self.escreve_texto('SCORE: 0', self.janela, [10,2], TAMANHO_FONTEJOGO, BRANCO, FONTE, centralizado=False)
        self.escreve_texto('HIGH SCORE: 0', self.janela, [LARGURA-140, 2], TAMANHO_FONTEJOGO, BRANCO, FONTE, centralizado=False)
        self.jogador.draw()
        pygame.display.update()