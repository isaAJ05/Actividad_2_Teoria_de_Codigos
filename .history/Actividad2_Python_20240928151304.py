import numpy as np 
from itertools import product

def hallar_codewords(matriz, q):
    k = len(matriz)
    v = []
    for i in range(q):
        v.append(i)
    combinaciones = list(product(v, repeat=k))

    codewords = []
    for U in combinaciones:
        U = np.array(U)
        codeword = np.dot(U, matriz) % q
        codewords.append(codeword.tolist())

    return codewords


def extension(codewords, q):
    for i in range(len(codewords)):
        codewords[i] = list(codewords[i])
        suma = sum(codewords[i])
        if suma%q==0:
            agregar = 0
        else:
            if q==3:
                if suma%q==1:
                    agregar = 2
                elif suma%q==2:
                    agregar = 1
            elif q==2:
                agregar = 1

        codewords[i].append(agregar)
    return codewords
    
def reduccion_perforacion(codewords, rp, lim_inf, lim_sup):
    for i in range(lim_inf-1, lim_sup):
        redperf_por_i=[]
        print(f'\ni = {i+1}')
        for j in range(len(codewords)):
            codeword = codewords[j]
            codeword_nuevo = cambio_redperf(codeword[:], rp, i)
            if codeword_nuevo != None:
                redperf_por_i.append(codeword_nuevo)
                print(codeword_nuevo)
        
def cambio_redperf(codeword, rp, i):
    if rp == 1: # ya no se si entendi la reduccion :(
        
        if i < len(codeword) and codeword[i] == 0:
            codeword.pop(i)
            return codeword
        else:
            return None
        
    elif rp == 2:
        codeword.pop(i)
        return codeword

def matriz_control(matriz):
    matriz = np.array(matriz)
    identidad = np.eye(matriz.shape[0], dtype=int)
    return identidad

print("\nPRIMER EJERCICIO")
matriz_1 = [[2, 1, 0, 0, 1, 1], [1, 0, 2, 2, 1, 0],[0, 1, 0, 0, 2, 1]]
q_1 = 3
print("\nCodewords del código C:")
codewords = hallar_codewords(matriz_1, q_1)
print(codewords)
print("\nCodewords del código C extendido:")
print(extension(codewords, q_1))
print("\nCodewords del código C reducido:")
reduccion_perforacion(codewords, 1, 1, 6)
print("\nCodewords del código C perforado:")
reduccion_perforacion(codewords, 2, 1, 6)

print("\nSEGUNDO EJERCICIO")
matriz_2 = [[1, 0, 0, 1, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 1, 0, 0, 1]]
q_2 = 2
print("\nCodewords del código C:")
hallar_codewords(matriz_2, q_2)
print(codewords)
print("\nCodewords del código C extendido:")
print(extension(codewords, q_2))
print("\nCodewords del código C reducido:")
reduccion_perforacion(codewords, 1, 1, 3)
print("\nCodewords del código C perforado:")
reduccion_perforacion(codewords, 2, 1, 3)