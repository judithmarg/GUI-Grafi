from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
from turtle import right, xcor
from PIL import ImageGrab
from cv2 import circle, line
import numpy as np
import math
import sys
import customtkinter


sys.setrecursionlimit(2000000000)
rows = 1500
cols = 1700
mat = [[0 for _ in range(cols)] for _ in range(rows)]


def init():
    global mat
    for i in range(0, rows):
        for l in range(0, cols):
            mat[i][l] = 'none'


            #print(i,"  ",l," = ",mat[i][l])
dondex = -1
dondey = -1
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]
dx8 = [0, 0, 1, -1, 1, -1, -1, 1]
dy8 = [1, -1, 0, 0, 1, -1, 1, -1]
punteada = False


def floodfill1():
    init()
    global x0, y0
    global mat
    SZ = len(puntosx)
    x0 = puntosx[SZ-1]
    y0 = puntosy[SZ-1]
    canvas.FloodFill()


class BresenhamCanvas(Canvas):

    def draw_point(self, x, y, color):
        global mat
        mat[x][y] = color
        if self.clippingControl(x, y):
            self.create_line(x, y, x+1, y+1, fill=colorHex, width=2)

    def FloodFill(self):
        #self.linea(100, 100, 60, 500, 1)
        #self.draw_point(500, 500, color="red")
        # self.floodFillReal(10,10,"none","red")
        self.floodFillReal(x0, y0, "none", "red")

    def floodFillReal(self, x, y, antiguo, nuevo):

        mat[x][y] = "red"
        for i in range(len(dx)):
            x1 = x+dx[i]
            y1 = y+dy[i]
            if (x1 > 0 and y1 > 0 and x1 < 1000 and y1 < 1000 and mat[x1][y1] == "none"):
                self.floodFillReal(x1, y1, antiguo, nuevo)

    def bresenham(self, x0, y0, x1, y1, color="red"):
        dx = abs(x1-x0)
        dy = abs(y1-y0)
        p = 2*dy-dx
        incE = 2*dy
        incNE = 2*(dy-dx)
        global dondex
        global dondey, punteada

        if dx > dy:
            if x0 > x1:
                x = x1
                y = y1
                xend = x0
                yend = y0
            else:
                x = x0
                y = y0
                xend = x1
                yend = y1
            ayuda = 0
            if y0 > y1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            for i in range(x, xend):
                if ayuda == 29:
                    if dondex == -1:
                        dondex = x
                    if dondey == -1:
                        dondey = y
                ayuda += 1
                if punteada == True:
                    if int(ayuda/10) % 2 == 1:
                        self.draw_point(x, y, color=colorHex)
                else:
                    self.draw_point(x, y, color=colorHex)
                x = x+1 if x < x1 else x-1
                if p < 0:
                    p += incE
                else:
                    y = y+1 if y < y1 else y-1
                    p += incNE
        else:
            p = 2*dx-dy
            incE = 2*dx
            incNE = 2*(dx-dy)
            if y0 > y1:
                y = y1
                x = x1
                yend = y0
                xend = x0
            else:
                y = y0
                x = x0
                yend = y1
                xend = x1
            if y0 > y1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            ayuda = 0
            for i in range(y, yend):
                if ayuda == 29:
                    if dondex == -1:
                        dondex = x
                    if dondey == -1:
                        dondey = y
                ayuda += 1
                self.draw_point(x, y, color=colorHex)
                y = y+1 if y < y1 else y-1
                if p < 0:
                    p += incE
                else:
                    x = x+1 if x < x1 else x-1
                    p += incNE

    def linea(self, x1, y1, x2, y2, ancho, color):

        BresenhamCanvas.bresenham(self, x1, y1, x2, y2, color)
        if ancho == 0:
            return
        vx = x2-x1
        vy = y2-y1
        # vector A,B extermos de la linea

        # perpendicular a AB
        wx = vy
        wy = -vx
        modulo = math.sqrt(wx*wx+wy*wy)
        wx /= modulo
        wy /= modulo
        modulo = math.sqrt(vx*vx+vy*vy)
        vx /= modulo
        vy /= modulo
        arribax = int(x1+wx*ancho)
        arribay = int(y1+wy*ancho)
        abajox = int(x1-wx*ancho)
        abajoy = int(y1-wy*ancho)
        BresenhamCanvas.bresenham(
            self, abajox, abajoy, arribax, arribay, color)
        arribax2 = int(x2+wx*ancho)
        arribay2 = int(y2+wy*ancho)
        abajox2 = int(x2-wx*ancho)
        abajoy2 = int(y2-wy*ancho)

        BresenhamCanvas.bresenham(
            self, abajox2, abajoy2, arribax2, arribay2, color)
        BresenhamCanvas.bresenham(
            self, arribax, arribay, arribax2, arribay2, color)
        BresenhamCanvas.bresenham(
            self, abajox, abajoy, abajox2, abajoy2, color)
        #print("donde  ",dondex," ",dondey)
        if ancho > 1:
            BresenhamCanvas.floodfill(self, dondex, dondey, color)
        # dondex=-1
        # dondey=-1
        # bresenham(arribax,arribay,abajox,abajoy)
        # floodfill(blank,abajox,abajoy,0)

    def floodfill(self, x, y, color="red"):
        global mat
        self.draw_point(x, y, color)
        for i in range(len(dx)):
            x1 = x+dx[i]
            y1 = y+dy[i]
            if (x1 > 0 and y1 > 0 and mat[x1][y1] == "none"):
                BresenhamCanvas.floodfill(self, x1, y1, color)

    def drawLineaConGrosor(self):
        setpoints_lineaCG()
        #self.linea(300, 300, 5, 200, 5)
        self.linea(x0, y0, x1, y1, groso)

    def drawLineaConGrosorFiguras(self, x, y, xe, ye):
        setpoints_lineaCG()
        #self.linea(300, 300, 5, 200, 5)
        self.linea(x, y, xe, ye, groso)

    def clippingControl(self, x, y):
        return x < 1900 and y < 1080 and x > 0 and y > 0

    def draw_line1(self, x0, y0, x1, y1):
        dx = abs(x1-x0)
        dy = abs(y1-y0)
        p = 2*dy-dx if dx > dy else 2*dx-dy
        incE = 2*dy if dx > dy else 2*dx
        incNE = 2*(dy-dx) if dx > dy else 2*(dx-dy)
        if (x0 > x1) and (y0 > y1):
            x, y = x1, y1
            xend, yend = x0, y0
        else:
            x, y = x0, y0
            xend, yend = x1, y1
        if dx > dy:
            start = x
            end = xend
        else:
            start = y
            end = yend

        self.draw_point(x, y, color=colorHex)
        for i in range(start, end):
            if dx > dy:
                x = x+1 if x < x1 else x-1
            else:
                y = y+1 if y < y1 else y-1
            if p < 0:
                p += incE
            else:
                if dx > dy:
                    y = y+1 if y < y1 else y-1
                else:
                    x = x+1 if x < x1 else x-1
                p += incNE
            self.draw_point(x, y, color=colorHex)

    def draw_line(self, x0, y0, x1, y1, color):
        dx = (x1-x0)
        dy = (y1-y0)
        if dy < 0:
            dy = -dy
            stepy = -1
        else:
            stepy = 1
        if dx < 0:
            dx = -dx
            stepx = -1
        else:
            stepx = 1
        x = x0
        y = y0
        self.draw_point(x, y, color=colorHex)
        if (dx > dy):
            p = 2 * dy-dx
            incE = 2 * dy
            incNE = 2 * (dy-dx)
            while (x != x1):
                x = x + stepx
                if p < 0:
                    p = p + incE
                else:
                    y = y + stepy
                    p = p + incNE
                self.draw_point(x, y, color=colorHex)
        else:
            p = 2 * dx - dy
            incE = 2 * dx
            incNE = 2 * (dx-dy)
            while y != y1:
                y = y + stepy
                if p < 0:
                    p = p + incE
                else:
                    x = x + stepx
                    p = p + incNE
                self.draw_point(x, y, color=colorHex)

    def draw_circunf(self, xc, yc, radio, color):
        x = 0
        y = radio
        p = 1 - radio
        self.draw_point(xc+x, yc+y, color)
        self.draw_point(xc+x, yc-y, color)
        self.draw_point(xc-x, yc+y, color)
        self.draw_point(xc-x, yc-y, color)
        self.draw_point(xc+y, yc+x, color)
        self.draw_point(xc-y, yc+x, color)
        self.draw_point(xc+y, yc-x, color)
        self.draw_point(xc-y, yc-x, color)

        while (x < y):
            x += 1
            if p < 0:
                p = p + 2*x + 1
            else:
                y -= 1
                p = p + 2*(x-y) + 1
            self.draw_point(xc+x, yc+y, color)
            self.draw_point(xc+x, yc-y, color)
            self.draw_point(xc-x, yc+y, color)
            self.draw_point(xc-x, yc-y, color)
            self.draw_point(xc+y, yc+x, color)
            self.draw_point(xc-y, yc+x, color)
            self.draw_point(xc+y, yc-x, color)
            self.draw_point(xc-y, yc-x, color)

    def borde(self, x, y, grosor):
        for i in range(-grosor, grosor+1):
            for l in range(-grosor, grosor+1):
                self.draw_point(x+i, y+l, color=colorHex)

    def draw_circunf_grosor(self, xc, yc, radio, color):
        setpoints_lineaCG()
        x = 0
        y = radio
        p = 1 - radio
        self.draw_point(xc+x, yc+y, color)
        self.draw_point(xc-x, yc+y, color)
        self.draw_point(xc+x, yc-y, color)
        self.draw_point(xc-x, yc-y, color)
        self.draw_point(xc+y, yc+x, color)
        self.draw_point(xc-y, yc+x, color)
        self.draw_point(xc+y, yc-x, color)
        self.draw_point(xc-y, yc-x, color)
        while (x < y):
            x += 1
            if p < 0:
                p = p + 2*x + 1
            else:
                y -= 1
                p = p + 2*(x-y) + 1
            self.borde(xc+x, yc+y, groso)
            self.draw_point(xc+x, yc+y, color)
            self.borde(xc-x, yc+y, groso)
            self.draw_point(xc-x, yc+y, color)
            self.borde(xc+x, yc-y, groso)
            self.draw_point(xc+x, yc-y, color)
            self.borde(xc-x, yc-y, groso)
            self.draw_point(xc-x, yc-y, color)
            self.borde(xc+y, yc+x, groso)
            self.draw_point(xc+y, yc+x, color)
            self.borde(xc-y, yc+x, groso)
            self.draw_point(xc-y, yc+x, color)
            self.borde(xc+y, yc-x, groso)
            self.draw_point(xc+y, yc-x, color)
            self.borde(xc-y, yc-x, groso)
            self.draw_point(xc-y, yc-x, color)

    def traslacion(self, x, y, tx, ty):
        matriz_traslacion = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
        coordenadas = np.array([x, y, 1])
        return np.dot(matriz_traslacion, coordenadas)

    def rotacion2(self, x, y, grado):
        matriz_traslacion = np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])
        matriz_rotacion = np.array([[math.cos(grado), (math.sin(
            grado)), 0], [-(math.sin(grado)), math.cos(grado), 0], [0, 0, 1]])
        multi = np.dot(matriz_traslacion, matriz_rotacion)
        matriz_traslacion2 = np.array([[1, 0, -x], [0, 1, -y], [0, 0, 1]])
        matriz_final = np.dot(multi, matriz_traslacion2)
        return matriz_final

    def rotacion3(self, x, y, matriz):
        coordenadas = np.array([x, y, 1])
        array_float = np.dot(matriz, coordenadas)
        return np.asarray(array_float, dtype=int)

    def escalacion(self, x, y, sx, sy):
        matriz_escalacion = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        coordenadas = np.array([x, y, 1])
        return np.dot(matriz_escalacion, coordenadas)

    def escalacion2(self, x, y, sx, sy):
        matriz_traslacion = np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])
        matriz_escalacion = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        multi = np.dot(matriz_traslacion, matriz_escalacion)
        matriz_traslacion2 = np.array([[1, 0, -x], [0, 1, -y], [0, 0, 1]])
        matriz_final = np.dot(multi, matriz_traslacion2)
        return np.asarray(matriz_final, dtype=int)

    def escalacion3(self, x, y, matriz):
        coordenadas = np.array([x, y, 1])
        return np.dot(matriz, coordenadas)


