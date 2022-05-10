   
import threading
from matplotlib.pyplot import grid
import numpy as np
import time
import pygame as pg
import sys
from scipy.spatial.distance import euclidean

class Dados():
    def __init__(self, diretorio):
        self.dados = np.loadtxt(diretorio) #leitura dos dados
        self.qntd_dados = len(self.dados) 
        self.dados_labels = list()
        self.alpha = self.calcula_alpha()
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
    
    def calcula_alpha(self):
        somatorio = 0
        for d1 in self.dados:
            for d2 in self.dados:
                somatorio += euclidean(d1[0:-1], d2[0:-1])
        return somatorio/((self.qntd_dados)**2)
    

class Formiga():
    def __init__(self, x,y,raio_visao, grid,its,alpha, n_dados):
        self.grid = grid
        self.raio_visao = raio_visao
        self.x = x
        self.y = y
        self.itera = its
        self._calc_r_()
        self.carregando = False
        self.data = None
        #self.c              = self.raio_visao*10
        self.max_step_size  = self.grid.shape[0]//2 +1 #int((20*n_dados)**0.5)
        #print(self.max_step_size)
        self.alpha = alpha

    def posicao(self):
        #print("passo",self.max_step_size, self.grid.shape[0])
        tam_passo = np.random.randint(1, self.max_step_size)
        tam_grid = self.grid.shape[0]
        x = self.x + np.random.randint(-1 * tam_passo, 1*tam_passo+1) #np.random.randint(-1,2)
        y = self.y + np.random.randint(-1 * tam_passo, 1*tam_passo+1) #np.random.randint(-1,2)

        #print(x,y)
        if x < 0: x = tam_grid + x# x=0 #x+1 #if x < 0: 
        if x >= tam_grid: x = x - tam_grid#if x >= tam_grid: x=(tam_grid-1) #x-1 
        if y < 0: y = tam_grid + y#if y < 0: y=0 #y+1 
        if y >= tam_grid: y = y - tam_grid#if y >= tam_grid: y=(tam_grid-1) #y-1 
                   
        return x,y
    
    def vizinhos(self, vet, x,y, n=3):
        #print(vet)
        vet = np.roll(np.roll(vet, shift=-x+1, axis=0), shift=-y+1, axis=1)

        #print(vet[:n,:n])
        return vet[:n,:n]
    '''
    def conta_vizinhos(self, vet, i,j):
        #cont = 0.0
        soma = 0
        #print("alpha = ",self.alpha)
        #raio_visao = raio  
        if self.carregando:
            centro = self.data[0:-1]
        else:
            centro = self.grid[self.x, self.y][0:-1]

        #if vet[i][j] == None:
         #   centro = 0
        #else:
         #   centro = vet[i][j][0:-1]    

        for x in range(1,self.raio_visao+1):
            for w in range(1,self.raio_visao+1):
                #print(x)
                #if (vet[i][j] != None): #centro
                    #cont=cont+ (1 - (euclidean(vet[i][j][0:-1], vet[i][j][0:-1]) / self.alpha) )
                #else:
                    #cont=cont+ (1 - (euclidean(0, vet[i][j][0:-1]) / self.alpha) )
                cont = 0
                if(i > 0):
                    if vet[i-x][j] != None: #oeste
                        aux = 1 - (euclidean(centro, vet[i-x][j][0:-1]) / self.alpha) 
                        if aux>0:
                            cont= aux
                            soma += cont
                        else: return 0 
                    # else: 
                    #     if (1 - (euclidean(centro, 0) / self.alpha)) > 0:
                    #         cont=(1 - (euclidean(centro, 0) / self.alpha))
                    #         soma += cont
                    #     else: return 0
                            
                
                if(j < vet.shape[0]-self.raio_visao): 
                    if vet[i][j+w] != None: #sul
                        aux = 1 - ((euclidean(centro, vet[i][j+w][0:-1]) / self.alpha) )
                        if aux>0:
                            cont=aux
                            soma += cont
                        else: return 0
                    # else: 
                    #     if (1 - (euclidean(centro, 0) / self.alpha)) > 0:
                    #         cont=(1 - (euclidean(centro, 0) / self.alpha))
                    #         soma += cont
                    #     else: return 0
                
                if(j > 0): 
                    if vet[i][j-w] != None: #norte
                        aux = 1 - ((euclidean(centro, vet[i][j-w][0:-1]) / self.alpha) )
                        if aux>0:
                            cont=aux
                            soma += cont
                        else: return 0
                    # else: 
                    #     if (1 - (euclidean(centro, 0) / self.alpha)) > 0:
                    #         cont=(1 - (euclidean(centro, 0) / self.alpha))
                    #         soma += cont
                    #     else: return 0
                
                if(i < vet.shape[0]-self.raio_visao): 
                    if vet[i+x][j] != None: #leste
                        aux = 1 - ((euclidean(centro, vet[i+x][j][0:-1]) / self.alpha) )
                        if aux>0:  
                            cont=aux
                            soma += cont
                        else: return 0
                    # else: 
                    #     if (1 - (euclidean(centro, 0) / self.alpha)) > 0:
                    #         cont=(1 - (euclidean(centro, 0) / self.alpha))
                    #         soma += cont
                    #     else: return 0

                if(i < vet.shape[0]-self.raio_visao and j < vet.shape[0]-self.raio_visao ):
                    if vet[i+x][j+w] != None: #sudeste
                        aux = 1 - ((euclidean(centro, vet[i+x][j+w][0:-1]) / self.alpha) )
                        if aux>0:
                            cont=aux
                            soma += cont
                        else: return 0
                    # else: 
                    #     if (1 - (euclidean(centro, 0) / self.alpha)) > 0:
                    #         cont=(1 - (euclidean(centro, 0) / self.alpha))
                    #         soma += cont
                    #     else: return 0

                if(i < vet.shape[0]-self.raio_visao and j > 0 ):
                    if vet[i+x][j-w] != None: #nordeste
                        aux = 1 - ((euclidean(centro, vet[i+x][j-w][0:-1]) / self.alpha) )
                        if aux>0:
                            cont=aux
                            soma += cont
                        else: return 0
                    # else: 
                    #     if (1 - (euclidean(centro, 0) / self.alpha)) > 0:
                    #         cont=(1 - (euclidean(centro, 0) / self.alpha))
                    #         soma += cont
                    #     else: return 0

                if(i > 0 and j < vet.shape[0]-self.raio_visao): 
                    if vet[i-x][j+w] != None: #sudoeste
                        aux = 1 - ((euclidean(centro, vet[i-x][j+w][0:-1]) / self.alpha) )
                        if aux>0:
                            cont=aux
                            soma += cont
                        else: return 0
                    # else: 
                    #     if (1 - (euclidean(centro, 0) / self.alpha)) > 0:
                    #         cont=(1 - (euclidean(centro, 0) / self.alpha))
                    #         soma += cont
                    #     else: return 0

                if(i > 0 and j > 0): 
                    if vet[i-x][j-w] != None: #noroeste
                        aux =  1 - ((euclidean(centro, vet[i-x][j-w][0:-1]) / self.alpha) )
                        if aux>0:
                            cont=aux
                            soma += cont
                        else: return 0
                    # else: 
                    #     if (1 - (euclidean(centro, 0) / self.alpha)) > 0:
                    #         cont=(1 - (euclidean(centro, 0) / self.alpha))
                    #         soma += cont
                    #     else: return 0
        #retorna o somatório de (1-(distancias)/alpha) das distâcnias
        #print ("soma= " ,soma)
        return soma 
    '''

    def media(self, som_dist):
        soma = 0
        if self.carregando:
            centro = self.data[0:-1]
        else:
            centro = self.grid[self.x, self.y][0:-1]
        
        for i in range(som_dist.shape[0]):
            for j in range(som_dist.shape[0]):
                conta = 0
                if som_dist[i,j] != None:
                    conta = 1 - (euclidean(centro, som_dist[i,j][0:-1]))/((self.alpha))
                    soma += conta
        return soma
        
       
    def calculos(self):
        visao = (self.r_)**2
        som_dist = self.vizinhos(self.grid, self.x, self.y, self.r_ )#self.conta_vizinhos(self.grid, self.x, self.y)
        f = (self.media(som_dist))/visao
        #print(f)
        if f > 0:
            return f
        else:
            return 0

    ''' Normalizes the _avg_similarity function '''
    def _sigmoid(self, c, x):
        return ((1-np.exp(-(c*x)))/(1+np.exp(-(c*x))))
    
    def pegar(self):
        f = self.calculos()     
        #print("f do pegar= ",f)  
        
        #sig = self._sigmoid(self.raio_visao*10,f)
        #probP = 1 -sig
        #k1 = 0.1
        k1 = 0.05 #este número n pode ser muito grande
        probP = (k1/(k1+f))**2   

        #if f <= 1.0:
        #    probP = 0.9
        #else:
        #    probP = (1/f**2) 
        
        #print("P=",probP)

        if ((probP)  >= (np.random.uniform(0.0, 1.0))):            
            self.carregando = True
            self.data = self.grid[self.x, self.y]
            self.grid[self.x, self.y] = None
            return True
        return False

    def largar(self):
        f = self.calculos()
        #print("f do largar= ",f)  
        
        #probL = self._sigmoid(self.raio_visao*10, f)
        
        k2 = 0.15 #0.15
        #probL = (f/(k2+f))**2
        if f < k2:
            probL = 5*f
        else:
            probL = 1
        
        #print("L=",probL)

        if (probL >= (np.random.uniform(0.0, 1.0))):            
            self.carregando = False
            self.grid[self.x, self.y] = self.data
            self.data = None
            return True
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
        #print(self.itera)

    def _calc_r_(self):
        self.r_ = 1
        for i in range(self.raio_visao):
            self.r_ = self.r_ + 2

    def get_carregando(self):
        return self.carregando




        

