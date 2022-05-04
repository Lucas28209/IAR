   
import threading
from matplotlib.pyplot import grid
import numpy as np
import time
import pygame as pg
import sys

class Dados():
    def __init__(self, diretorio):
        self.dados = np.loadtxt(diretorio) #leitura dos dados
        self.qntd_dados = len(self.dados) 
        self.dados_labels = list()

        self.le_dados()       

    def le_dados(self):       
        #print (self.dados)
        dados_labels = list()
        for i in self.dados:
            dados2 = i[0:-1], i[-1]*22    	    
            self.dados_labels.append(dados2)
    		#labels.append(label) 
    	    #print(dados_labels)
        #print(len(dados_labels))
        #return dados_labels, self.qnt_dados 
    

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
        
        if grid[x,y] is None:
            if self.carregando:
                self.largar()
        elif grid[x,y] is not None:
            if not self.carregando:
                self.pegar()

        self.x, self.y = self.posicao()
        self.itera -= 1
        #print(self.itera)


    '''
    def _pick(self):
        seen = self._neighbors(self.grid, self.x, self.y, n=self.r_)
        #print(seen)
        fi = self._avg_similarity(seen)
        sig = self._sigmoid(self.c, fi)
        f = 1 - sig
        rd = np.random.uniform(0.0, 1.0)
        #print("sig: " + str(sig) + "\npick: " + str(f) + "\nrd: " + str(rd) + "\n")

        if f >= rd:
            self.carrying = True
            self.data = self.grid[self.x, self.y]
            self.grid[self.x, self.y] = None
            return True
        return False

    
    def _drop(self):
        seen = self._neighbors(self.grid, self.x, self.y, n=self.r_)
        fi = self._avg_similarity(seen)
        f = self._sigmoid(self.c, fi)
        rd = np.random.uniform(0.0, 1.0)
        #print("drop: " + str(f) + "\nrd: " + str(rd) + "\n")

        if f >= rd:
            self.carrying = False
            self.grid[self.x, self.y] = self.data
            self.data = None
            return True
        return False


    def _avg_similarity(self, seen):
        s = 0
        shape = seen.shape[0]
        if self.carrying:
            data = self.data.get_attribute()
        else:
            data = self.grid[self.x, self.y].get_attribute()

        for i in range(shape):
            for j in range(shape):
                ret = 0
                if seen[i,j] != None:
                    ret = 1 - (euclidean(data,
                            seen[i,j].get_attribute()))/((self.alpha))
                    s += ret

        fi = s/(self.r_**2)
        if fi > 0: return fi
        else: return 0


    def _sigmoid(self, c, x):
        return ((1-np.exp(-(c*x)))/(1+np.exp(-(c*x))))

    '''

    def _calc_r_(self):
        self.r_ = 1
        for i in range(self.raio_visao):
            self.r_ = self.r_ + 2

    def get_carregando(self):
        return self.carregando




        

class AntProgram():
    def __init__(self, grid, qntd_dados, dados, raio_visao, num, itr, tam,sleep=0):
        self.size = int(grid)
        self.raio_visao = raio_visao
        self.num = num
        self.itr = itr
        self.tam = tam
        self.dados = dados
        self.n_dados = qntd_dados  #1 #criar dados
        #self.n_dados = len(dados_label)
        self.lista = list()
        self.sleep = sleep

        self.grid = np.empty((self.size, self.size), dtype=np.object_)
        self.distribui(self.grid, self.dados)
        #print(self.grid)
        
        self.cria_formigas(self.num, self.raio_visao, self.grid, self.itr // self.num)
    
    def cria_dados(self):
        pass

    '''def calc_alpha(self):
        s = 0
        for d1 in self.data:
            for d2 in self.data:
                s += euclidean(d1.get_attribute(), d2.get_attribute())
        return s/(len(self.data)**2)'''

    def distribui(self,grid,dados):
        for a in dados:
            i = np.random.randint(0, self.size)
            j = np.random.randint(0, self.size)
            while grid[i,j] != None:
                i = np.random.randint(0, self.size)
                j = np.random.randint(0, self.size)
            grid[i,j] = a
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
                #print(self.grid)
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
    dados = Dados('dados.txt')
    program = AntProgram(grid=(dados.qntd_dados*10)**0.5, qntd_dados=dados.qntd_dados, dados=dados.dados_labels, raio_visao=1, num=20, itr=5*10**6, tam=650,sleep=1)
    program.run()
    #print(grid)
    #Dados.le_dados('dados.txt')
    # mostrar os routlos de dados bidimensionais

