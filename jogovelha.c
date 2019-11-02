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

Tabuleiro* inicializaTabuleiro(); //mistura algumas funcoes pra gerar o tabuleiro inicial
Peca getPeca(Tabuleiro* t,int x, int y); //troca a peca no tabuleiro
Peca recebeInformacao(Peca info); //passa tudo de uma estrutura peca pra outra
void moveTabuleiro(Tabuleiro* t, Peca x, Peca y);
void liberaTabuleiro(Tabuleiro* t); //free coletivo
void mostraTabuleiro(Tabuleiro* t); //printa o tabuleiro
void poePeca(Tabuleiro* t,int x, int y, int id); //id vai ser 1 pra branco, -1 pra preto.
void movePeca(Tabuleiro* t, Peca p, int xDestino, int yDestino); //troca as informacoes da peca
void removePeca(Tabuleiro* t, int x, int y); //remove uma peca comida
void processaMovimento(Tabuleiro* t); //função que recebe uma entrada do usuario e trata o movimento
void clr(); //limpa tela
char getCharPeca(Peca p); //retorna um caracter da peca desejada (REPRESENTACAO VISUAL)
char* getMovimentos(Peca p); //retorna os movimentos possiveis e pede para o usuario seleciona-los
int setCor(Peca p); //gera uma string da cor da peca
int getID(Peca p); //pega a ID da cor da peca
int isCome(Tabuleiro* t, Peca p, Peca alvo); //verifica se é um movimento normal, caso seja retorna 0, ou se é um movimento que come outra peca, retornando 1, caso seja invalido, retorna -1.
int direcao(Peca p, Peca alvo); //funcao pra ver se o alvo ta a esquerda ou direita da peca original (-1 esquerda, 1 direita)
int atrasVazio(Tabuleiro* t, Peca p,Peca alvo, int dir); //retorna 1 se a casa atras do alvo ta vazia, 0 se tem alguem, -1 se a casa de tras nao existir
int isVencedor(Tabuleiro *t); //retorna 1 se brancas vencem, -1 se pretas vencem, 0 se ninguem venceu
int isPeca(Peca p); //verifica se e uma peca ou um espaco (1 se peca, 0 espaco)
int getX(Peca p); //retorna X (linha que a peca ta)
int getY(Peca p); //retorna Y (coluna q a peca ta)
void DEBUG_printaPeca(Peca p); //funcao pra entregar os specs da peca //todas as funcoes debug vao ser deletadas depois

int main (void){
	Tabuleiro* tab;
	int finaliza = 0;
	tab = inicializaTabuleiro();
	while(isVencedor(tab) == 0 && finaliza != 42){ //game loop (remover a variavel finaliza [unicamente pra parar o while quando eu quiser])
		mostraTabuleiro(tab);
		finaliza = 42;
	}
	liberaTabuleiro(tab);
}

void processaMovimento(Tabuleiro* t){
	int x, y; //coordenadas do par ordenado inserido pelo usuario
	char *moves;
	int intString; //atoi vai gerar um numero de duas casas, dezenas é x, unidades y
	int newX, newY; 
	Peca movida, destino;
	printf("Por favor, insira as coordenadas da peca que deseja mover na ordem a seguir: (linha, coluna)\n");
	scanf("%d %d",&x,&y);
	movida = getPeca(t,x,y);
	moves = getMovimentos(movida);
	intString = atoi(moves);
	newX = intString / 10;
	newY = intString % 10;
	movePeca(t,movida,newX,newY); //a partir daqui, o movimento já ta feito, mas tem que ver se pode comer outra peça e se o usuario deseja isso
	destino = getPeca(t,newX,newY);
	
	//finalizar com excecoes pra caso seja comer e o movimento em si
}

char* getMovimentos(Peca p){
	int x1 = getX(p);
	int x2 = x1;
	int validador;
	char *moves;
	moves = (char*)malloc(sizeof(char) * 2);
	printf("Movimentos possiveis: [1] (%d,%d) , [2] (%d,%d). Insira o numero do movimento desejado.\n",--x1,getY(p),++x2,getY(p));
	scanf("%d",&validador);
	if(validador == 1){
		moves[0] = x1;
		moves[1] = getY(p);
	}
	if(validador == 2){
		moves[0] = x2;
		moves[1] = getY(p);
	}
	return *moves;
}

