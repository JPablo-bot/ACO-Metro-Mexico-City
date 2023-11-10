import pygame
from math import sqrt
import numpy as np
import pandas as pd

def DistEuclidiana(p1,p2):
    suma = 0
    for i in range(len(p1)):
        suma += (p1[i] - p2[i])**2
    d =sqrt(suma)
    return d

pygame.init()
clock = pygame.time.Clock()

# -------------- Variables Globales -------------------------------------------
nodos = np.array(pd.read_csv('Nodos.csv'))
nodos = nodos[:,1:]

estaciones = [['El Rosario'],['Inst. Petróleo'],['Dep. 18 Marzo'],['Martín Carrera'],['La Raza'],
              ['Consulado'],['Tacuba'],['Guerrero'],['Garibaldi'],['Oceanía'],
              ['Hidalgo'],['Bellas Artes'],['Morelos'],['Candelaria'],['San Lázaro'],
              ['Balderas'],['Salto del Agua'],['Pino Suarez'],['Tacubaya'],['Centro Médico'],
              ['Chabacano'],['Jamaica'],['Pantitlán']]

nodosMapa = np.array(pd.read_csv('NodosMap.csv'))
nodosMapa = nodosMapa[:,1:]

conexiones = np.array([[0,1],[0,6],
              [1,0],[1,2],[1,4],
              [2,1],[2,4],[2,3],
              [3,2],[3,5],
              [4,1],[4,2],[4,5],[4,7],
              [5,3],[5,4],[5,9],[5,12],
              [6,0],[6,10],[6,18],
              [7,4],[7,8],[7,10],
              [8,7],[8,11],[8,12],
              [9,5],[9,14],[9,22],
              [10,6],[10,7],[10,11],[10,15],
              [11,8],[11,10],[11,16],[11,17],
              [12,5],[12,8],[12,13],[12,14],
              [13,12],[13,14],[13,17],[13,21],
              [14,9],[14,12],[14,13],[14,22],
              [15,10],[15,16],[15,18],[15,19],
              [16,11],[16,15],[16,17],[16,20],
              [17,11],[17,13],[17,16],[17,20],
              [18,6],[18,15],[18,19],
              [19,15],[19,18],[19,20],
              [20,16],[20,17],[20,19],[20,21],
              [21,13],[21,20],[21,22],
              [22,9],[22,14],[22,21]])

# -----------------------------------------------------------------------------

# ---------
# CONSTANTS
# ---------
WIDTH = 1190
HEIGHT = 900
LINE_WIDTH = 15
METRO_WIDTH = 5
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 180
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
# rgb: red green blue
RED = (255, 0, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (180,180,180)

BG_COLOR = (255, 255, 255)
LINE_COLOR = (23, 145, 135)
POINT_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

myFont = pygame.font.Font(None, 20)

# ------
# SCREEN
# ------
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'ACO Metro' )
screen.fill( BG_COLOR )

def CrearMetro():
    for i in range(len(conexiones)):
        [i1,i2] = nodosMapa[conexiones[i,0]]
        [f1,f2] = nodosMapa[conexiones[i,1]]
        pygame.draw.line( screen, GRAY, (i1, i2), (f1, f2), METRO_WIDTH )
    
    for i in range(len(nodosMapa)):
        pygame.draw.circle(screen, BLACK, (nodosMapa[i,0],nodosMapa[i,1]), 8)
        if (i == 14):
            miTexto = myFont.render((estaciones[i][0]),0,BLACK)
            screen.blit(miTexto,(nodosMapa[i,0]-25,nodosMapa[i,1]+10))
        else:
            miTexto = myFont.render((estaciones[i][0]),0,BLACK)
            screen.blit(miTexto,(nodosMapa[i,0]-25,nodosMapa[i,1]-20))
    pygame.draw.line( screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH )
    
    return

