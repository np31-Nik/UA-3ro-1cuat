import sys, pygame
import tkinter
from casilla import *
from mapa import *
from nodo import *
from pygame.locals import *
import tkinter.filedialog
import tkinter.messagebox
import numpy as np


MARGEN=5
MARGEN_INFERIOR=60
TAM=15
NEGRO=(0,0,0)
BLANCO=(255, 255,255)
VERDE=(0, 255,0)
ROJO=(255, 0, 0)
AZUL=(0, 0, 255)
AMARILLO=(255, 255, 0)

#Constantes
MOV_H=1
MOV_V=1
MOV_D=1.5


# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

# Devuelve si una casilla del mapa se puede seleccionar como destino
def bueno(mapi, pos):
    res= False
    
    if mapi.getCelda(pos.getFila(),pos.getCol())==0:
       res=True
    
    return res
    
# Devuelve si una posición de la ventana corresponde al mapa
def esMapa(mapi, posicion):
    res=False     
    
    if posicion[0] > MARGEN and posicion[0] < mapi.getAncho()*(TAM+MARGEN)+MARGEN and \
    posicion[1] > MARGEN and posicion[1] < mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True       
    
    return res
    
#PDevuelve si se ha pulsado el botón. Posición del botón: 20, mapa.getAlto()*(TAM+MARGEN)+MARGEN+10]
def pulsaBoton(mapi, posicion):
    res=False
    
    if posicion[0] > 20 and posicion[0] < 70 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True
    
    return res
    
    
# Construye la matriz para guardar el camino
def inic(mapi):    
    cam=[]
    for i in range(mapi.alto):        
        cam.append([])
        for j in range(mapi.ancho):            
            cam[i].append('.')
    return cam

# funcion algoritmo de busqueda
def aEstrella(mapi,origen,destino,camino):

    listaCerrada=[]
    listaAbierta=[Nodo(0,0,0,None,origen)]
    i = 0

    calto = len(camino)
    cancho = len(camino[0])
    micamino = np.full((calto,cancho),-1)
    orden = 0

    while listaAbierta:
        #print("--- Nº iteración: "+str(i))
        n=Nodo.nodoMenor(listaAbierta)

        alto = n.casilla.getFila()
        ancho = n.casilla.getCol()
        micamino[alto][ancho]=orden
        orden+=1

        if n.casilla == destino:
            #print("     Destino encontrado!!! (x="+str(n.casilla.getCol())+",y="+str(n.casilla.getFila())+") \n")
            #print("Orden de exploracion:")
            #print(str(micamino))
            (coste,camino) = Nodo.reconstruirCamino(camino,n)
            return coste
        else:
            #print("     El nodo actual pasa de la listaAbierta a la listaCerrada: (x="+str(n.casilla.getCol())+",y="+str(n.casilla.getFila())+") \n")
            listaAbierta.remove(n)
            listaCerrada.append(n)
            nhijo = 0
            for m in n.hijosN(mapi,camino,Nodo(0,0,0,None,destino)):
                #print("     Hijo nº"+str(nhijo) +": "+"(x="+str(m.casilla.getCol())+",y="+str(m.casilla.getFila())+") f="+str(m.f))
                if m.casilla not in Nodo.casillas(listaCerrada):
                    gm = n.g + Nodo.coste(n,m)
                    if m.casilla not in Nodo.casillas(listaAbierta):
                        #print("         el hijo no está en listaAbierta, se añade.")
                        listaAbierta.append(m)
                    else:
                        #print("         el hijo ya está en listaAbierta...")
                        index=Nodo.casillas(listaAbierta).index(m.casilla)
                        if gm < listaAbierta[index].g:
                            #print("         ...la g nueva (gm) es mejor que la g antigua, se actualiza.")
                            index=Nodo.casillas(listaAbierta).index(m.casilla)
                            del listaAbierta[index]
                            listaAbierta.append(m)
                        #else:
                            #print("         ...la g antigua es mejor, no se hace nada.")
                #else:
                    #print("         el hijo ya está en listaCerrada.")
                nhijo+=1
        i+=1
        #print("")
    return -1
    
