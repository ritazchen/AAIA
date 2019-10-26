#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define tam 8

typedef struct peca{
	int cor;
	char corString[10];
	int x;
	int y;
}Peca;

typedef struct tabuleiro{
	Peca** board;
}Tabuleiro;

Tabuleiro* inicializaTabuleiro();
void liberaTabuleiro(Tabuleiro* t);
void mostraTabuleiro(Tabuleiro* t);
void poePeca(Tabuleiro* t,int x, int y, int id); //id vai ser 1 pra branco, -1 pra preto.
char getCharPeca(Peca p); //retorna um caracter da peça desejada (REPRESENTAÇÃO VISUAL)
int setCor(Peca p); //gera uma string da cor da peça

int main (void){
	Tabuleiro* tab;
	tab = inicializaTabuleiro();
	mostraTabuleiro(tab);
	liberaTabuleiro(tab);
}

void mostraTabuleiro(Tabuleiro* t){ //deixar mais semioticamente viável
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
		strcpy(p.corString," ");
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
				poePeca(t,i,j,1); //poe as peças brancas em cima
				distribui = 0;
			}
			else if(distribui == 1 && i>4){
				poePeca(t,i,j,-1); //poe as peças pretas em baixo
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