def AntsMetro (inicio, fin):
    distancias = np.zeros((len(conexiones),1))
    visibilidad = np.zeros((len(conexiones),1))
    feromona = np.ones((len(conexiones),1))*0.01
    
    for i in range(len(conexiones)):
        distancias[i] = DistEuclidiana(nodos[conexiones[i][0]],nodos[conexiones[i][1]])
        visibilidad[i] = 1/distancias[i]
        
    cont = 0
    alpha = 1
    beta = 1
    nodosMin = len(nodos)
    while(cont < 10):

        nAnts = 50
        allAnts = []
        
        for i in range(nAnts):
            inicio = 22
            fin = 0
            anterior = -1
            currentAnt = []
            while(inicio != fin):
                rutasP = np.where(conexiones[:,0] == inicio)
                [indx,indy] = np.where(conexiones[rutasP,1] == anterior)
                if (indy.size > 0):
                    rutasP = np.delete(rutasP, int(indy))
                
                denominador = ((feromona[rutasP[:]]**alpha)*(visibilidad[rutasP[:]]**beta))
                denominador = sum(denominador)
                
                probabilidad = (((feromona[rutasP[:]]**alpha)*(visibilidad[rutasP[:]]**beta)) / denominador)
                rectaSelect = []
                suma1 = 0
                for i in range(len(probabilidad)):
                    suma1 = suma1 + probabilidad[i]
                    rectaSelect.append(suma1)
                rectaSelect = np.array(rectaSelect)
                
                select = np.random.rand()
                [camx,camy] = np.where(select < rectaSelect)
                
                [antTox,antToy] = np.where(probabilidad  == probabilidad[camx[0]])
                anterior = inicio
                inicio = int(conexiones[np.array(rutasP).T[antTox[0]],1])
                currentAnt.append([anterior,inicio])
            allAnts.append(currentAnt)
        
        # ------------------ Calcular distancias por cada ruta de hormiga -------------
        allDists = []
        for i in range(len(allAnts)):
            indDists = []
            for j in range(len(allAnts[i])):
                for k in range(len(conexiones)):
                    if(allAnts[i][j] == conexiones[k]).all():
                        indDists.append(k)
            allDists.append(sum(distancias[indDists]))            
        
        
        # ----------------------------- Actualizar feromona ---------------------------
        rho = 0.5 # Factor de evaporación
        Q = 1 # Factor de olvido
        
        for i in range(len(feromona)):
            dTau = 0
            for j in range(nAnts):
                paso = False
                hormiga = np.array(allAnts[j])
                pasoPor = np.zeros(np.shape(hormiga))
                pasoPor = np.where(hormiga == conexiones[i][0], True, pasoPor)
                pasoPor = np.where(hormiga == conexiones[i][1], True, pasoPor)
                for k in range(len(pasoPor)):
                    if(pasoPor[k][0] == 1 and pasoPor[k][1] == 1): paso = True
                
                if (paso): dTau = dTau + (Q/allDists[j])
            feromona[i] = (1 - rho) * feromona[i] + dTau
            
        inicio = 22
        fin = 0
        anterior = -1
        rutaFinal = []
        while(inicio != fin):
            rutasP = np.where(conexiones[:,0] == inicio)
            [indx,indy] = np.where(conexiones[rutasP,1] == anterior)
            if (indy.size > 0):
                rutasP = np.delete(rutasP, int(indy))
            
            denominador = ((feromona[rutasP[:]]**alpha)*(visibilidad[rutasP[:]]**beta))
            denominador = sum(denominador)
            probabilidad = (((feromona[rutasP[:]]**alpha)*(visibilidad[rutasP[:]]**beta)) / denominador)
        
            [antTox,antToy] = np.where(probabilidad  == max(probabilidad))
            anterior = inicio
            inicio = int(conexiones[np.array(rutasP).T[antTox[0]],1])
            rutaFinal.append([anterior,inicio])
            
            
            if (len(rutaFinal) > nodosMin):
                beta -= 0.05
                cont = 0
                break
            
        cont += 1    
        if(len(rutaFinal) < nodosMin):
            nodosMin = len(rutaFinal)
            rutaMin = rutaFinal
            cont = 0
            
    return rutaMin
    