class AntProgram():
    def __init__(self, grid, qntd_dados, dados, alpha, raio_visao, num, itr, tam,sleep=0):
        self.size = int(grid)
        self.raio_visao = raio_visao
        self.num = num
        self.itr = itr
        self.tam = tam
        self.dados = dados
        self.n_dados = qntd_dados  #1 #criar dados
        self.alpha = alpha
        #self.n_dados = len(dados_label)
        self.lista = list()
        self.sleep = sleep

        self.grid = np.empty((self.size, self.size), dtype=np.object_)
        self.distribui(self.grid, self.dados)
        #print(self.grid)
        
        self.cria_formigas(self.num, self.raio_visao, self.grid, self.itr // self.num, self.alpha, self.n_dados)
    

    def distribui(self,grid,dados):
        for a in dados:
            i = np.random.randint(0, self.size)
            j = np.random.randint(0, self.size)
            while grid[i,j] != None:
                i = np.random.randint(0, self.size)
                j = np.random.randint(0, self.size)
            grid[i,j] = a
        #print(self.grid)

      

    def cria_formigas(self, num, raio_visao, grid, its, alpha, n_dados):
        for i in range(num):
            x = np.random.randint(0,self.size-1)
            y = np.random.randint(0,self.size-1)
            formiga = Formiga(x,y,raio_visao, grid,its, alpha, n_dados)
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
                #print("oi")
                if self.grid[i,j] != None:
                    #print("oi")
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
    print(dados.alpha)
    program = AntProgram(grid=50, qntd_dados=dados.qntd_dados, dados=dados.dados_labels, alpha=dados.alpha, raio_visao=1, num=20, itr=2000*dados.qntd_dados, tam=650,sleep=1)
    program.run()
    #print(grid)
    #Dados.le_dados('dados.txt')
    # mostrar os routlos de dados bidimensionais
    # (dados.qntd_dados*10)**0.5


