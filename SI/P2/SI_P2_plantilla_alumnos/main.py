# Importamos las librerias que necesitaremos
import numpy as np
import matplotlib.pyplot as plt
import utils
import adaboost

# Cargamos la base de datos
npzfile = np.load("mnist.npz")
mnist_X = npzfile['x']
mnist_Y = npzfile['y']

# Mostrar una imagen y su etiqueta
#utils.mostrar_imagen(mnist_X[0])

# Adaptar los conjuntos X e Y a AdaBoost
(X, Y) = utils.adaptar_conjuntos(mnist_X, mnist_Y)
clase = 0
Yclase = utils.clase(Y,clase)
# Lanzar Adaboost
T = 1 #num cd a usar
A = 5 #num pruebas aleatorias para cada cd

tam_muestra=10
Xtrain=X[:tam_muestra]
Ytrain=Yclase[:tam_muestra]


H = adaboost.entrenar(Xtrain, Ytrain, T, A)
res = adaboost.aplicarCF(H,Xtrain)
porcentajeEntrenamiento = adaboost.comparar(res,Ytrain)

# Analisis y resultados de las pruebas realizadas
#T = [0, 100, 200, 300, 400]      # Numero de clasificadores 
# resultados = [0, 20, 35, 56, 68] # Resultados obtenidos de clasificacion
#utils.plot_arrays(T, resultados, "Porcentajes con valores de T")
print('clase: ',clase,'resultados train[',tam_muestra,']: ',porcentajeEntrenamiento,'%')

P = 10
for p in range(2,P):
    muestra_hasta = tam_muestra*p*5
    muestra_desde = tam_muestra*(p-1)+1

    Xtest = X[muestra_desde:muestra_hasta]
    Ytest = Yclase[muestra_desde:muestra_hasta]
    #print(Xtest)
    #print(Ytest)
    resTest = adaboost.aplicarCF(H,Xtest)
    porcentajeTest = adaboost.comparar(resTest,Ytest)

    print('clase: ',clase,'resultados test[',muestra_desde,'-',muestra_hasta,']: ',porcentajeTest,'%')
