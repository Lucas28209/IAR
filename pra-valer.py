import threading
from matplotlib.pyplot import grid
import numpy as np
import time
import pygame as pg
import sys

class Formiga():
    def __init__(self, x,y,raio_visao, grid,its):
        self.grid = grid
        self.raio_visao = raio_visao
        self.x = x
        self.y = y
        self.itera = its
        self._calc_r_()
        self.carregando = False
        self.data = None
        self.c              = self.raio_visao*10
        self.max_step_size  = self.grid.shape[0] // 2 + 1
        
        #self.alpha          = alpha

    def posicao(self):
        tam_passo = np.random.randint(1, self.max_step_size)
        tam_grid = self.grid.shape[0]
        x = self.x + np.random.randint(-1 * tam_passo, 1*tam_passo+1)
        y = self.y + np.random.randint(-1 * tam_passo, 1*tam_passo+1)
        if x < 0: x = tam_grid + x
        if x >= tam_grid: x = x - tam_grid
        if y < 0: y = tam_grid + y
        if y >= tam_grid: y = y - tam_grid
        return x,y

    def vizinhos(self, vet, x,y, n=3):
        vet = np.roll(np.roll(vet, shift=-x+1, axis=0), shift=-y+1, axis=1)
        print(vet[:n,:n])
        return vet[:n,:n]
    
    def pegar(self):
        if conta_vizinhos():
            return True
        else:
            return False
            
    def largar(self):
        if conta_vizinhos():
            return True
        else:
            return False        
            
    def conta_vizinhos(self):
    	cont = 0
	self.raio_visao = 1
	n_celulas = raio_visao*8
	
	
	if(self.grid[i-raio_visao][j] == 0): #oeste
		cont=cont+1
	if(self.grid[i][j+raio_visao] == 0): #sul
		cont=cont+1
	if(self.grid[i][j-raio_visao] == 0): #norte
		cont=cont+1
	if(self.grid[i+raio_visao][j] == 0): #leste
		cont=cont+1
	
	if(self.grid[i+raio_visao][j+raio_visao] == 0): #sudeste
		cont=cont+1
	if(self.grid[i+raio_visao][j-raio_visao] == 0): #nordeste
		cont=cont+1
	if(self.grid[i-raio_visao][j+raio_visao] == 0): #sudoeste
		cont=cont+1
	if(self.grid[i-raio_visao][j-raio_visao] == 0): #noroeste
		cont=cont+1
	
	if ((cont/n_celulas) > np.random.uniform(0.0,1.0)):
		return True
	else:
		return False
		        

    
    
    def run(self):
        self.andar()
        if self.itera <=0 and self.carregando:
            while self.carregando:
                self.andar()
    
    def andar(self):
        grid = self.grid
        x,y = self.x, self.y
        
        if grid[x,y] == None:
            if self.carregando:
                self.largar()
        elif grid[x,y] != None:
            if not self.carregando:
                self.pegar()

        self.x, self.y = self.posicao()
        self.itera -= 1

    def probabilidade():
        pass

    def _calc_r_(self):
        self.r_ = 1
        for i in range(self.raio_visao):
            self.r_ = self.r_ + 2

    def get_carregando(self):
        return self.carregando




        

class AntProgram():
    def __init__(self, grid, raio_visao, num, itr, tam, n_dados):
        self.size = grid
        self.raio_visao = raio_visao
        self.num = num
        self.itr = itr
        self.tam = tam
        self.dados = 1 #criar dados
        self.n_dados = n_dados
        self.lista = list()
        self.sleep = 3

        self.grid = np.empty((self.size, self.size), dtype=np.object)
        self.distribui(self.grid, self.dados)
        print(self.grid)
        
        self.cria_formigas(self.num, self.raio_visao, self.grid, self.itr // self.num)
    
    def cria_dados(self):
        pass

    def distribui(self,grid, dados):
        for a in range(self.n_dados):
            i = np.random.randint(0, self.size)
            j = np.random.randint(0, self.size)
            grid[i][j] = self.dados
        #print(self.grid)

      

    def cria_formigas(self, num, raio_visao, grid, its):
        for i in range(num):
            x = np.random.randint(0,self.size-1)
            y = np.random.randint(0,self.size-1)
            formiga = Formiga(x,y,raio_visao, grid,its)
            self.lista.append(formiga)

    def inicio(self):
        time.sleep(self.sleep)
        for i in range(self.itr // self.num):
            for formiga in self.lista:
                formiga.run()
        l = list()
        for formiga in self.lista:
            l.append(formiga.get_carregando())
        print(l)

    def matriz(self):
        ret = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i,j] != None:
                    ret[i,j] = self.grid[i,j]
        return ret
        

    def run(self):
        pg.init()
        tela = pg.display.set_mode((self.tam, self.tam))
        tela.set_alpha(None)
        #print(np.count_nonzero(self.grid != None))
        t = threading.Thread(target=self.inicio)
        t.daemon=True
        t.start()

        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT: sys.exit()
            vetor = self.matriz()
            formigueiro = pg.surfarray.make_surface(vetor)
            n_formigueiro = pg.transform.scale(formigueiro, (self.tam, self.tam))
            tela.blit(n_formigueiro, (0,0))
            pg.display.flip()


if __name__ == "__main__":
    program = AntProgram(grid=100, raio_visao=1, num=5, itr=100, tam=500, n_dados=40)
    program.run()
    print(grid)
