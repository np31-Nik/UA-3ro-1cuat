from casilla import *
from mapa import *
import math
import sys

class Nodo():
#inicializador de clase
    def __init__(self,g,h,f,padre,casilla):
        self.f=f
        self.g=g
        self.h=h
        self.padre=padre
        self.casilla=casilla

#funcion de igualdad
    def __eq__(self,other):
        if isinstance(other,Nodo):
            return self.casilla==other.casilla
        return False

#funcion que calcula el coste desde el nodo(self) al nodo m
    def coste(self,m):
        ny=self.casilla.getFila()
        nx=self.casilla.getCol()
        my=m.casilla.getFila()
        mx=m.casilla.getCol()

        if nx==mx or ny==my:
            return 1.0
        return 1.5

#funcion que calcula la f,g,h de un nodo y lo actualiza
    def reCalcularNodo(self,destino):

        #------- aqui se cambia la heuristica:
        self.h = self.manhattan(destino)
        #-------

        self.g=self.padre.g + Nodo.coste(self.padre,self)
        self.f=self.g+self.h

#funcion que devuelve los hijos de un nodo
    def hijosN(self,mapi,camino,destino):
        listaHijos=[]

        x=self.casilla.getFila()
        y=self.casilla.getCol()

        for i in range(-1,2):
            for j in range(-1,2):
                if i!=0 or j!=0:
                    xi=i+x
                    yj=y+j

                    if mapi.getCelda(xi,yj)!=1:
                        casilla=Casilla(xi,yj)
                        padre=self
                        n=Nodo(0,0,0,padre,casilla)
                        n.reCalcularNodo(destino)
                        listaHijos.append(n)

        return listaHijos

#funcion que devuelve el nodo menor de una lista
    @staticmethod
    def nodoMenor(listaAbierta):
        menorF=sys.maxsize
        menorN=None
        
        for nodo in listaAbierta:
            if nodo.f < menorF:
                menorF=nodo.f
                menorN=nodo

        return menorN

#funcion que devuelve una lista de casillas a partir de una lista de nodos
    @staticmethod
    def casillas(lista):
        cas=[]
        for c in lista:
            cas.append(c.casilla)        
        return cas

#funcion que se encarga de modificar la matriz camino
    @staticmethod
    def reconstruirCamino(camino,n):
        npad = n.padre
        coste = 0

        if npad:
            coste = n.coste(npad)

        while npad:
            alto = npad.casilla.getFila()
            ancho = npad.casilla.getCol()
            camino[alto][ancho]=npad.f
            if npad.padre:
                coste += npad.padre.coste(npad)
                npad = npad.padre
            else:
                break
        return (coste,camino)

#funcion de heuristica que calcula la distancia manhattan
# man = |x2-x1| + |y2-y1|
    def manhattan(self,destino):
        man = abs(destino.casilla.getCol() - self.casilla.getCol()) + abs(destino.casilla.getFila() - self.casilla.getFila())
        return man

#funcion de heuristica que calcula la distancia euclidea
# sqrt( (x2-x1)**2 + (y2-y1)**2 )
    def euclidea(self,destino):
        euc = math.sqrt((destino.casilla.getCol() - self.casilla.getCol())**2 + (destino.casilla.getFila() - self.casilla.getFila())**2)
        return euc

#funcion de heuristica que calcula la distancia de Chebyshov
# Cheb = max( |x2-x1|, |y2-y1| )
    def chebyshov(self,destino):
        cheb = max(abs(destino.casilla.getCol() - self.casilla.getCol()) , abs(destino.casilla.getFila() - self.casilla.getFila()))
        return cheb