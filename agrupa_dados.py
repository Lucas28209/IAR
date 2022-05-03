   
import threading
from matplotlib.pyplot import grid
import numpy as np
import time
import pygame as pg
import sys


class Dados():
    def le_dados(diretorio):
        #leitura dos dados
        dados = np.loadtxt(diretorio)
        #print (self.dados)
        dados_labels = list()
        for i in dados:
            dados2 = i[0:-1], i[-1]*22    	    
            dados_labels.append(dados2)
    		#labels.append(label) 
    	    #print(dados_labels)
        #print(len(dados_labels))
        return dados_labels, len(dados_labels) 

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
        #self.c              = self.raio_visao*10
        self.max_step_size  = (self.grid.shape[0] // 2) + 1
        #print(self.max_step_size)
        
        #self.alpha          = alpha

    def posicao(self):
        #print("passo",self.max_step_size, self.grid.shape[0])
        tam_passo = np.random.randint(1, self.max_step_size)
        tam_grid = self.grid.shape[0]
        x = self.x + np.random.randint(-1,2) #np.random.randint(-1 * tam_passo, 1*tam_passo+1)
        y = self.y + np.random.randint(-1,2) #np.random.randint(-1 * tam_passo, 1*tam_passo+1)

        #print(x,y)
        if x < 0: x=0 #x+1 #if x < 0: x = tam_grid + x
        if x >= tam_grid: x=(tam_grid-1) #x-1 #if x >= tam_grid: x = x - tam_grid
        if y < 0: y=0 #y+1 #if y < 0: y = tam_grid + y
        if y >= tam_grid: y=(tam_grid-1) #y-1 #if y >= tam_grid: y = y - tam_grid
                   
        return x,y
    '''
    def vizinhos(self, vet, x,y, n=3):
        #print(vet)
        vet = np.roll(np.roll(vet, shift=-x+1, axis=0), shift=-y+1, axis=1)

        #print(vet[:n,:n])
        return vet[:n,:n]
    '''
    def conta_vizinhos(self, vet, i,j):
        cont = 0
        #raio_visao = raio      
        for x in range(1,self.raio_visao+1):
            for w in range(1,self.raio_visao+1):
                #print(x)
                if (vet[i][j] != None): #centro
                    cont=cont+1
                if(i > 0 and vet[i-x][j] != None): #oeste
                    cont=cont+1
                if(j < vet.shape[0]-self.raio_visao and vet[i][j+w] != None): #sul
                    cont=cont+1
                if(j > 0 and vet[i][j-w] != None): #norte
                    cont=cont+1
                if(i < vet.shape[0]-self.raio_visao and vet[i+x][j] != None): #leste
                    cont=cont+1

                if(i < vet.shape[0]-self.raio_visao and j < vet.shape[0]-self.raio_visao and vet[i+x][j+w] != None): #sudeste
                    cont=cont+1
                if(i < vet.shape[0]-self.raio_visao and j > 0 and vet[i+x][j-w] != None): #nordeste
                    cont=cont+1
                if(i > 0 and j < vet.shape[0]-self.raio_visao and vet[i-x][j+w] != None): #sudoeste
                    cont=cont+1
                if(i > 0 and j > 0 and vet[i-x][j-w] != None): #noroeste
                    cont=cont+1
        return cont

    def pegar(self):
        #visao = self.vizinhos(self.grid, self.x, self.y, n=self.r_ )
        #qntd = self.conta(visao)
        #print(visao, qntd)
        #print("tamanho = ", self.r_)
        visao = (self.r_)**2
        qntd = self.conta_vizinhos(self.grid, self.x, self.y)
        # prob = ()
        if ((float(qntd)/float(visao))  <= (np.random.uniform(0.0, 1.0))):
            self.carregando = True
            self.data = self.grid[self.x, self.y]
            self.grid[self.x, self.y] = None
            return True
        return False

    def largar(self):
        #print(self.r_)
        visao = (self.r_)**2
        qntd = self.conta_vizinhos(self.grid, self.x, self.y)
        #print("tamanho = ", visao)
        #print(qntd)
        #print(float(qntd)/float(visao.size))
        if ( (float(qntd)/ float(visao))**2  >= (np.random.uniform(0.0, 1.0))):
            self.carregando = False
            self.grid[self.x, self.y] = self.data
            self.data = None
            return True
        return False
        
    '''
    def conta(self,visao):
        qntd = 0
        for i in range (visao.shape[0]):
            for j in range (visao.shape[0]):
                if visao[i][j] != None:
                    qntd = qntd+1
        return qntd
    '''


   
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
        #print(self.itera)

    def _calc_r_(self):
        self.r_ = 1
        for i in range(self.raio_visao):
            self.r_ = self.r_ + 2

    def get_carregando(self):
        return self.carregando




        

class AntProgram():
    def __init__(self, grid, raio_visao, num, itr, tam,sleep=0):
        self.size = grid
        self.raio_visao = raio_visao
        self.num = num
        self.itr = itr
        self.tam = tam
        self.dados, self.n_dados = Dados.le_dados(diretorio='dados.txt')  #1 #criar dados
        #self.n_dados = len(dados_label)
        self.lista = list()
        self.sleep = sleep

        self.grid = np.empty((self.size, self.size), dtype=np.object_)
        self.distribui(self.grid)
        #print(self.grid)
        
        self.cria_formigas(self.num, self.raio_visao, self.grid, self.itr // self.num)
    
    def cria_dados(self):
        pass

    def distribui(self,grid):
        for a in range(self.n_dados):
            i = np.random.randint(0, self.size)
            j = np.random.randint(0, self.size)
            grid[i,j] = self.dados[a]
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
                    data = self.grid[i,j]
                    ret[i,j] = data[-1] #50 #cor dos dados
                else:
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
    program = AntProgram(grid=50, raio_visao=1, num=20, itr=5*10**6, tam=650,sleep=1)
    program.run()
    #print(grid)
    Dados.le_dados('dados.txt')
    # mostrar os routlos de dados bidimensionais

