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

def parametros(matriz, q):
    n = matriz.shape[1]  # Número de columnas de la matriz 
    k = matriz.shape[0] # Número de filas de la matriz 
    codewords_ext = extension(hallar_codewords(matriz, q), q)
    d = float('inf')
    for codeword in codewords_ext:
        if any(x != 0 for x in codeword):  # Ignorar el vector nulo
            distancia = sum(1 for x in codeword if x != 0) # Contar los elementos no nulos
            if distancia < d: # Actualizar la distancia mínima
                d = distancia
    res = [n+1, k, d] # parametros del codigo extendido
    if q==2: # si es binario
        if d%2 != 0: # si la distancia es impar
            d= d+1 # se le suma 1
            res= [n+1, k, d] 
    return res
    
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

def matriz_identidad(matriz):
    matriz = np.array(matriz)
    identidad = np.eye(matriz.shape[0], dtype=int)
    return identidad

def matriz_generadora_estandar(matriz, q):
    matriz = np.array(matriz)
    tamano = matriz.shape[0]
    for i in range(tamano):
        # Hacer que el elemento diagonal sea 1
        factor = matriz[i, i]
        if factor == 0:
            # Buscar una fila para intercambiar
            for k in range(i + 1, tamano):
                if matriz[k, i] != 0:
                    matriz[[i, k]] = matriz[[k, i]]
                    factor = matriz[i, i]
                    break
        if factor != 0:
            factor = int(factor)  # Convertir a tipo de datos estándar de Python
            matriz[i] = (matriz[i] * pow(factor, -1, q)) % q
        
        # Hacer ceros en la columna i para todas las filas excepto la i-ésima
        for j in range(tamano):
            if i != j:
                factor = matriz[j, i]
                matriz_1[j] = (matriz_1[j] - factor * matriz_1[i]) % q
    return matriz_1

def Matriz_Control(matriz_1, q):
    matriz_1 = np.array(matriz_1)
    tamano = matriz_1.shape[0]
    # Extraer la parte que está al lado de la matriz identidad
    parte_lateral = matriz_1[:, tamano:]
    # Transponer la parte lateral
    parte_lateral_transpuesta = parte_lateral.T

    # Crear la matriz identidad de tamaño (n - número de filas de la matriz)
    n = matriz_1.shape[1]  # Número de columnas de la matriz original
    numero_filas = matriz_1.shape[0]
    identidad_n_k = np.eye(n - numero_filas, dtype=int)

    if (q ==3):
        inverso_ternario = np.zeros_like(parte_lateral_transpuesta, dtype=int)
        for i in range(parte_lateral_transpuesta.shape[0]):
            for j in range(parte_lateral_transpuesta.shape[1]):
                elemento = int(parte_lateral_transpuesta[i, j])
                if elemento == 0:
                    inverso_ternario[i, j] = 0
                elif elemento == 1:
                    inverso_ternario[i, j] = 2
                elif elemento == 2:
                    inverso_ternario[i, j] = 1
        # Unir la matriz del inverso ternario con la identidad n_k
        matrizdecontrol = np.hstack((inverso_ternario, identidad_n_k))
    else: 
        matrizdecontrol = np.hstack((parte_lateral_transpuesta, identidad_n_k))
    return matrizdecontrol

print("\nPRIMER EJERCICIO")
matriz_1 = [[2, 1, 0, 0, 1, 1], [1, 0, 2, 2, 1, 0],[0, 1, 0, 0, 2, 1]]
q_1 = 3
print("\nCodewords del código C:")
codewords = hallar_codewords(matriz_1, q_1)
print(codewords)
print("\nCodewords del código C extendido:")
print(extension(codewords, q_1))
print("\nParámetros del código C extendido:")
print(parametros(np.array(matriz_1), q_1))
print("\nCodewords del código C reducido:")
reduccion_perforacion(codewords, 1, 1, 6)
print("\nCodewords del código C perforado:")
reduccion_perforacion(codewords, 2, 1, 6)
matrizgeneradora_estandar = matriz_generadora_estandar(matriz_1, q_1)
matrizdeControl = Matriz_Control(matrizgeneradora_estandar, q_1)
print("\nMatriz de Control H: \n", matrizdeControl)

print("\nSEGUNDO EJERCICIO")
matriz_2 = [[1, 0, 0, 1, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 1, 0, 0, 1]]
q_2 = 2
print("\nCodewords del código C:")
hallar_codewords(matriz_2, q_2)
print(codewords)
print("\nCodewords del código C extendido:")
print(extension(codewords, q_2))
print("\nParámetros del código C extendido:") 
print(parametros(np.array(matriz_2), q_2))
print("\nCodewords del código C reducido:")
reduccion_perforacion(codewords, 1, 1, 3)
print("\nCodewords del código C perforado:")
reduccion_perforacion(codewords, 2, 1, 3)
matrizgeneradora_estandar = matriz_generadora_estandar(matriz_2, q_2)
matrizdeControl = Matriz_Control(matrizgeneradora_estandar, q_2)
print("\nMatriz de Control H: \n", matrizdeControl)