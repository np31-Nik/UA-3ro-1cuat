import clasificador_debil as cd
import numpy as np
import math

    # ###########################
    # #### Bloque de ejemplo ####

    # # Datos
    # imagenes_X = [[3,234,50], [1,89,100], [245,130,134]]
    # etiquetas_Y = [1, -1, 1]
    # D = [0.2,0.6,0.3]

    # # Obtenemos un clasificador debil
    # c_d = cd.generar_clasificador_debil(3) #28*28

    # # Aplicamos el clasificador a una imagen
    # res = cd.aplicar_clasificador_debil(c_d, imagenes_X[0])

    # # Calculamos el error 
    # error = cd.obtener_error(c_d, imagenes_X, etiquetas_Y, D)

    # ##########################

def entrenar(X, Y, T, A):
    clasificadores_debiles = []
    alphas = []

    for t in range(T):
        D = np.full(len(X), 1/len(X))
        min_cd = ((),())

        for k in range(A):
            c_d = cd.generar_clasificador_debil(len(X[t]))
            error = cd.obtener_error(c_d,X,Y,D)
            if k == 0:
                min_cd = (c_d,error)
            elif error < min_cd[1]:
                min_cd = (c_d,error)

        clasificadores_debiles.append(min_cd[0])

        if min_cd[1]<=0:
            alfa=1/2
        else:
            alfa = (1/2) * math.log( (1-min_cd[1])/min_cd[1] ,2)

        alphas.append(alfa)
        
        z = np.sum(D)  
        for i in range(len(X)):
            Dtemp=D
            cd_d = cd.aplicar_clasificador_debil(min_cd[0],X[i])

            if cd_d:
                cd_d = 1
            else:
                cd_d = -1

            Dtemp[i] = D[i] * np.exp( -alfa * Y[i] * cd_d ) 

        D = Dtemp/z
    
    return (clasificadores_debiles, alphas) 


def aplicarCF(H,X):
    res=np.full(len(X),0.0)

    for x in range(len(X)):
        h=0.0
        for i in range(len(H[0])):
            cd_res=cd.aplicar_clasificador_debil(H[0][i],X[x])
            if cd_res:
                cd_res=1
            else:
                cd_res=-1

            h += H[1][i]*cd_res
        res[x]=h

    res = np.sign(res)
    res = res.astype(int)
    return res

def comparar(res,Y):
    aciertos=0
    for y in range(len(Y)):
        if res[y]==Y[y]:
            aciertos+=1

    return round(aciertos/len(Y)*100,2)

