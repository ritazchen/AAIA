import pygame
from AA.configuracoes import *
vec = pygame.math.Vector2

class Pacman:
    def __init__(self, programa, posicao):
        self.programa = programa
        self.grid_pos = posicao
        self.starting_pos = [posicao.x, posicao.y]
        self.pix_pos = self.get_pix_pos()
        #self.pix_pos.x += 9
        #self.pix_pos.y += 9
        self.direcao = vec(1,0)
        self.stored_direcao = None
        self.pode_mover = True
        self.pontuacao = 0
        self.velocidade = 2
        self.vidas = 3
        #self.pacmanImg = pygame.image.load("imagens/pacman_ABERTO.png")

    def atualiza(self):
        #só pode andar se não for parede
        if self.pode_mover:
            self.pix_pos += self.direcao*self.velocidade
        # não permitir que ande pela diagonal
        if self.tempo_para_mover():
            if self.stored_direcao != None:
                self.direcao = self.stored_direcao
            self.pode_mover = self.verifica_movimento()

        #a parte de baixo indica qual a posicao do grid está o pacman
        self.grid_pos[0] = (self.pix_pos[0]-ESPACOS_JOGO + self.programa.largura_quadradoGrid//2)//self.programa.largura_quadradoGrid + 1 #2
        self.grid_pos[1] = (self.pix_pos[1]-ESPACOS_JOGO + self.programa.altura_quadradoGrid//2)//self.programa.altura_quadradoGrid + 1 #2

        if self.sobreAMoeda():
            self.coleta_moeda()

    def desenha(self):
        #pacmanImg = pygame.image.load("imagens/pacman_ABERTO.png")
        #self.programa.janela.blit(self.pacmanImg, ((int)(self.pix_pos.x), (int)(self.pix_pos.y)))
        pygame.draw.circle(self.programa.janela, AMARELO, (int(self.pix_pos.x), int(self.pix_pos.y)), self.programa.largura_quadradoGrid//2-2)
        #pygame.draw.rect(self.programa.janela, LARANJA, (self.grid_pos[0]*self.programa.largura_quadradoGrid + ESPACOS_JOGO//2,
                                                         #self.grid_pos[1]*self.programa.altura_quadradoGrid + ESPACOS_JOGO//2,
                                                         #self.programa.largura_quadradoGrid, self.programa.altura_quadradoGrid), 1)
            #if self.vidas >= 2:
                #self.programa.janela.blit(self.vidaImg, (35, ALTURA - 25))
            #if self.vidas >=3:
                #self.programa.janela.blit(self.vidaImg, (55, ALTURA - 25))

    def sobreAMoeda(self):
        #verifica se o pacman passou por cima das moedas
        if self.grid_pos in self.programa.moedas:
            if self.tempo_para_mover():
                return True
        return False

    def coleta_moeda(self):
        #remove da lista de moedas existentes e soma 10 à pontuação
        self.programa.moedas.remove(self.grid_pos)
        self.pontuacao += 10

    def move(self, direcao):
        self.stored_direcao = direcao

    def get_pix_pos(self): #espacos_jogo//3
        return vec((self.grid_pos[0]*self.programa.largura_quadradoGrid) + ESPACOS_JOGO//2+self.programa.largura_quadradoGrid//2,
                (self.grid_pos[1]*self.programa.altura_quadradoGrid) + ESPACOS_JOGO//2+self.programa.altura_quadradoGrid//2)

    def tempo_para_mover(self):
        #bloqueia que ele mude de coordenada no mesmo tempo.
        if int(self.pix_pos.x+ESPACOS_JOGO//2) % self.programa.largura_quadradoGrid == 0:
            if self.direcao == vec(1,0) or self.direcao == vec(-1,0) or self.direcao == vec(0,0):
                return True
        if int(self.pix_pos.y+ESPACOS_JOGO//2) % self.programa.altura_quadradoGrid == 0 or self.direcao == vec(0,0):
            if self.direcao == vec(0,1) or self.direcao == vec(0,-1):
                return True
        return False

    def verifica_movimento(self):
        #se o bater numa parede, não vai atravessar
        #tentar fazer com que ele não deixe movimentar pro lado da parede
        for parede in self.programa.paredes:
            if vec(self.grid_pos + self.direcao) == parede:
                return False
        return True

    def get_grid_posX(self):
        return self.grid_pos[0]

    def get_grid_posY(self):
        return self.grid_pos[1]