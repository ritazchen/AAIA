import pygame
from AA.configuracoes import *
vec = pygame.math.Vector2

class Pacman:
    def __init__(self, programa, posicao):
        self.programa = programa
        self.grid_pos = posicao
        self.pix_pos = self.get_pix_pos()
        self.direcao = vec(0,0)

    def atualiza(self):
        self.pix_pos += self.direcao
        #a parte de baixo indica qual a posicao do grid está o pacman
        self.grid_pos[0] = (self.pix_pos[0]-ESPACOS_JOGO)//self.programa.largura_quadradoGrid + 2
        self.grid_pos[1] = (self.pix_pos[1]-ESPACOS_JOGO)//self.programa.altura_quadradoGrid + 2

    def draw(self):
        pacmanImg = pygame.image.load("imagens/pacman_ABERTO.png")
        self.programa.janela.blit(pacmanImg, ((int)(self.pix_pos.x), (int)(self.pix_pos.y)))
        #pygame.draw.circle(self.programa.janela, LARANJA, (int(self.pix_pos.x), int(self.pix_pos.y)), self.programa.largura_quadradoGrid//2-2)
        pygame.draw.rect(self.programa.janela, LARANJA, (self.grid_pos[0]*self.programa.largura_quadradoGrid + ESPACOS_JOGO//2,
                                                         self.grid_pos[1]*self.programa.altura_quadradoGrid + ESPACOS_JOGO//2,
                                                         self.programa.largura_quadradoGrid, self.programa.altura_quadradoGrid), 1)

    def move(self, direcao):
        self.direcao = direcao

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.programa.largura_quadradoGrid) + ESPACOS_JOGO//3+self.programa.largura_quadradoGrid//2,
                (self.grid_pos.y*self.programa.altura_quadradoGrid) + ESPACOS_JOGO//3+self.programa.altura_quadradoGrid//2)