thereIsCircle = False
thereIsRectangle = False
thereIsTriangle = False


class Figura:

    def draw(self, objeto):
        if objeto.__class__.__name__ is Circle:
            objeto.drawCircle()
        if objeto.__class__.__name__ is Rectangle:
            objeto.drawRectangle()
        if objeto.__class__.name__ is Triangle:
            objeto.drawTriangle()


class Circle(Figura):

    def __init__(self):
        self.xcenterP = 0
        self.ycenterP = 0
        self.radiousP = 10

    def modify(self, xcenter, ycenter, radious):
        self.xcenterP = xcenter
        self.ycenterP = ycenter
        self.radiousP = radious

    def draw_circle(self, xcenter, ycenter, radious):
        canvas.draw_circunf(xcenter, ycenter, radious, color=colorHex)
        self.modify(xcenter, ycenter, radious)

    def drawCircle(self):
        setpoints_circ()
        self.draw_circle(xc, yc, r-xc)
        self.modify(xc, yc, r-xc)

    def draw_circle_automat(self):
        global xcenterP, ycenterP, radiousP
        canvas.draw_circunf(self.xcenterP, self.ycenterP,
                            self.radiousP, color=colorHex)

    def traslation_circle(self):
        global xcenterP, ycenterP, radiousP
        coordinates_traslation()
        array = canvas.traslacion(self.xcenterP, self.ycenterP, coordx, coordy)
        self.draw_circle(array[0], array[1], self.radiousP)

    def rotation_circle(self):
        global xcenterP, ycenterP, radiousP
        coordinates_rotation()
        setpoints_punto_pivote()
        matrizCal = canvas.rotacion2(pivx, pivy, angulo)
        arrayAux = canvas.rotacion3(self.xcenterP, self.ycenterP, matrizCal)
        self.draw_circle(arrayAux[0], arrayAux[1], self.radiousP)

    def escalation_circle(self):
        global xcenterP, ycenterP, radiousP
        coordinates_escalation()
        setpoints_punto_pivote()
        # array = canvas.escalacion(self.xcenterP,self.ycenterP,coorx,coory) #demostracion
        # self.draw_circle(array[0],array[1],(self.radiousP*coorx)-array[0]) #demostracion
        matrizCal = canvas.escalacion2(pivx, pivy, coorx, coory)
        arrayAux = canvas.escalacion3(self.xcenterP, self.ycenterP, matrizCal)
        self.draw_circle(arrayAux[0], arrayAux[1], (self.radiousP*coorx))

    def draw_grosor(self):
        global xcenterP, ycenterP, radiousP
        canvas.draw_circunf_grosor(
            self.xcenterP, self.ycenterP, self.radiousP, color=colorHex)