def selectNodo (mouse_x, mouse_y):
    if(mouse_x>=192 and mouse_x<=208 and mouse_y>=242 and mouse_y<=258): station = 0
    elif(mouse_x>=440 and mouse_x<=456 and mouse_y>=288 and mouse_y<=304): station = 1
    elif(mouse_x>=553 and mouse_x<=569 and mouse_y>=288 and mouse_y<=304): station = 2
    elif(mouse_x>=761 and mouse_x<=777 and mouse_y>=288 and mouse_y<=304): station = 3
    elif(mouse_x>=506 and mouse_x<=522 and mouse_y>=353 and mouse_y<=369): station = 4
    elif(mouse_x>=761 and mouse_x<=777 and mouse_y>=405 and mouse_y<=421): station = 5
    elif(mouse_x>=192 and mouse_x<=208 and mouse_y>=434 and mouse_y<=450): station = 6
    elif(mouse_x>=439 and mouse_x<=455 and mouse_y>=470 and mouse_y<=486): station = 7
    elif(mouse_x>=526 and mouse_x<=542 and mouse_y>=470 and mouse_y<=486): station = 8
    elif(mouse_x>=918 and mouse_x<=934 and mouse_y>=495 and mouse_y<=511): station = 9
    elif(mouse_x>=439 and mouse_x<=455 and mouse_y>=509 and mouse_y<=525): station = 10
    elif(mouse_x>=526 and mouse_x<=542 and mouse_y>=509 and mouse_y<=525): station = 11
    elif(mouse_x>=761 and mouse_x<=777 and mouse_y>=504 and mouse_y<=520): station = 12
    elif(mouse_x>=761 and mouse_x<=777 and mouse_y>=545 and mouse_y<=561): station = 13
    elif(mouse_x>=802 and mouse_x<=818 and mouse_y>=545 and mouse_y<=561): station = 14
    elif(mouse_x>=439 and mouse_x<=455 and mouse_y>=643 and mouse_y<=659): station = 15
    elif(mouse_x>=527 and mouse_x<=543 and mouse_y>=643 and mouse_y<=659): station = 16
    elif(mouse_x>=637 and mouse_x<=653 and mouse_y>=643 and mouse_y<=659): station = 17
    elif(mouse_x>=193 and mouse_x<=209 and mouse_y>=792 and mouse_y<=808): station = 18
    elif(mouse_x>=441 and mouse_x<=457 and mouse_y>=792 and mouse_y<=808): station = 19
    elif(mouse_x>=638 and mouse_x<=654 and mouse_y>=792 and mouse_y<=808): station = 20
    elif(mouse_x>=761 and mouse_x<=777 and mouse_y>=792 and mouse_y<=808): station = 21
    elif(mouse_x>=984 and mouse_x<=1000 and mouse_y>=749 and mouse_y<=765): station = 22
        
    return station


def pintaRuta(rutaMinFinal):
    for i in range(len(rutaMinFinal)):
        [i1,i2] = nodosMapa[rutaMinFinal[i][0]]
        [f1,f2] = nodosMapa[rutaMinFinal[i][1]]
        pygame.draw.line( screen, LINE_COLOR, (i1, i2), (f1, f2), METRO_WIDTH+1)
        pygame.draw.circle(screen, RED, (i1,i2), 10)
        pygame.draw.circle(screen, RED, (f1,f2), 10)
        if (i1 == 810 and i2 == 553):
            miTexto = myFont.render((estaciones[rutaMinFinal[i][0]][0]),0,RED)
            screen.blit(miTexto,(i1-25,i2+10))
        elif (f1 == 810 and f2 == 553):
            miTexto = myFont.render((estaciones[rutaMinFinal[i][1]][0]),0,RED)
            screen.blit(miTexto,(f1-25,f2+10))
            
        else:
            miTexto = myFont.render((estaciones[rutaMinFinal[i][0]][0]),0,RED)
            screen.blit(miTexto,(i1-25,i2-20))
            miTexto = myFont.render((estaciones[rutaMinFinal[i][1]][0]),0,RED)
            screen.blit(miTexto,(f1-25,f2-20))
    
    return

siCalcula = 0
CrearMetro()
flag = 0
state = True
while state:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = False        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            if (flag == 0):
                inicio = selectNodo(mouse_x,mouse_y)
                siCalcula += 1
                flag = 1
                
            else:
                fin = selectNodo (mouse_x,mouse_y)
                siCalcula += 1
                flag = 0
        
        if(siCalcula == 2):
            rutaMinFinal = AntsMetro(inicio, fin)
            pintaRuta(rutaMinFinal)
            siCalcula = 0
        
    
    
    pygame.display.update()
    clock.tick(30)
    
pygame.quit()