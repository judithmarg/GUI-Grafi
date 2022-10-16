from tkinter import *
from tkinter import filedialog
from PIL import ImageGrab
from cv2 import circle
import numpy as np
import math

class BresenhamCanvas(Canvas):

    def draw_point(self, x, y, color):
        if self.clippingControl(x,y):
            self.create_line(x, y, x+1, y+1, fill=color, width=2)
            
    def clippingControl (self,x,y):
        return x < 1900 and y < 1080 and x > 0 and  y > 0
    
    def draw_line1(self, x0, y0, x1, y1, color="red"):
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

        self.draw_point(x, y, color=color)
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

            self.draw_point(x, y, color=color)
    def draw_line(self, x0, y0, x1, y1, color="red"):
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
        self.draw_point(x, y, color=color)
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
                self.draw_point(x, y, color=color)
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
                self.draw_point(x, y, color=color)
                
    def draw_circunf(self,xc, yc, radio, color):
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
                p = p + 2*x +1
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
    
    def traslacion(self, x, y, tx, ty):
        matriz_traslacion = np.array([[1,0,tx],[0,1,ty],[0,0,1]])
        coordenadas = np.array([x,y,1])
        return np.dot(matriz_traslacion, coordenadas)

    def rotacion2(self,x,y, grado):
        matriz_traslacion = np.array([[1,0,x],[0,1,y],[0,0,1]])
        matriz_rotacion = np.array([[math.cos(grado), (math.sin(grado)),0],[-(math.sin(grado)),math.cos(grado),0],[0,0,1]])
        multi = np.dot(matriz_traslacion, matriz_rotacion)
        matriz_traslacion2 = np.array([[1,0,-x],[0,1,-y],[0,0,1]])
        matriz_final = np.dot(multi, matriz_traslacion2)
        return matriz_final
    
    def rotacion3(self,x,y,matriz):
        coordenadas = np.array([x,y,1])
        array_float = np.dot(matriz, coordenadas)
        return np.asarray(array_float, dtype=int)
     
    def escalacion(self,x,y,sx,sy):
        matriz_escalacion = np.array([[sx,0,0],[0,sy,0],[0,0,1]])
        coordenadas = np.array([x,y,1])
        return np.dot(matriz_escalacion, coordenadas)

    def escalacion2(self, x, y, sx, sy):
        matriz_traslacion = np.array([[1,0,x],[0,1,y],[0,0,1]])
        matriz_escalacion = np.array([[sx,0,0],[0,sy,0],[0,0,1]])
        multi = np.dot(matriz_traslacion, matriz_escalacion)
        matriz_traslacion2 = np.array([[1,0,-x],[0,1,-y],[0,0,1]])
        matriz_final = np.dot(multi, matriz_traslacion2)
        return np.asarray(matriz_final, dtype = int)
    
    def escalacion3(self,x,y,matriz):
        coordenadas = np.array([x,y,1])
        return np.dot(matriz, coordenadas)
        
thereIsCircle = False
thereIsRectangle = False
thereIsSquare = False
thereIsTriangle = False

class Circle:

    def __init__(self):
        self.xcenterP = 0
        self.ycenterP = 0
        self.radiousP = 10
    
    def modify(self,xcenter,ycenter, radious):
        self.xcenterP = xcenter
        self.ycenterP = ycenter
        self.radiousP = radious
    
    def draw_circle(self,xcenter, ycenter, radious):
        canvas.draw_circunf(xcenter,ycenter,radious,color="red") 
        self.modify(xcenter,ycenter,radious)

    def drawCircle(self):
        setpoints_circ()
        self.draw_circle(xc, yc, r-xc)
        self.modify(xc,yc,r-xc)   
    
    def traslation_circle(self):
        global xcenterP, ycenterP, radiousP
        coordinates_traslation()
        array = canvas.traslacion(self.xcenterP ,self.ycenterP,coordx,coordy)
        self.draw_circle(array[0],array[1],self.radiousP)
    
    def rotation_circle(self):
        global xcenterP, ycenterP, radiousP
        coordinates_rotation()
        setpoints_punto_pivote()
        matrizCal = canvas.rotacion2(pivx,pivy,angulo)
        arrayAux = canvas.rotacion3(self.xcenterP,self.ycenterP,matrizCal)
        self.draw_circle(arrayAux[0], arrayAux[1], self.radiousP)
    
    def escalation_circle(self):
        global xcenterP, ycenterP, radiousP
        coordinates_escalation()
        setpoints_punto_pivote()
        #array = canvas.escalacion(self.xcenterP,self.ycenterP,coorx,coory) #demostracion
        #self.draw_circle(array[0],array[1],(self.radiousP*coorx)-array[0]) #demostracion
        matrizCal = canvas.escalacion2(pivx,pivy,coorx,coory)
        arrayAux = canvas.escalacion3(self.xcenterP,self.ycenterP,matrizCal)
        self.draw_circle(arrayAux[0], arrayAux[1], (self.radiousP*coorx))