class Rectangle(Figura):

    def __init__(self):
        self.x0P = 0
        self.y0P = 0
        self.x1P = 2
        self.y1P = 2
        self.x2P = 2
        self.y2P = 0
        self.x3P = 2
        self.y3P = 0

    def modify(self, x0, y0, x1, y1):
        self.x0P = x0
        self.y0P = y0
        self.x1P = x1
        self.y1P = y1

    def modify2(self, x0, y0, x1, y1, x2, y2, x3, y3):
        self.modify(x0, y0, x1, y1)
        self.x2P = x2
        self.y2P = y2
        self.x3P = x3
        self.y3P = y3

    def draw_rectangle(self, x0, y0, x1, y1):
        canvas.draw_line(x0, y0, x1, y0, color=colorHex)
        canvas.draw_line(x0, y1, x1, y1, color=colorHex)
        canvas.draw_line(x1, y0, x1, y1, color=colorHex)
        canvas.draw_line(x0, y0, x0, y1, color=colorHex)
        self.modify(x0, y0, x1, y1)

    def draw_rectangle2(self, x0, y0, x1, y1, x2, y2, x3, y3):
        canvas.draw_line(x0, y0, x2, y2, color=colorHex)
        canvas.draw_line(x0, y0, x3, y3, color=colorHex)
        canvas.draw_line(x3, y3, x1, y1, color=colorHex)
        canvas.draw_line(x2, y2, x1, y1, color=colorHex)
        self.modify2(x0, y0, x1, y1, x2, y2, x3, y3)

    def drawRectangle(self):
        setpoints_square()
        self.draw_rectangle(x0, y0, x1, y1)
        self.modify(x0, y0, x1, y1)

    def draw_rectangle_automat(self):
        global x0P, y0P, x1P, y1P
        self.draw_rectangle(self.x0P, self.y0P, self.x1P, self.y1P)

    def traslation_rectangle(self):
        global x0P, y0P, x1P, y1P
        coordinates_traslation()
        array2 = canvas.traslacion(self.x0P, self.y0P, coordx, coordy)
        array3 = canvas.traslacion(self.x1P, self.y1P, coordx, coordy)
        self.draw_rectangle(array2[0], array2[1], array3[0], array3[1])

    def rotation_rectangle(self):
        global x0P, y0P, x1P, y1P, x2P, y2P, x3P, y3P
        coordinates_rotation()
        setpoints_punto_pivote()
        self.x2P, self.y2P = self.x1P, self.y0P
        self.x3P, self.y3P = self.x0P, self.y1P
        matrizCal = canvas.rotacion2(pivx, pivy, angulo)
        array2 = canvas.rotacion3(self.x0P, self.y0P, matrizCal)
        array3 = canvas.rotacion3(self.x1P, self.y1P, matrizCal)
        array4 = canvas.rotacion3(self.x2P, self.y2P, matrizCal)
        array5 = canvas.rotacion3(self.x3P, self.y3P, matrizCal)
        self.draw_rectangle2(array2[0], array2[1], array3[0],
                             array3[1], array4[0], array4[1], array5[0], array5[1])

    def escalation_rectangle(self):
        global x0P, y0P, x1P, y1P
        coordinates_escalation()
        setpoints_punto_pivote()
        matrizCalc = canvas.escalacion2(pivx, pivy, coorx, coory)
        array2 = canvas.escalacion3(self.x0P, self.y0P, matrizCalc)
        array3 = canvas.escalacion3(self.x1P, self.y1P, matrizCalc)
        self.draw_rectangle(array2[0], array2[1], array3[0], array3[1])

    def draw_grosor(self):
        global x0P, y0P, x1P, y1P
        canvas.drawLineaConGrosorFiguras(
            self.x0P, self.y0P, self.x1P, self.y0P)
        canvas.drawLineaConGrosorFiguras(
            self.x0P, self.y1P, self.x1P, self.y1P)
        canvas.drawLineaConGrosorFiguras(
            self.x1P, self.y0P, self.x1P, self.y1P)
        canvas.drawLineaConGrosorFiguras(
            self.x0P, self.y0P, self.x0P, self.y1P)


