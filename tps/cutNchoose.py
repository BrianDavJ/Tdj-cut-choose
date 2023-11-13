import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sabores = [3, 2, 1]
test=0
if test==1:
    funcion_de_valoracion=pd.read_csv("funcion_gusto.txt")
else:
    funcion_de_valoracion=pd.read_csv("funcion_gusto2.txt")

N=100
np.random.seed(41)

results = [] 

for i in range(N):
    T=np.random.randint(3, 15)
    torta = np.random.choice(sabores, size=T)    
    preferencias_1 = funcion_de_valoracion['jug1'].argsort()[::-1].values
    cuanto_prefiere_1 = funcion_de_valoracion['jug1']
    preferencias_2 = funcion_de_valoracion['jug2'].argsort()[::-1].values
    cuanto_prefiere_2 = funcion_de_valoracion['jug2']

    current_value = torta[0]
    current_chain_length = 0
    
    longest_chains = {1: [0,-1], 2: [0,-1], 3: [0,-1]}
    current_value = torta[0]
    current_chain_length = 1
    inicio=0

    for j, value in enumerate(torta[1:], start=0):
        if value == current_value:
            current_chain_length += 1
        else:
            current_value = value
            current_chain_length = 1
            inicio=j

        if current_chain_length > longest_chains[value][0]:
            longest_chains[value] = (current_chain_length, inicio)
    total2=0
    total1=0
    for j in range(T):
        sabor=torta[j]-1
        total1+=funcion_de_valoracion.loc[sabor,'jug1']
        total2+=funcion_de_valoracion.loc[sabor,'jug2']
    actual_2=1
    actual_1=0
    epsilon=np.inf
    if (longest_chains[preferencias_1[0]+1][0]*cuanto_prefiere_1[preferencias_1[0]]>=longest_chains[preferencias_1[1]+1][0])*cuanto_prefiere_1[preferencias_1[1]]:
        if preferencias_1[0]==preferencias_2[0]:
            ind_aux=longest_chains[preferencias_1[0]+1][1]+longest_chains[preferencias_1[0]+1][1]/2
        else:
            ind_aux=longest_chains[preferencias_1[0]+1][1]
    else:
        if preferencias_1[1]==preferencias_2[0]:
            ind_aux=longest_chains[preferencias_1[1]+1][1]+longest_chains[preferencias_1[1]+1][1]/2
        else:
            ind_aux=longest_chains[preferencias_1[1]+1][1]
    ind_aux=int(ind_aux)
    temp_t=torta[ind_aux:]

    torta=np.concatenate((torta[:ind_aux],temp_t), axis=0)
    for j in range(len(torta)):
        actual_1+=funcion_de_valoracion.loc[torta[j]-1,'jug1']/total1
        actual_2-=funcion_de_valoracion.loc[torta[j]-1,'jug2']/total2
        diff=abs(actual_1-actual_2)
        if ( diff < epsilon):
            epsilon=diff
            iter=j
    if iter!=T-1:
        iter+=1
    porcion=torta[:iter]
    porcion2=torta[iter:]
    gananciaPorc1_1=0
    gananciaPorc1_2=0
    gananciaPorc2_1=0
    gananciaPorc2_2=0
    for j in range(len(porcion)):
        gananciaPorc1_1+=funcion_de_valoracion.loc[porcion[j]-1,'jug1']
        gananciaPorc1_2+=funcion_de_valoracion.loc[porcion[j]-1,'jug2']
    for j in range(len(porcion2)):
        gananciaPorc2_1+=funcion_de_valoracion.loc[porcion2[j]-1,'jug1']
        gananciaPorc2_2+=funcion_de_valoracion.loc[porcion2[j]-1,'jug2']
    
    
    results.append((i, gananciaPorc1_1/total1,gananciaPorc1_2/total2,  gananciaPorc2_1/total1, gananciaPorc2_2/total2))


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
for i,  gananciaPorc1_1, gananciaPorc1_2, gananciaPorc2_1, gananciaPorc2_2 in results:
    if gananciaPorc2_2< gananciaPorc1_2:
        ax1.plot([i], [gananciaPorc2_1], 'o-', alpha=0.5)
        ax2.plot([i], [gananciaPorc1_2], 'o-', alpha=0.5)
       
    else:
        ax1.plot([i], [gananciaPorc1_1], 'o-', alpha=0.5)
        ax2.plot([i], [gananciaPorc2_2], 'o-', alpha=0.5)
ax1.set_xlabel('Iteración')
ax1.set_ylabel('Ganancia jugador 1')
ax2.set_xlabel('Iteración')
ax2.set_ylabel('Ganancia jugador 2')
fig.suptitle(f"Tamaño de torta= {T}")
ax1.axhline(y=0.5, color='c', linestyle='--', label='Equilibrio de Nash')
ax2.axhline(y=0.5, color='r', linestyle='--', label='Equilibrio de Nash')
plt.grid()
plt.show()
    
    #print(f' las porciones son {porcion,porcion2} \n iteración: {i} \n Para el jugador 1 las porciones valen {gananciaPorc1_2, gananciaPorc1_2} \n', f' Para el jugador 2 las porciones valen {gananciaPorc2_2, gananciaPorc2_2}')