class Rectangle:
    
    def __init__(self):
        self.x0P = 0
        self.y0P = 0
        self.x1P = 2
        self.y1P = 2 
        self.x2P = 2
        self.y2P = 0
        self.x3P = 2
        self.y3P = 0 

    def modify(self,x0,y0,x1,y1):
        self.x0P = x0
        self.y0P = y0
        self.x1P = x1
        self.y1P = y1
    
    def modify2(self,x0,y0,x1,y1,x2,y2,x3,y3):
        self.modify(x0,y0,x1,y1)
        self.x2P = x2
        self.y2P = y2
        self.x3P = x3
        self.y3P = y3

    def draw_rectangle(self,x0,y0,x1,y1):
        canvas.draw_line(x0, y0, x1, y0, color="blue")
        canvas.draw_line(x0, y1, x1, y1, color="blue")
        canvas.draw_line(x1, y0, x1, y1, color="blue")
        canvas.draw_line(x0, y0, x0, y1, color="blue")
        self.modify(x0,y0,x1,y1)

    def draw_rectangle2(self,x0,y0,x1,y1,x2,y2,x3,y3):
        canvas.draw_line(x0, y0, x2, y2, color="blue")
        canvas.draw_line(x0, y0, x3, y3, color="blue")
        canvas.draw_line(x3, y3, x1, y1, color="blue")
        canvas.draw_line(x2, y2, x1, y1, color="blue")
        self.modify2(x0,y0,x1,y1,x2,y2,x3,y3)

    def drawRectangle(self):
        setpoints_square()
        self.draw_rectangle(x0, y0, x1, y1)
        self.modify(x0,y0,x1,y1)   
    
    def traslation_rectangle(self):
        global x0P,y0P,x1P,y1P
        coordinates_traslation()
        array2 = canvas.traslacion(self.x0P,self.y0P,coordx,coordy)
        array3 = canvas.traslacion(self.x1P,self.y1P,coordx,coordy)
        self.draw_rectangle(array2[0], array2[1], array3[0], array3[1])
    
    def rotation_rectangle(self):
        global x0P,y0P,x1P,y1P,x2P,y2P,x3P,y3P
        coordinates_rotation()
        setpoints_punto_pivote()
        self.x2P,self.y2P = self.x1P,self.y0P
        self.x3P,self.y3P = self.x0P,self.y1P
        matrizCal = canvas.rotacion2(pivx,pivy,angulo)
        array2 = canvas.rotacion3(self.x0P,self.y0P,matrizCal)
        array3 = canvas.rotacion3(self.x1P,self.y1P,matrizCal)
        array4 = canvas.rotacion3(self.x2P,self.y2P,matrizCal)
        array5 = canvas.rotacion3(self.x3P,self.y3P,matrizCal)
        self.draw_rectangle2(array2[0], array2[1], array3[0], array3[1],array4[0], array4[1], array5[0], array5[1])
    
    def escalation_rectangle(self):
        global x0P,y0P,x1P,y1P
        coordinates_escalation()
        setpoints_punto_pivote()
        matrizCalc = canvas.escalacion2(pivx,pivy,coorx,coory)
        array2 = canvas.escalacion3(self.x0P,self.y0P,matrizCalc)
        array3 = canvas.escalacion3(self.x1P,self.y1P,matrizCalc)
        self.draw_rectangle(array2[0], array2[1], array3[0], array3[1])