class Triangle(Figura):

    def __init__(self):
        self.x0p = 0
        self.y0p = 0
        self.x1p = 0
        self.y1p = 0
        self.x2p = 0
        self.y2p = 0

    def modify(self, x0, y0, x1, y1, x2, y2):
        self.x0p = x0
        self.y0p = y0
        self.x1p = x1
        self.y1p = y1
        self.x2p = x2
        self.y2p = y2

    def draw_triangle(self, x0, y0, x1, y1, x2, y2):
        canvas.draw_line(x0, y0, x1, y1, color=colorHex)
        canvas.draw_line(x1, y1, x2, y2, color=colorHex)
        canvas.draw_line(x2, y2, x0, y0, color=colorHex)
        self.modify(x0, y0, x1, y1, x2, y2)

    def drawTriangle(self):
        setpoints_triangle()
        self.draw_triangle(x0, y0, x1, y1, x2, y2)
        self.modify(x0, y0, x1, y1, x2, y2)

    def draw_triangle_automat(self):
        global x0p, y0p, x1p, y1p, x2p, y2p
        self.draw_triangle(self.x0p, self.y0p, self.x1p,
                           self.y1p, self.x2p, self.y2p)

    def traslation_triangle(self):
        global x0p, y0p, x1p, y1p, x2p, y2p
        coordinates_traslation()
        setpoints_triangle()
        array0 = canvas.traslacion(self.x0p, self.y0p, coordx, coordy)
        array1 = canvas.traslacion(self.x1p, self.y1p, coordx, coordy)
        array2 = canvas.traslacion(self.x2p, self.y2p, coordx, coordy)
        self.draw_triangle(array0[0], array0[1],
                           array1[0], array1[1], array2[0], array2[1])

    def rotation_triangle(self):
        global x0p, y0p, x1p, y1p, x2p, y2p
        coordinates_rotation()
        setpoints_punto_pivote()
        matrizCal = canvas.rotacion2(pivx, pivy, angulo)
        array0 = canvas.rotacion3(self.x0p, self.y0p, matrizCal)
        array1 = canvas.rotacion3(self.x1p, self.y1p, matrizCal)
        array2 = canvas.rotacion3(self.x2p, self.y2p, matrizCal)
        self.draw_triangle(array0[0], array0[1],
                           array1[0], array1[1], array2[0], array2[1])

    def escalation_triangle(self):
        global x0p, y0p, x1p, y1p, x2p, y2p
        coordinates_escalation()
        setpoints_punto_pivote()
        setpoints_triangle()
        matrizCal = canvas.escalacion2(pivx, pivy, coorx, coory)
        array0 = canvas.escalacion3(self.x0p, self.y0p, matrizCal)
        array1 = canvas.escalacion3(self.x1p, self.y1p, matrizCal)
        array2 = canvas.escalacion3(self.x2p, self.y2p, matrizCal)
        self.draw_triangle(array0[0], array0[1],
                           array1[0], array1[1], array2[0], array2[1])

    def draw_grosor(self):
        global x0p, y0p, x1p, y1p, x2p, y2p
        canvas.drawLineaConGrosorFiguras(
            self.x0p, self.y0p, self.x1p, self.y1p)
        canvas.drawLineaConGrosorFiguras(
            self.x1p, self.y1p, self.x2p, self.y2p)
        canvas.drawLineaConGrosorFiguras(
            self.x0p, self.y0p, self.x2p, self.y2p)


