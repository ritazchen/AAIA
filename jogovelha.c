#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define tam 8

typedef struct peca{
	int cor; //codigo de cor
	char corString[10]; //nome da cor (semiotica)
	int x; //coordenada horizontal
	int y; //coordenada vertical
}Peca;

typedef struct tabuleiro{
	Peca** board; //estrutura do tabuleiro
}Tabuleiro;

Tabuleiro* inicializaTabuleiro(); //mistura algumas funções pra gerar o tabuleiro inicial
Peca getPeca(Tabuleiro* t,int x, int y); //troca a peca no tabuleiro
Peca recebeInformacao(Peca info); //passa tudo de uma estrutura peça pra outra
void moveTabuleiro(Tabuleiro* t, Peca x, Peca y);
void liberaTabuleiro(Tabuleiro* t); //free coletivo
void mostraTabuleiro(Tabuleiro* t); //printa o tabuleiro
void poePeca(Tabuleiro* t,int x, int y, int id); //id vai ser 1 pra branco, -1 pra preto.
void movePeca(Tabuleiro* t, Peca p, int xDestino, int yDestino); //troca as informa��es da pe�a
char getCharPeca(Peca p); //retorna um caracter da peca desejada (REPRESENTACAO VISUAL)
int setCor(Peca p); //gera uma string da cor da peca
void DEBUG_printaPeca(Peca p); //fun��o pra entregar os specs da pe�a //todas as fun��es debug v�o ser deletadas depois

int main (void){
	Tabuleiro* tab;
	tab = inicializaTabuleiro();
	mostraTabuleiro(tab);
	liberaTabuleiro(tab);
}

void movePeca(Tabuleiro* t, Peca p, int xDestino, int yDestino){
	char auxString[10];
	int auxX, auxY, auxCor;
	Peca aux, destino;
	destino = getPeca(t,xDestino,yDestino);
	moveTabuleiro(t,p,destino);
}

void DEBUG_printaPeca(Peca p){
	printf("Par Ordenado Cartesiano(x,y) = (%d,%d) Cor = %d\n",p.x,p.y,p.cor);
}

void moveTabuleiro(Tabuleiro* t,Peca x, Peca y){
	Peca aux = recebeInformacao(y);
	t->board[y.x][y.y] = recebeInformacao(t->board[x.x][x.y]);
	t->board[x.x][x.y] = recebeInformacao(aux);
}

Peca recebeInformacao(Peca info){
	Peca destino;
	destino.cor = info.cor;
	setCor(destino);
	destino.x = info.x;
	destino.y = info.y;
	return destino;
}

Peca getPeca(Tabuleiro* t, int x, int y){
	return t->board[x][y];
}

void mostraTabuleiro(Tabuleiro* t){ //deixar mais semioticamente viavel
	int i, j;
	printf("\n");
	for(i = 0; i < 8; i++){
		printf("[");
		for(j = 0; j < 8; j++){
			printf("| %c |",getCharPeca(t->board[i][j]));
		}
		printf("] %d \n\n",i);
	}
	for(i = 0; i < 8; i++){
		printf("  %d  ",i);
	}
}

char getCharPeca(Peca p){
	if(p.cor == 1){
		return 'b';
	}
	else if(p.cor == -1){
		return 'p';
	}
	else{
		return ' ';
	}
}

int setCor(Peca p){
	if(p.cor == 1){
		strcpy(p.corString,"Branco");
	}
	if(p.cor == -1){
		strcpy(p.corString,"Preto");
	}
	if(p.cor == 0){
		strcpy(p.corString,"  ");
	}
}

Tabuleiro* inicializaTabuleiro(){
	Tabuleiro* t;
	int i,j;
	int distribui;
	t = (Tabuleiro*)malloc(sizeof(Tabuleiro));
	t->board = (Peca**)malloc(sizeof(Peca*) * tam);
	for(i = 0; i < tam; i++){
		t->board[i] = (Peca*)malloc(sizeof(Peca) * tam);
	}
	for(i = 0; i < tam; i++){
		distribui = i%2;
		for(j = 0; j < tam; j++){
			if(distribui == 1 && i<3){
				poePeca(t,i,j,1); //poe as pecas brancas em cima
				distribui = 0;
			}
			else if(distribui == 1 && i>4){
				poePeca(t,i,j,-1); //poe as pecas pretas em baixo
				distribui = 0;
			}
			else{
				poePeca(t,i,j,0); //poe espaco vazio
				distribui++;
			}
		}
	}
	return t;
}

void poePeca(Tabuleiro* t,int x, int y, int id){
	t->board[x][y].cor = id;
	setCor(t->board[x][y]);
	t->board[x][y].x = x;
	t->board[x][y].y = y;
}

void liberaTabuleiro(Tabuleiro* t){
	free(t->board);
	free(t);
}