# función principal
def main():
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    file=tkinter.filedialog.askopenfilename() #abre el explorador de archivos    
    
    pygame.init()
    destino=Casilla(-1,-1)
    
    reloj=pygame.time.Clock()    
    
    if not file:     #si no se elige un fichero coge el mapa por defecto   
        file='mapa.txt'
    
    mapi=Mapa(file)
    origen=mapi.getOrigen()    
    camino=inic(mapi)   
    
    anchoVentana=mapi.getAncho()*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1")
    
    boton=pygame.image.load("boton.png").convert()
    boton=pygame.transform.scale(boton,[50, 30])
    
    personaje=pygame.image.load("pig.png").convert()
    personaje=pygame.transform.scale(personaje,[TAM, TAM])   
    
    coste=-1
    running= True
    primeraVez=True
    
    while running:        
        #procesamiento de eventos
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                running=False               
                
            if event.type==pygame.MOUSEBUTTONDOWN:                
                #obtener posición y calcular coordenadas matriciales
                pos=pygame.mouse.get_pos()                
                colDestino=pos[0]//(TAM+MARGEN)
                filDestino=pos[1]//(TAM+MARGEN)
                casi=Casilla(filDestino, colDestino)
                if pulsaBoton(mapi, pos): #reinicializar                    
                    origen=mapi.getOrigen()
                    destino=Casilla(-1,-1)                    
                    camino=inic(mapi)
                    coste=-1
                    primeraVez=True
                elif esMapa(mapi, pos):
                    if bueno(mapi, casi):
                        if not primeraVez: #la primera vez el origen está en el mapa
                            origen=destino                            
                        else:                          
                            mapi.setCelda(int(origen.getFila()), int(origen.getCol()), 0) #se marca como libre la celda origen
                        destino=casi                        
                        camino=inic(mapi)
                        # llamar al A*
                        coste=aEstrella(mapi, origen, destino, camino)      
                        if coste==-1:
                            tkinter.messagebox.showwarning(title='Error', message='No existe un camino entre origen y destino')                     
                        else:
                            primeraVez=False  # hay un camino y el destino será el origen para el próximo movimiento
                    else: # se ha hecho click en una celda roja                
                        tkinter.messagebox.showwarning(title='Error', message='Esa casilla no es valida')
                
          
        #código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        #pinta mapa
        for fil in range(mapi.getAlto()):
            for col in range(mapi.getAncho()):
                if mapi.getCelda(fil, col)==2 and not primeraVez: #para que no quede negro el origen inicial
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)                    
                if mapi.getCelda(fil,col)==0:
                    if camino[fil][col]=='.':
                        pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    else:
                        pygame.draw.rect(screen, AMARILLO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
                elif mapi.getCelda(fil,col)==1:
                    pygame.draw.rect(screen, ROJO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
        #pinta origen
        screen.blit(personaje, [(TAM+MARGEN)*origen.getCol()+MARGEN, (TAM+MARGEN)*origen.getFila()+MARGEN])    
        #pinta destino
        pygame.draw.rect(screen, VERDE, [(TAM+MARGEN)*destino.getCol()+MARGEN, (TAM+MARGEN)*destino.getFila()+MARGEN, TAM, TAM], 0)
        #pinta boton
        screen.blit(boton, [20, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        #pinta coste
        if coste!=-1:            
            fuente= pygame.font.Font(None, 30)
            texto= fuente.render("Coste "+str(coste), True, AMARILLO)            
            screen.blit(texto, [anchoVentana-120, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])            
            
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)        
       
        
    pygame.quit()
    
#---------------------------------------------------------------------
if __name__=="__main__":
    main()