circle1 = Circle()
rectangle1 = Rectangle()
triangle1 = Triangle()
figuras = []


def traslation():
    global thereIsCircle, thereIsTriangle, thereIsRectangle
    global circle1, rectangle1
    canvas.delete('all')
    if thereIsCircle:
        figuras[len(figuras)-1].traslation_circle()
    if thereIsRectangle:
        figuras[len(figuras)-1].traslation_rectangle()
    if thereIsTriangle:
        figuras[len(figuras)-1].traslation_triangle()


def rotation():
    global thereIsCircle, thereIsTriangle, thereIsRectangle
    global circle1, rectangle1
    canvas.delete('all')
    coordinates_rotation()
    setpoints_punto_pivote()
    if thereIsCircle:
        figuras[len(figuras)-1].rotation_circle()
    if thereIsRectangle:
        figuras[len(figuras)-1].rotation_rectangle()
    if thereIsTriangle:
        figuras[len(figuras)-1].rotation_triangle()


def escalation():
    global thereIsCircle, thereIsTriangle, thereIsRectangle
    global circle1, rectangle1
    canvas.delete('all')
    coordinates_escalation()
    setpoints_punto_pivote()
    if thereIsCircle:
        figuras[len(figuras)-1].escalation_circle()
    if thereIsRectangle:
        figuras[len(figuras)-1].escalation_rectangle()
    if thereIsTriangle:
        figuras[len(figuras)-1].escalation_triangle()


