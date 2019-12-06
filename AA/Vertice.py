import pygame
import math
from AA.configuracoes import *
vec = pygame.math.Vector2

class Vertice:
    def __init__(self, programa, ehParede):
        self.ehParede = ehParede
        self.g = self.inicializa_G()
        self.h = self.inicializa_H()
        self.f = self.set_F()
        self.pai = None
        self.GdoPai = 0

    def inicializa_G(self):
        if self.ehParede == True:
            self.g = 10000000
        else:
            self.g = 0
        return self.g

    def inicializa_H(self):
        if self.ehParede == True:
            self.h = 10000000
        else:
            self.h = 0
        return self.h

    def set_GdoPai(self, g):
        self.GdoPai = g

    def set_G(self, atual, vizinho):
        self.g = math.sqrt(math.pow((atual[0] - vizinho[0]), 2) + math.pow((atual[1] - vizinho[1]), 2)) +\
                 self.GdoPai

    def set_H(self, destino, vizinho):
        #fazer com que todas as paredes tenha uma heurística muito grande
        if self.ehParede == True:
            self.h = 10000000
        else:
            self.h = math.sqrt(math.pow((vizinho[0] - destino[0]), 2) + math.pow((vizinho[1] - destino[1]), 2))

    def set_F(self):
        self.f = self.g + self.h

    def set_Pai(self, vertice_pai):
        self.pai = vertice_pai

    def get_GdoPai(self):
        return self.GdoPai

    def get_F(self):
        return self.f

    def get_G(self):
        return self.g

    def get_H(self):
        return self.h

    def get_Pai(self):
        return self.pai
