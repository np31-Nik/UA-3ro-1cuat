import matplotlib.pyplot as plt
import numpy as np

def mostrar_imagen(imagen):
    plt.figure()
    plt.imshow(imagen)
    plt.show()

def adaptar_conjuntos(mnist_X, mnist_Y):
    X = mnist_X.reshape(60000,28*28)
    Y = mnist_Y
    return (X,Y)

def plot_arrays(X, Y, title):
    plt.title(title)
    plt.plot(X, Y)
    plt.show()

def clase(Y,clase):
    Ytemp = np.full(len(Y),0)
    for i in range(len(Y)):
        if Y[i]==clase:
            Ytemp[i]= 1
        else:
            Ytemp[i]= -1
    return Ytemp