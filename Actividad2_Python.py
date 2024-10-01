#PAULA NUÑEZ E ISABELLA ARRIETA
import numpy as np 
from itertools import product

def hallar_codewords(matriz, q): # Hallar los codewords a partir de la matriz generadora
    k = len(matriz) # Número de filas
    v = [] 
    for i in range(q): # Vector de 0 a q-1 para sacar las combinaciones lineales
        v.append(i)
    combinaciones = list(product(v, repeat=k)) # Combinaciones de los elementos de v

    codewords = []
    for U in combinaciones: # Multiplicar las combinaciones por la matriz generadora
        U = np.array(U) 
        codeword = np.dot(U, matriz) % q # Producto punto y módulo q para Fq
        codewords.append(codeword.tolist()) # Agregar a la lista de codewords
    return codewords


def extension(codewords, q): # Extensión del código
    for i in range(len(codewords)): # Recorrer los codewords
        codewords[i] = list(codewords[i]) 
        suma = sum(codewords[i]) # Suma de los elementos de cada codeword
        if suma%q==0: # Si la suma es 0 en Fq, agregar 0
            agregar = 0
        else:
            if q==3: # Agregar 1 o 2 si la suma no es 0 en código ternario dependiendo del resultado
                if suma%q==1:
                    agregar = 2
                elif suma%q==2:
                    agregar = 1
            elif q==2: # Agregar 1 si la suma no es 0 en código binario
                agregar = 1 

        codewords[i].append(agregar)
    return codewords

def parametros(matriz, q):
    n = matriz.shape[1]  # Longitud: Número de columnas de la matriz 
    k = matriz.shape[0] # Dimension: Número de filas de la matriz 
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
    
def reduccion_perforacion(codewords, rp, lim_inf, lim_sup): # Función para reducción y perforación
    for i in range(lim_inf-1, lim_sup): # Hacer para cada i dentro de 1<=i<=lim_sup
        redperf_por_i=[]
        print(f'\ni = {i+1}')
        for j in range(len(codewords)): # Recorrer los codewords
            codeword = codewords[j] 
            codeword_nuevo = cambio_redperf(codeword[:], rp, i) # Llama la función respectiva para hacer el cambio
            if codeword_nuevo != None:
                redperf_por_i.append(codeword_nuevo) # Agregar el codeword nuevo a la lista
        print(' '.join(str(codeword) for codeword in redperf_por_i)) # Imprimir los codewords
        
def cambio_redperf(codeword, rp, i):
    if rp == 1: # Reducción
        if codeword[i] == 0: # Eliminar el elemento en la posición i si es igual a 0
            codeword.pop(i)
            codeword.pop()
            return codeword
        else:
            return None # Si no se cumple la condición se ignora
        
    elif rp == 2: # Perforación
        codeword.pop(i) # Eliminar el elemento en la posición i
        codeword.pop()
        return codeword


def matriz_generadora_estandar(matriz, q):
    matriz = np.array(matriz)
    kdim = matriz.shape[0] # Dimension: Número de filas de la matriz
    for i in range(kdim):
        # Hacer que el elemento diagonal sea 1
        factor = matriz[i, i]
        if factor == 0:
            # Buscar una fila para intercambiar
            for k in range(i + 1, kdim):
                if matriz[k, i] != 0:
                    matriz[[i, k]] = matriz[[k, i]]
                    factor = matriz[i, i]
                    break
        if factor != 0:
            factor = int(factor)  # Convertir a tipo de datos estándar de Python
            matriz[i] = (matriz[i] * pow(factor, -1, q)) % q
        
        # Hacer ceros en la columna i para todas las filas excepto la i-ésima
        for j in range(kdim):
            if i != j:
                factor = matriz[j, i]
                matriz[j] = (matriz[j] - factor * matriz[i]) % q
    return matriz

def Matriz_Control(matriz, q):
    matriz = np.array(matriz)
    k = matriz.shape[0] # Dimensión: Número de filas de la matriz
    # Extraer la parte que está al lado de la matriz identidad
    A = matriz[:, k:]
    # Transponer la parte lateral
    A_transpuesta = A.T
    # Crear la matriz identidad de tamaño n - k
    n = matriz.shape[1]  # Longitud: Número de columnas de la matriz original
    identidad_n_k = np.eye(n - k, dtype=int)

    if (q ==3): # si es ternario
        A_inverso_ternario = np.zeros_like(A_transpuesta, dtype=int)
        for i in range(A_transpuesta.shape[0]):
            for j in range(A_transpuesta.shape[1]):
                elemento = int(A_transpuesta[i, j])
                if elemento == 0:
                    A_inverso_ternario[i, j] = 0 # si es 0 se queda igual
                elif elemento == 1:
                    A_inverso_ternario[i, j] = 2 # si es 1 se cambia por 2
                elif elemento == 2:
                    A_inverso_ternario[i, j] = 1 # si es 2 se cambia por 1
        # Unir -A con la matriz identidad n-k
        matrizdecontrol = np.hstack((A_inverso_ternario, identidad_n_k))
    else: # si es binario
        matrizdecontrol = np.hstack((A_transpuesta, identidad_n_k))
    return matrizdecontrol

# LLAMAR FUNCIONES PARA LOS RESPECTIVOS EJERCICIOS
print("\n[ACTIVIDAD 2 - TEORÍA DE CÓDIGOS]\nPor: Paula Nuñez e Isabella Arrieta")
print("\n**[PRIMER EJERCICIO]**")
matriz_1 = [[2, 1, 0, 0, 1, 1], [1, 0, 2, 2, 1, 0],[0, 1, 0, 0, 2, 1]]
q_1 = 3
print("\n→ Codewords del código C:")
codewords = hallar_codewords(matriz_1, q_1)
print(codewords)
print("\n(a) → Codewords del código C extendido:")
print(extension(codewords, q_1))
print("\n(b) → Parámetros del código C extendido:")
print(parametros(np.array(matriz_1), q_1))
print("\n(c) → Codewords del código C perforado:")
reduccion_perforacion(codewords, 2, 1, 6)
print("\n(d) → Codewords del código C reducido:")
reduccion_perforacion(codewords, 1, 1, 6)
matrizgeneradora_estandar = matriz_generadora_estandar(matriz_1, q_1)
matrizdeControl = Matriz_Control(matrizgeneradora_estandar, q_1)
print("\n** Matriz generadora de forma estandar: \n", matrizgeneradora_estandar)
print("\n(e) → Matriz de Control H: \n", matrizdeControl)

print("\n**[SEGUNDO EJERCICIO]**")
matriz_2 = [[1, 0, 0, 1, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 1, 0, 0, 1]]
q_2 = 2
print("\n→ Codewords del código C:")
hallar_codewords(matriz_2, q_2)
codewords = hallar_codewords(matriz_2, q_2)
print(codewords)
print("\n(a) → Codewords del código C extendido:")
print(extension(codewords, q_2))
print("\n(b) → Parámetros del código C extendido:") 
print(parametros(np.array(matriz_2), q_2))
print("\n(c) → Codewords del código C perforado:")
reduccion_perforacion(codewords, 2, 1, 3)
print("\n(d) → Codewords del código C reducido:")
reduccion_perforacion(codewords, 1, 1, 3)
matrizgeneradora_estandar = matriz_generadora_estandar(matriz_2, q_2)
matrizdeControl = Matriz_Control(matrizgeneradora_estandar, q_2)
print("\n** Matriz generadora de forma estandar: \n", matrizgeneradora_estandar)
print("\n(e) → Matriz de Control H: \n", matrizdeControl)
