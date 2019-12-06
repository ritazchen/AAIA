from AA.Vertice import *
from AA.configuracoes import *
vec = pygame.math.Vector2

class Fantasma:
    def __init__(self, programa, posicao, num):
        self.programa = programa #chama o programa
        self.grid_pos = posicao #posicao do inimigo em relação ao grid
        self.starting_pos = [posicao.x, posicao.y]
        self.pix_pos = self.get_pix_pos() #posicao do inimigo em relação aos pixels
        #as adições são só feitas para que os inimigos fiquem no centro do espaço
        #self.pix_pos.x += 11
        #self.pix_pos.y += 10
        self.raio = self.programa.largura_quadradoGrid//2 - 2 #tamanho do raio do inimigo
        self.numero = num #cada inimigo será representado por um numero
        self.cor = None #cada inimigo será representado por uma cor
        self.direcao = vec(0,0) #movimentação inicial de cada inimigo (subir para sair do espaço)
        self.normal = True
        self.forma = self.set_forma() #se ele vai estar normal (rapido) ou se vai estar assustado (lento)
        self.target = None #objetivo de alcançar o pacman ou fugir do pacman
        #self.fantAzulImg = pygame.image.load("imagens/fant_azul.png")
        self.velocidade = self.altera_velocidade()
        self.pode_mover = True

    def atualiza(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            #if self.pode_mover:
            self.pix_pos += self.direcao*self.velocidade
            if self.tempo_para_mover():
                self.move()
                #self.pode_mover = self.verifica_movimento()

        # a parte de baixo indica qual a posicao do grid está o inimigo
        self.grid_pos[0] = (self.pix_pos[0] - ESPACOS_JOGO + self.programa.largura_quadradoGrid // 2) // self.programa.largura_quadradoGrid + 1  # 2
        self.grid_pos[1] = (self.pix_pos[1] - ESPACOS_JOGO + self.programa.altura_quadradoGrid // 2) // self.programa.altura_quadradoGrid + 1  # 2

    def verifica_movimento(self):
        for parede in self.programa.paredes:
            if vec(self.grid_pos + self.direcao) == parede:
                return False
        return True

    def altera_velocidade(self):
        if self.forma in ["clyde", "blinky", "inky"]:
            velocidade = 1 #2
        else:
            velocidade = 1

        return velocidade

    def desenha(self):
        if self.numero == 0:
            #self.programa.janela.blit(self.fantAzulImg, (int(self.pix_pos.x), int(self.pix_pos.y)))
            pygame.draw.circle(self.programa.janela, LARANJA, (int(self.pix_pos.x), int(self.pix_pos.y)), int(self.raio))
        elif self.numero == 1:
            #self.programa.janela.blit(self.fantAzulImg, (int(self.pix_pos.x), int(self.pix_pos.y)))
            pygame.draw.circle(self.programa.janela, VERMELHO, (int(self.pix_pos.x), int(self.pix_pos.y)), int(self.raio))
        elif self.numero == 2:
            #self.programa.janela.blit(self.fantAzulImg, (int(self.pix_pos.x), int(self.pix_pos.y)))
            pygame.draw.circle(self.programa.janela, AZULBB, (int(self.pix_pos.x), int(self.pix_pos.y)), int(self.raio))
        elif self.numero == 3:
            #self.programa.janela.blit(self.fantAzulImg, (int(self.pix_pos.x), int(self.pix_pos.y)))
            pygame.draw.circle(self.programa.janela, ROSA, (int(self.pix_pos.x), int(self.pix_pos.y)), int(self.raio))
        #while self.caminho:
            #pygame.draw.rect(self.programa.background, LARANJA, (
                #self.caminho[0][0] * self.programa.largura_quadradoGrid, self.caminho[0][1] * self.programa.altura_quadradoGrid,
                #self.programa.largura_quadradoGrid, self.programa.altura_quadradoGrid))
            #self.caminho.pop(self.caminho[0])

    def set_forma(self):
        if self.numero == 0:
            return "clyde"
        elif self.numero == 1:
            return "blinky"
        elif self.numero == 2:
            return "inky"
        elif self.numero == 3:
            return "pinky"

    def move(self):
        # pode ser um aleatório mais fácil até uma certa pontuação e depois o A* entra em ação
        if self.forma == "blinky":
            caminho = self.pega_caminho(self.target)
            while(caminho):
                x = caminho[0][0] - self.grid_pos[0]
                y = caminho[0][1] - self.grid_pos[1]
                if caminho[0] in self.programa.paredes:
                    caminho.pop()
                    continue
                else:
                    caminho.pop()
                    self.direcao = vec(x, y)
        elif self.forma == "pinky":
            caminho = self.pega_caminho(self.target)
            while(caminho):
                x = caminho[0][0] - self.grid_pos[0]
                y = caminho[0][1] - self.grid_pos[1]
                if caminho[0] in self.programa.paredes:
                    caminho.pop()
                    continue
                else:
                    caminho.pop()
                    self.direcao = vec(x, y)
        elif self.forma == "inky":
            caminho = self.pega_caminho(self.target)
            while(caminho):
                x = caminho[0][0] - self.grid_pos[0]
                y = caminho[0][1] - self.grid_pos[1]
                if caminho[0] in self.programa.paredes:
                    caminho.pop()
                    continue
                else:
                    caminho.pop()
                    self.direcao = vec(x, y)
        elif self.forma == "clyde":
            caminho = self.pega_caminho(self.target)
            while(caminho):
                x = caminho[0][0] - self.grid_pos[0]
                y = caminho[0][1] - self.grid_pos[1]
                if caminho[0] in self.programa.paredes:
                    caminho.pop()
                    continue
                else:
                    caminho.pop()
                    self.direcao = vec(x, y)

    def tempo_para_mover(self):
        #bloqueia que ele mude de coordenada no mesmo tempo.
        if int(self.pix_pos.x+ESPACOS_JOGO//2) % self.programa.largura_quadradoGrid == 0:
            if self.direcao == vec(1,0) or self.direcao == vec(-1,0):
                return True
        if int(self.pix_pos.y+ESPACOS_JOGO//2) % self.programa.altura_quadradoGrid == 0:
            if self.direcao == vec(0,1) or self.direcao == vec(0,-1):
                return True
        if self.forma == "clyde" and self.direcao == vec(0,0) and self.programa.jogador.pontuacao >= 0:
            self.direcao = vec(0,-1)
            return True
        elif self.forma == "pinky" and self.direcao == vec(0,0) and self.programa.jogador.pontuacao >= 500:
            self.direcao = vec(0,-1)
            return True
        elif self.forma == "inky" and self.direcao == vec(0,0) and self.programa.jogador.pontuacao >= 800:
            self.direcao = vec(0,-1)
            return True
        elif self.forma == "blinky" and self.direcao == vec(0,0) and self.programa.jogador.pontuacao >= 1200:
            self.direcao = vec(0,-1)
            return True
        return False

    def pega_caminho(self, target):
        path = self.Aestrela([int(self.grid_pos.x), int(self.grid_pos.y)],
                [int(target[0]), int(target[1])])
        return path

    def bSort(self, grid, lista):
        tam = len(lista)
        for i in range(0, tam):
            for j in range(0, tam - i - 1):
                if (grid[lista[j][0]][lista[j][1]].get_F() > grid[lista[j + 1][0]][lista[j+1][1]].get_F()):
                    vertice = lista[j]
                    lista[j] = lista[j + 1]
                    lista[j + 1] = vertice
                elif (grid[lista[j][0]][lista[j][1]].get_F() == grid[lista[j + 1][0]][lista[j + 1][1]].get_F()):
                    if (grid[lista[j][0]][lista[j][1]].get_H() > grid[lista[j + 1][0]][lista[j + 1][1]].get_H()):
                        vertice = lista[j]
                        lista[j] = lista[j + 1]
                        lista[j + 1] = vertice
        return lista

    def Aestrela(self, origem, destino):
        #faz um grid auxiliar de vertices
        gridAuxiliar = [[Vertice(self.programa, False) for x in range(30)] for x in range(28)]
        for parede in self.programa.paredes:
            if parede.x < COLS and parede.y < ROWS:
                gridAuxiliar[int(parede.x)][int(parede.y)].ehParede = True #ele tem as coordenadas trocadas msm
                gridAuxiliar[int(parede.x)][int(parede.y)].inicializa_G() #trocar o g
                gridAuxiliar[int(parede.x)][int(parede.y)].inicializa_H() #trocar o h
                gridAuxiliar[int(parede.x)][int(parede.y)].set_F() #trocar o f

        # 1 - adicione o quadrado inicial à lista de abertos
        lista_aberta = [origem] #origem é a posição do grid que o inimigo estará inicialmente
        lista_fechada = []
        atual = lista_aberta[0]

        # 2 - enquanto há elemento na lista de abertos e não chegou ao destino
        while lista_aberta:
            # 2a Ache a célula que tenha o menor custo f(n) na lista aberta
            lista_aberta = self.bSort(gridAuxiliar, lista_aberta)
            atual = lista_aberta[0] #o vertice que tem o menor f está na pos 0 e será o vertice a ser analisado

            # 2b Retire o nó escolhido da lista aberta para a lista fechada
            lista_aberta.remove(lista_aberta[0])
            lista_fechada.append(atual)

            if atual == destino:
                break

            # 2c Para cada vértice vizinho adjacente a célula analisada faça
            vizinhos = [[atual[0], atual[1] + 1], [atual[0], atual[1] - 1], [atual[0] + 1, atual[1]], [atual[0] - 1, atual[1]]] #Pega apenas os vizinhos das verticais e horizontais
            for vizinho in vizinhos:
                #não pega os inimigos que são foras do grid
                if vizinho[0] >= 0 and vizinho[0] < 28: #len(gridAuxiliar[0])
                    if vizinho[1] >= 0 and vizinho[1] < 30: #len(gridAuxiliar)
                        if gridAuxiliar[vizinho[0]][vizinho[1]].get_F() == 20000000 or vizinho in lista_fechada: # 2d Verifique se o vértice adjacente pertence a lista fechada. Se sim, destarte.
                            continue #verifica o próximo vizinho, pula essa iteração
                        else: # Caso contrário, verifique se pertence a lista aberta.
                            if vizinho not in lista_aberta: # Se não pertence a lista aberta,
                                # Insira o vertice (vizinho) na lista aberta
                                lista_aberta.append(vizinho)
                                #Torne a célula analisada a célula pai
                                gridAuxiliar[vizinho[0]][vizinho[1]].set_Pai(atual)
                                gridAuxiliar[vizinho[0]][vizinho[1]].set_GdoPai(gridAuxiliar[atual[0]][atual[1]].get_G())
                                #Atualize os custos:
                                gridAuxiliar[vizinho[0]][vizinho[1]].set_G(atual, vizinho)
                                gridAuxiliar[vizinho[0]][vizinho[1]].set_H(destino, vizinho)
                                gridAuxiliar[vizinho[0]][vizinho[1]].set_F()
                            else: #Se pertence a lista aberta
                                for vertice in lista_aberta: #ver essa parte aqui !!
                                    if vizinho == vertice:
                                        if gridAuxiliar[vizinho[0]][vizinho[1]].get_G() < gridAuxiliar[vertice[0]][vertice[1]].get_G():
                                            gridAuxiliar[vizinho[0]][vizinho[1]].set_Pai(atual)
                                            gridAuxiliar[vizinho[0]][vizinho[1]].set_GdoPai(gridAuxiliar[atual[0]][atual[1]].get_G())
                                            # Atualize os custos:
                                            gridAuxiliar[vizinho[0]][vizinho[1]].set_G(atual, vertice)
                                            gridAuxiliar[vizinho[0]][vizinho[1]].set_H(destino, vertice)
                                            gridAuxiliar[vizinho[0]][vizinho[1]].set_F()
                                            print("oi")

        if atual == destino: #retornar a lista para percorrer até o destino
            caminho = []
            while(atual != origem):
                caminho.insert(0, atual)
                atual = gridAuxiliar[atual[0]][atual[1]].get_Pai()
            return caminho

    def set_target(self): #arrumar essa parte de alvo
        if self.forma == "blinky" or self.forma == "inky" or self.forma == "pinky":
            return self.programa.jogador.grid_pos
        else:
            if self.programa.jogador.grid_pos[0] > COLS // 2 and self.programa.jogador.grid_pos[1] > ROWS // 2:
                return vec(1, 1)
            if self.programa.jogador.grid_pos[0] > COLS // 2 and self.programa.jogador.grid_pos[1] < ROWS // 2:
                return vec(1, ROWS - 2)
            if self.programa.jogador.grid_pos[0] < COLS // 2 and self.programa.jogador.grid_pos[1] > ROWS // 2:
                return vec(COLS - 2, 1)
            else:
                return vec(COLS - 2, ROWS - 2)

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.programa.largura_quadradoGrid) + ESPACOS_JOGO//2+self.programa.largura_quadradoGrid//2,
                (self.grid_pos.y*self.programa.altura_quadradoGrid) + ESPACOS_JOGO//2+self.programa.altura_quadradoGrid//2)