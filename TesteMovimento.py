import numpy as np
import random as rn

direcoes = ['N','S','L','O']

def direcao():
    return direcoes[rn.randint(0,3)]    
    
def pegar_largar(i,j):
	cont = 0
	raio_visao = 1
	n_celulas = 8.0
	razao = 0.25
	formiga = 55
	
	if(copia[i-raio_visao][j] == 0): #oeste
		cont=cont+1
	if(copia[i][j+raio_visao] == 0): #sul
		cont=cont+1
	if(copia[i][j-raio_visao] == 0): #norte
		cont=cont+1
	if(copia[i+raio_visao][j] == 0): #leste
		cont=cont+1
	
	if(copia[i+raio_visao][j+raio_visao] == 0): #sudeste
		cont=cont+1
	if(copia[i+raio_visao][j-raio_visao] == 0): #nordeste
		cont=cont+1
	if(copia[i-raio_visao][j+raio_visao] == 0): #sudoeste
		cont=cont+1
	if(copia[i-raio_visao][j-raio_visao] == 0): #noroeste
		cont=cont+1
	
	if ((cont/n_celulas) == razao and copia[i][j] == 1):
		formiga = copia[i][j]
		copia[i][j] = 0		
	print(formiga)	
	    

posicao = np.zeros(shape=(10,10) , dtype=int) # random.randint(9, size=(10,10))
posicao[3][3] = 1
posicao[7][7] = 1
copia = posicao.copy() 
i = rn.randint(0,len(posicao)-1)
j = rn.randint(0,len(posicao)-1)

print(posicao)

dir = direcao()
for k in range(1,100):
    aux = rn.randint(1,100)

    if (aux%2 == 0):
        dir = direcao() 
    
    #print(dir)
    #print(i,j)      
    
    if (dir == 'N' and i+1 < len(posicao)):    
        posicao[i][j] = copia[i][j]  
        i = i+1       
    elif (dir == 'S' and i-1 > 0):
        posicao[i][j] = copia[i][j]
        i=i-1        
    elif (dir == 'L' and j+1 < len(posicao)):
        posicao[i][j] = copia[i][j]
        j=j+1        
    elif (dir == 'O' and j-1 > 0):
        posicao[i][j] = copia[i][j]
        j=j-1        
    posicao[i][j] = 22
    pegar_largar(i,j)
    #print("\n",posicao)
print('\n', copia)




#cheio = true 
#raio de visao = 1
# substituir "1" por "raio_de_visao"
#pegar - if (posicao[i+1][j] == 0)
# if(posicao[i][j-1] == 0) and # if(posicao[i+1][j+1] == 0) and if(posicao[i+1][j-1] == 0) and if(posicao[i-1][j+1] == 0) and if(posicao[i-1][j-1] == 0)  

# if(o número de células com 0 for igual a 2/8 das céluas do raio de visao): pegue

# o agente terá dois estados
# fazer o cálculo de pegar/largar
# fazer o desenvolviemtento 
# tirar os zeros da matriz no txt
# qnd o sistema parar, nenhuma formiga pode estar segurando itens 