def drawCircle1():
    global thereIsCircle, thereIsTriangle, thereIsRectangle, figuras
    global circle1
    thereIsCircle = True
    # canvas.delete('all')
    thereIsRectangle = False
    thereIsTriangle = False
    circle1.drawCircle()
    figuras.append(Circle())
    dibujar(figuras[len(figuras)-1])


def drawRectangle1():
    global thereIsCircle, thereIsTriangle, thereIsRectangle
    thereIsRectangle = True
    # canvas.delete('all')
    thereIsCircle = False
    thereIsTriangle = False
    rectangle1.drawRectangle()
    figuras.append(Rectangle())
    dibujar(figuras[len(figuras)-1])


def drawTriangle1():
    global thereIsCircle, thereIsTriangle, thereIsRectangle
    thereIsTriangle = True
    # canvas.delete('all')
    thereIsCircle = False
    thereIsRectangle = False
    triangle1.drawTriangle()
    figuras.append(Triangle())
    dibujar(figuras[len(figuras)-1])


def drawLineaconGrosor1():
    canvas.delete('all')
    global thereIsCircle, thereIsTriangle, thereIsRectangle
    inLinea()
    if thereIsRectangle:
        rectangle1.draw_grosor()
    if thereIsTriangle:
        triangle1.draw_grosor()
    if thereIsCircle:
        circle1.draw_grosor()
    # clear_canvas()


def dibujar(figura):
    global figuras
    figuras.remove(figura)
    figuras.append(figura)
    redibujar()


