import cv2
import numpy as np
import math

def translacion(x, y, tx, ty):
    matriz_translacion = np.array([[1,0,tx],[0,1,ty],[0,0,1]])
    coordenadas = np.array([x,y,1])
    return np.dot(matriz_translacion, coordenadas)

def rotacion(x,y, grado):
    matriz_rotacion = np.array([[math.cos(grado), -(math.sen(grafo)),0],[math.sin(grado),math.cos(grado),0],[0,0,1]])
    coordenadas = np.array([x,y,1])
    return np.dot(matriz_rotacion, coordenadas)

def escalacion(x,y,sx,sy):
    matriz_escalacion = np.array([[sx,0,0],[0,sy,0],[0,0,1]])
    coordenadas = np.array([x,y,1])
    return np.dot(matriz_escalacion, coordenadas)

def main():
    s = translacion(200, 100, 40, 30)
    print(s[2])
    
if __name__ == '__main__':
    main()
 