class Triangle:

    def __init__(self):
        self.x0p = 0
        self.y0p = 0
        self.x1p = 0
        self.y1p = 0
        self.x2p = 0
        self.y2p = 0
    
    def modify(self,x0,y0,x1,y1,x2,y2):
        self.x0p = x0
        self.y0p = y0
        self.x1p = x1
        self.y1p = y1
        self.x2p = x2
        self.y2p = y2
    
    def draw_triangle(self,x0,y0,x1,y1,x2,y2):
        canvas.draw_line(x0, y0, x1, y1, color="blue")
        canvas.draw_line(x1, y1, x2, y2, color="blue")
        canvas.draw_line(x2, y2, x0, y0, color="blue")
        self.modify(x0,y0,x1,y1,x2,y2)

    def drawTriangle(self):
        setpoints_triangle()
        self.draw_triangle(x0, y0, x1, y1, x2, y2)
        self.modify(x0, y0, x1, y1, x2, y2)   
    
    def traslation_triangle(self):
        global x0p,y0p,x1p,y1p,x2p,y2p
        coordinates_traslation()
        setpoints_triangle()
        array0 = canvas.traslacion(self.x0p,self.y0p,coordx,coordy)
        array1 = canvas.traslacion(self.x1p,self.y1p,coordx,coordy)
        array2 = canvas.traslacion(self.x2p,self.y2p,coordx,coordy)
        self.draw_triangle(array0[0], array0[1], array1[0], array1[1], array2[0], array2[1])
    
    def rotation_triangle(self):
        global x0p,y0p,x1p,y1p,x2p,y2p
        coordinates_rotation()
        setpoints_punto_pivote()
        matrizCal = canvas.rotacion2(pivx,pivy,angulo)
        array0 = canvas.rotacion3(self.x0p,self.y0p,matrizCal)
        array1 = canvas.rotacion3(self.x1p,self.y1p,matrizCal)
        array2 = canvas.rotacion3(self.x2p,self.y2p,matrizCal)
        self.draw_triangle(array0[0], array0[1], array1[0], array1[1], array2[0], array2[1])
    
    def escalation_triangle(self):
        global x0p,y0p,x1p,y1p,x2p,y2p
        coordinates_escalation()
        setpoints_punto_pivote()
        setpoints_triangle()
        matrizCal = canvas.escalacion2(pivx,pivy,coorx,coory)
        array0 = canvas.escalacion3(self.x0p,self.y0p,matrizCal)
        array1 = canvas.escalacion3(self.x1p,self.y1p,matrizCal)
        array2 = canvas.escalacion3(self.x2p,self.y2p,matrizCal)
        self.draw_triangle(array0[0], array0[1], array1[0], array1[1], array2[0], array2[1])

circle1 = Circle()
rectangle1 = Rectangle()
triangle1 = Triangle()

def traslation():
    global thereIsCircle, thereIsSquare,thereIsTriangle,thereIsRectangle
    global circle1,rectangle1
    canvas.delete('all')
    if thereIsCircle:
        circle1.traslation_circle()
    if thereIsRectangle:
        rectangle1.traslation_rectangle()
    if thereIsTriangle:
        triangle1.traslation_triangle()

def rotation():
    global thereIsCircle, thereIsSquare,thereIsTriangle,thereIsRectangle
    global circle1,rectangle1
    canvas.delete('all')
    coordinates_rotation()
    setpoints_punto_pivote()
    if thereIsCircle:
        circle1.rotation_circle()
    if thereIsRectangle:
        rectangle1.rotation_rectangle()
    if thereIsTriangle:
        triangle1.rotation_triangle()

def escalation():
    global thereIsCircle, thereIsSquare,thereIsTriangle,thereIsRectangle
    global circle1,rectangle1
    canvas.delete('all')
    coordinates_escalation()
    setpoints_punto_pivote()
    if thereIsCircle:
        circle1.escalation_circle()
    if thereIsRectangle:
        setpoints_square()
        rectangle1.escalation_rectangle()
    if thereIsTriangle:
        triangle1.escalation_triangle()
        
def drawCircle1():
    global thereIsCircle, thereIsSquare,thereIsTriangle,thereIsRectangle
    global circle1
    thereIsCircle = True
    canvas.delete('all')
    thereIsRectangle = False
    thereIsSquare = False
    thereIsTriangle = False 
    circle1.drawCircle()

def drawRectangle1():
    global thereIsCircle, thereIsSquare,thereIsTriangle,thereIsRectangle
    thereIsRectangle = True
    canvas.delete('all')
    thereIsCircle = False
    thereIsSquare = False
    thereIsTriangle = False
    rectangle1.drawRectangle()

def drawTriangle1():
    global thereIsCircle, thereIsSquare,thereIsTriangle,thereIsRectangle
    thereIsTriangle = True
    canvas.delete('all')
    thereIsCircle = False
    thereIsRectangle = False
    thereIsSquare = False
    triangle1.drawTriangle()
    


def press_button_mouse(event):
    puntosx.append(event.x)
    puntosy.append(event.y)
    canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill="red")

def setpoints_circ():
    global xc, yc, r, p
    xc = puntosx[0]
    yc = puntosy[0]
    r = puntosx[1]

def setpoints_square():
    global x0, y0, x1, y1
    x0 = puntosx[0]
    y0 = puntosy[0]
    x1 = puntosx[1]
    y1 = puntosy[1]


def setpoints_triangle():
    global x0, y0, x1, y1, x2, y2
    x0 = puntosx[0]
    y0 = puntosy[0]
    x1 = puntosx[1]
    y1 = puntosy[1]
    x2 = puntosx[2]
    y2 = puntosy[2]

def setpoints_punto_pivote():
    global pivx, pivy
    pivx = puntosx[len(puntosx)-1]
    pivy = puntosy[len(puntosy)-1]