def redibujar():
    global figuras
    canvas.delete('all')
    for figura in figuras:
        try:
            if figura.__class__.__name__ == 'Circle':
                if figura.xcenterP == 0:
                    figura.drawCircle()
                else:
                    figura.draw_circle_automat()
            if figura.__class__.__name__ == 'Rectangle':
                if figura.x0P == 0:
                    figura.drawRectangle()
                else:
                    figura.draw_rectangle_automat()
            if figura.__class__.__name__ == 'Triangle':
                if figura.x0p == 0:
                    figura.drawTriangle()
                else:
                    figura.draw_triangle_automat()
        except:
            print("No hay más figuras")


def borrar():
    figuras.pop(len(figuras)-1)
    redibujar()


def limpiar():
    # clear_canvas()
    init()
    global donde, dondey, punteada
    punteada = False
    dondex = -1
    dondey = -1
    puntosx.clear()
    puntosy.clear()


def press_button_mouse(event):
    puntosx.append(event.x)
    puntosy.append(event.y)
    canvas.create_oval(event.x-2, event.y-2, event.x +
                       2, event.y+2, fill=colorHex)


def setpoints_circ():
    global xc, yc, r, p
    if len(puntosx) < 1:
        xc = puntosx[0]
        yc = puntosy[0]
        r = puntosx[1]
    else:
        xc = puntosx[len(puntosx)-2]
        yc = puntosy[len(puntosy)-2]
        r = puntosx[len(puntosx)-1]


def setpoints_square():
    global x0, y0, x1, y1
    if len(puntosx) < 1:
        x0 = puntosx[0]
        y0 = puntosy[0]
        x1 = puntosx[1]
        y1 = puntosy[1]
    else:
        x0 = puntosx[len(puntosx)-2]
        y0 = puntosy[len(puntosy)-2]
        x1 = puntosx[len(puntosx)-1]
        y1 = puntosy[len(puntosy)-1]


def setpoints_triangle():
    global x0, y0, x1, y1, x2, y2
    if len(puntosx) < 1:
        x0 = puntosx[0]
        y0 = puntosy[0]
        x1 = puntosx[1]
        y1 = puntosy[1]
        x2 = puntosx[2]
        y2 = puntosy[2]
    else:
        x0 = puntosx[len(puntosx)-3]
        y0 = puntosy[len(puntosy)-3]
        x1 = puntosx[len(puntosx)-2]
        y1 = puntosy[len(puntosy)-2]
        x2 = puntosx[len(puntosx)-1]
        y2 = puntosy[len(puntosy)-1]


def setpoints_punto_pivote():
    global pivx, pivy
    pivx = puntosx[len(puntosx)-1]
    pivy = puntosy[len(puntosy)-1]


def setpoints_lineaCG():
    global x0, y0, x1, y1, x2, y2
    x0 = puntosx[0]
    y0 = puntosy[0]
    x1 = puntosx[1]
    y1 = puntosy[1]


def savefile():
    file = filedialog.asksaveasfilename(initialdir="C:/",
                                        filetypes=(('PNG File', '.PNG'), ('PNG File', '.PNG')))
    file = file + ".PNG"
    ImageGrab.grab().crop((70, 70, 1500, 1000)).save(file)


def clear_canvas():
    init()
    global dondex, dondey
    dondey = -1
    dondex = -1
    canvas.delete('all')
    puntosx.clear()
    puntosy.clear()
    figuras.clear()


def set_opcion_limpiar(choice):
    if choice == "Limpiar Canvas":
        clear_canvas()
    if choice == "Limpiar Puntos":
        limpiar()


def set_opcionfigura(choice):
    if choice == "Cuadrado":
        drawRectangle1()
    if choice == "Triangulo":
        drawTriangle1()
    if choice == "Circulo":
        drawCircle1()


def set_grosor(choice):
    global grosor
    if choice == "Grosor 1":
        grosor = int("1")
        drawLineaconGrosor1()
    if choice == "Grosor 2":
        grosor = int("2")
        drawLineaconGrosor1()
    if choice == "Grosor 3":
        grosor = int("3")
        drawLineaconGrosor1()


