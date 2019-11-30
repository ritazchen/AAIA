import pygame
from AA.configuracoes import *
vec = pygame.math.Vector2

class Fantasma:
    def __init__(self, programa, posicao):
        self.programa = programa
        self.grid_pos = posicao
        self.pix_pos = self.get_pix_pos()

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.programa.largura_quadradoGrid) + ESPACOS_JOGO//3+self.programa.largura_quadradoGrid//2,
                (self.grid_pos.y*self.programa.altura_quadradoGrid) + ESPACOS_JOGO//3+self.programa.altura_quadradoGrid//2)

    def atualiza(self):
        pass

    def desenha(self):
        pygame.draw.circle(self.programa.janela, VERMELHO, (int(self.pix_pos.x), int(self.pix_pos.y)), self.programa.largura_quadradoGrid//2-2)

