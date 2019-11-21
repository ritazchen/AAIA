from pygame.math import Vector2 as vec

#Dimensoes da janela
LARGURA, ALTURA = 560, 620 #418, 596

#Dimensoes para colocar a pontuação e as vidas restantes
ESPACOS_JOGO = 50

#Dimensoes do labirinto
LARGURA_LAB, ALTURA_LAB = (LARGURA - ESPACOS_JOGO), (ALTURA - ESPACOS_JOGO)

#FPS
FPS = 60

#Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
LARANJA = (244, 164, 96)
AZUL = (0, 178, 238)
AQUAMARINE = (118, 238, 198)

#Fontes
TAMANHO_FONTE = 15
TAMANHO_FONTEJOGO = 14
FONTE = 'arial black'

#Informacoes sobre o Pacman
POSICAO_INICIAL_PACMAN = vec(1,1) #posicao inicial dele