def create_menu():
    init()
    opciones_figura = customtkinter.StringVar(value="Figuras")
    combobox_figura = customtkinter.CTkOptionMenu(master=window, values=["Cuadrado", "Triangulo", "Circulo"],
                                                  command=set_opcionfigura,
                                                  variable=opciones_figura)
    combobox_figura.place(x=10, y=10)

    opciones_limpiar = customtkinter.StringVar(value="Limpiar")
    combobox_limpiar = customtkinter.CTkOptionMenu(master=window, values=[
                                                   "Limpiar Canvas", "Limpiar Puntos"], command=set_opcion_limpiar, variable=opciones_limpiar)
    combobox_limpiar.place(x=350, y=10)

    option_grosor = customtkinter.StringVar(value="Grosor")
    combobox_grosor = customtkinter.CTkOptionMenu(
        master=window, values=["Grosor 1", "Grosor 2", "Grosor 3"], command=set_grosor, variable=option_grosor)
    combobox_grosor.place(x=180, y=10)


def inLinea():
    global groso
    groso = grosor


def coordinates_traslation():
    global coordx, coordy
    coordx = int(entryX.get())
    coordy = int(entryY.get())


def coordinates_rotation():
    global angulo
    angulo = valorRotacion


def coordinates_escalation():
    global coorx, coory
    coorx = int(entryX1.get())
    coory = int(entryY1.get())


def cambiarPunteada():
    global punteada
    punteada = True
    drawLineaconGrosor1()


def colors():
    global colorHex
    color = colorchooser.askcolor()
    colorHex = color[1]
    print(colorHex)


def open_dialog():
    global valorRotacion
    dialog = customtkinter.CTkInputDialog(
        master=None, text="Angulo:", title="Ingrese un angulo")
    valorRotacion = int(dialog.get_input())
    rotation()


def create_buttons():
    global entryX, entryY, entryX1, entryY1
    button_color = customtkinter.CTkButton(
        master=window, text="Color", command=colors)
    button_color.place(x=520, y=10)
    button_rotar = customtkinter.CTkButton(
        master=window, text="Rotar", command=open_dialog)
    button_rotar.place(x=690, y=10)
    button_trasladar = customtkinter.CTkButton(
        master=window, text="Trasladar", command=traslation)
    button_trasladar.place(x=1320, y=40)
    label1 = customtkinter.CTkLabel(
        master=window, text="X:").place(x=1240, y=90)
    entryX = customtkinter.CTkEntry(
        master=window, placeholder_text="Punto x")
    entryX.pack()
    entryX.place(x=1320, y=90)
    label2 = customtkinter.CTkLabel(
        master=window, text="Y:").place(x=1240, y=130)
    entryY = customtkinter.CTkEntry(
        master=window, placeholder_text="Punto y")
    entryY.pack()
    entryY.place(x=1320, y=130)

    button_escalar = customtkinter.CTkButton(
        master=window, text="Escalar", command=escalation).place(x=1320, y=180)
    label3 = customtkinter.CTkLabel(
        master=window, text="X:").place(x=1240, y=220)
    entryX1 = customtkinter.CTkEntry(
        master=window, placeholder_text="Punto x")
    entryX1.pack()
    entryX1.place(x=1320, y=220)
    label4 = customtkinter.CTkLabel(
        master=window, text="Y:").place(x=1240, y=260)
    entryY1 = customtkinter.CTkEntry(
        master=window, placeholder_text="Punto y")
    entryY1.pack()
    entryY1.place(x=1320, y=260)

    button_pintar = customtkinter.CTkButton(
        master=window, text="Pintar").place(x=1320, y=310)
    button_save = customtkinter.CTkButton(
        master=window, text="Guardar Imagen", command=savefile).place(x=1320, y=380)

    button_close = customtkinter.CTkButton(
        master=window, text="Cerrar App", command=window.destroy).place(x=1320, y=700)


def create_canvas():
    global canvas
    canvas = BresenhamCanvas(window, width=1540, height=950)
    canvas.bind("<Button-1>", press_button_mouse)
    canvas.place(x=0, y=70)


def main():
    global window, puntosx, puntosy, circle, colorHex
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    puntosx = []
    puntosy = []
    window = customtkinter.CTk()
    window.geometry("1540x800+0+0")
    window.title("GUI grafi")
    window.resizable(0, 0)
    create_menu()
    create_buttons()
    create_canvas()

    window.mainloop()


if __name__ == '__main__':
    main()