def savefile():
    file = filedialog.asksaveasfilename(initialdir="C:/",
                                        filetypes=(('PNG File', '.PNG'), ('PNG File', '.PNG')))
    file = file + ".PNG"
    ImageGrab.grab().crop((150, 150, 1500, 1000)).save(file)


def clear_canvas():
    canvas.delete('all')
    puntosx.clear()
    puntosy.clear()


def create_menu():
    menu_bar = Menu(window)
    window.config(menu=menu_bar)
    options1 = Menu(menu_bar, tearoff=0)
    options1.add_command(label="Clear", command=clear_canvas)
    options1.add_command(label="Save", command=savefile)
    menu_bar.add_cascade(label="Options", menu=options1)

def coordinates_traslation():
    global coordx, coordy
    coordx = int(entryX.get())
    coordy = int(entryY.get())
    
def coordinates_rotation():
    global angulo
    angulo = int(entryAngulo.get())
    
def coordinates_escalation():
    global coorx, coory
    coorx = int(entryX1.get())
    coory = int(entryY1.get())

def create_buttons():
    buton_square = Button(window, text="Square", 
                            font=("Comic Sans", 15), width=10, command=drawRectangle1)
    buton_square.place(x=1540, y=150)

    buton_triangle = Button(window, text="Triangle",
                            font=("Comic Sans", 15), width=10, command=drawTriangle1)
    buton_triangle.place(x=1540, y=200)

    buton_circle = Button(window, text="Circle",
                            font=("Comic Sans", 15), width=10, command=drawCircle1)
    buton_circle.place(x=1540, y=250)

    button_traslacion = Button(window, text="Trasladar", font=(
        "Comic Sans", 15), width=10, command=traslation)
    button_traslacion.place(x=1540,y=300)
    label1 = Label(window, text="x:", fg="white", bg="#1c1c1c", font=("Verdana", 10)).place(x=1570, y=350)
    global entryX, entryY
    entryX = Entry(window, font=("Arial",15), width=5)
    entryX.pack()
    entryX.place(x=1590,y=350)
    label2 = Label(window, text="y:", fg="white", bg="#1c1c1c", font=("Verdana", 10)).place(x=1670, y=350)
    entryY = Entry(window, font=("Arial",15), width=5)
    entryY.pack()
    entryY.place(x=1690,y=350)
    
    button_rotar = Button(window, text="Rotar", font=(
        "Comic Sans", 15), width=10, command=rotation)
    button_rotar.place(x=1540,y=400)
    label3 = Label(window, text="Angulo:", fg="white", bg="#1c1c1c", font=("Verdana", 10)).place(x=1530, y=450)
    global entryAngulo
    entryAngulo = Entry(window, font=("Arial",15), width=5)
    entryAngulo.pack()
    entryAngulo.place(x=1590,y=450)
    
    button_escalar = Button(window, text="Escalar", font=(
        "Comic Sans", 15), width=10, command=escalation)
    button_escalar.place(x=1540,y=500)
    label4 = Label(window, text="x:", fg="white", bg="#1c1c1c", font=("Verdana", 10)).place(x=1570, y=550)
    global entryX1, entryY1
    entryX1 = Entry(window, font=("Arial",15), width=5)
    entryX1.pack()
    entryX1.place(x=1590,y=550)
    label5 = Label(window, text="y:", fg="white", bg="#1c1c1c", font=("Verdana", 10)).place(x=1670, y=550)
    entryY1 = Entry(window, font=("Arial",15), width=5)
    entryY1.pack()
    entryY1.place(x=1690,y=550)
    
    
    button_close = Button(window, text="Close",
                          font=("Comic Sans", 15), width=10, command=window.destroy)
    button_close.place(x=1540, y=600)


def create_canvas():
    global canvas
    canvas = BresenhamCanvas(frame, width=1500, height=1700)
    # canvas.bind("<Motion>", mouse_move)
    canvas.bind("<Button-1>", press_button_mouse)
    canvas.pack(side=LEFT)


def main():
    global window, frame, puntosx, puntosy, circle
    puntosx = []
    puntosy = []
    window = Tk()
    window.geometry("1900x1000")
    window.title("GUI grafi")
    window.resizable(0, 0)
    window.config(background="#1c1c1c")
    create_menu()
    label = Label(window, text="  Choose your \n figure to draw", fg="white", bg="#1c1c1c", font=("Verdana", 15)).place(
        x=1515, y=60)
    create_buttons()
    frame = Frame(window, width=1500, height=1000, bg="white")
    frame.pack(side=LEFT)
    create_canvas()
    
    window.mainloop()


if __name__ == '__main__':
    main()