int isCome(Tabuleiro* t,Peca p, Peca alvo){
	if(getID(p) != getID(alvo)){//verifica se uma peca nao ta tentando mover contra outra do mesmo tipo
		if(getID(p) == 0 || getID(alvo) == 0){ //cai nesse laço se alguma casa (ou p, ou alvo) for vazia.
			return 0;
		}
		else if(getID(p) + getID(alvo) == 0){ //caso seja um movimento de comer valido, a soma do ID de uma peça preta -1 e de uma branca 1 sempre vai dar zero
			if(atrasVazio(t,p,alvo,direcao(p,alvo)) == 1){
				return 1;
			}
		}
		else{
			return -1;
		}
	}
}

void removePeca(Tabuleiro* t, int x, int y){
	t->board[x][y].cor = 0;
	setCor(t->board[x][y]);
}

int atrasVazio(Tabuleiro* t, Peca p, Peca alvo, int dir){ 
	int auxX = getX(alvo);
	int auxY = getY(alvo);
	if(getX(p) > auxX){ //caso caia aqui, p esta abaixo do alvo
		if(dir == -1){// caso esquerda
			if(auxX != 0 && auxY != 0){ //verifica se a casa acima a esquerda existe
				auxX--;
				auxY--;
				if(isPeca(t->board[auxX][auxY]) == 0){
					return 1;
				}
				else{
					return 0;
				}
			}
			else{
				return -1;
			}
		}
		if(dir == 1){//caso direita
			if(auxX != 0 && auxY != 7){ //verifica se a casa acima a direita existe
				auxX--;
				auxY++;
				if(isPeca(t->board[auxX][auxY]) == 0){
					return 1;
				}
				else{
					return 0;
				}	
			}
			else{
				return -1;
			}
		}
	}
	else{ //caso caia aqui, p esta acima do alvo
		if(dir == -1){// caso esquerda
			if(auxX != 7 && auxY != 0){ //verifica se a casa abaixo a esquerda existe
				auxX++;
				auxY--;
				if(isPeca(t->board[auxX][auxY]) == 0){
					return 1;
				}
				else{
					return 0;
				}	
			}
			else{
				return -1;
			}
		}
		else{ //caso direita
			if(auxX != 7 && auxY != 7){ //verifica se a casa abaixo a direita existe
				auxX++;
				auxY++;
				if(isPeca(t->board[auxX][auxY]) == 0){
					return 1;
				}
				else{
					return 0;
				}	
			}
			else{
				return -1;
			}
		}
	}
}

int isPeca(Peca p){
	if(p.cor == 1 || p.cor == -1){
		return 1;
	}
	else{
		return 0;
	}
}

int direcao(Peca p, Peca alvo){
	if(getY(p) > getY(alvo)){
		return -1;
	}
	else{
		return 1;
	}
}

void movePeca(Tabuleiro* t, Peca p, int xDestino, int yDestino){
	char auxString[10];
	int auxX, auxY, auxCor;
	Peca aux, destino;
	destino = getPeca(t,xDestino,yDestino);
	if(isCome(t,p,destino) == 1){
		int auxX = getX(destino);
		int auxY = getY(destino);
		int dir = direcao(p,destino);
		if(getX(p) > auxX){ //caso caia aqui, p esta abaixo do alvo
			if(dir == -1){// caso esquerda
				if(auxX != 0 && auxY != 0){ //verifica se a casa acima a esquerda existe
					auxX--;
					auxY--;
				}
			}
			if(dir == 1){//caso direita
				if(auxX != 0 && auxY != 7){ //verifica se a casa acima a direita existe
					auxX--;
					auxY++;
				}
			}
		}
		else{ //caso caia aqui, p esta acima do alvo
			if(dir == -1){// caso esquerda
				if(auxX != 7 && auxY != 0){ //verifica se a casa abaixo a esquerda existe
					auxX++;
					auxY--;
				}
			}
			else{ //caso direita
				if(auxX != 7 && auxY != 7){ //verifica se a casa abaixo a direita existe
					auxX++;
					auxY++;
				}
			}
		}
		destino = getPeca(t,auxX,auxY);
		removePeca(t,xDestino,yDestino);
	}
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

int getX(Peca p){
	return p.x;
}

int getY(Peca p){
	return p.y;
}

int getID(Peca p){
	return p.cor;
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

int isVencedor(Tabuleiro *t){
	int i, j;
	int temBrancas = 0;
	int temPretas = 0;
	for(i = 0; i < tam; i++){
		for(j = 0; j < tam; j++){
			if(getID(t->board[i][j]) == 1){
				temBrancas = 1;
			}
			else if(getID(t->board[i][j]) == -1){
				temPretas = 1;
			}
		}
	}
	if(temBrancas == 0){
		return -1; //pretas vencem
	}
	else if(temPretas == 0){
		return 1; //brancas vencem
	}
	else{
		return 0; //jogo ainda não acabou
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

void clr(){
	system("@cls||clear");
}
