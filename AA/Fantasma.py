import pygame
from AA.configuracoes import *
vec = pygame.math.Vector2

class Fantasma:
    def __init__(self, programa, posicao, num):
        self.programa = programa
        self.grid_pos = posicao
        self.pix_pos = self.get_pix_pos()
        self.pix_pos.x += 11
        self.pix_pos.y += 10
        self.raio = self.programa.largura_quadradoGrid//2 - 2
        self.numero = num
        self.cor = None

    def atualiza(self):
        pass

    def desenha(self):
        if self.numero == 0:
            pygame.draw.circle(self.programa.janela, LARANJA, (int(self.pix_pos.x), int(self.pix_pos.y)), int(self.raio))
        elif self.numero == 1:
            pygame.draw.circle(self.programa.janela, VERMELHO, (int(self.pix_pos.x), int(self.pix_pos.y)), int(self.raio))
        elif self.numero == 2:
            pygame.draw.circle(self.programa.janela, AZULBB, (int(self.pix_pos.x), int(self.pix_pos.y)), int(self.raio))
        elif self.numero == 3:
            pygame.draw.circle(self.programa.janela, ROSA, (int(self.pix_pos.x), int(self.pix_pos.y)), int(self.raio))

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.programa.largura_quadradoGrid) + ESPACOS_JOGO//2+self.programa.largura_quadradoGrid//2,
                (self.grid_pos.y*self.programa.altura_quadradoGrid) + ESPACOS_JOGO//2+self.programa.altura_quadradoGrid//2)
