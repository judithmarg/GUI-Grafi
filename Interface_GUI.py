from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageGrab


class BresenhamCanvas(Canvas):
    def draw_point(self, x, y, color="red"):
        self.create_line(x, y, x+1, y+1, fill=color, width=2)

    def draw_line(self, x0, y0, x1, y1, color="red"):
        dx = abs(x1-x0)
        dy = abs(y1-y0)
        p = 2*dy-dx if dx > dy else 2*dx-dy
        incE = 2*dy if dx > dy else 2*dx
        incNE = 2*(dy-dx) if dx > dy else 2*(dx-dy)
        if (x0 > x1) or (y0 > y1):
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


def drawsquare():
    canvas.delete('all')
    canvas.draw_line(x0, y0, x1, y1, color="blue")
    canvas.draw_line(x1, y1, x0, y0, color="blue")
    # canvas.draw_line(x1, y0, x1, x1, color="blue")
    # canvas.draw_line(x1, y0, x1, y1, color="blue")


def draw_triangle():
    canvas.delete('all')
    canvas.draw_line(100, 100, 200, 100, color="blue")
    canvas.draw_line(200, 100, 100, 200, color="blue")
    canvas.draw_line(100, 200, 100, 100, color="blue")


def setpoints():
    global x0, y0, x1, y1
    point1 = int(entry1.get())
    point2 = int(entry2.get())
    point3 = int(entry3.get())
    point4 = int(entry4.get())

    if type(point1) == int and type(point2) == int and type(point3) == int and type(point4) == int:
        x0 = point1
        y0 = point2
        x1 = point3
        y1 = point4
    else:
        messagebox.showwarning('Mensaje', 'Debe escribir un numero entero')


def savefile():
    file = filedialog.asksaveasfilename(initialdir="C:/",
                                        filetypes=(('PNG File', '.PNG'), ('PNG File', '.PNG')))
    file = file + ".PNG"
    ImageGrab.grab().crop((100, 100, 700, 700)).save(file)


def main():
    global window, frame, canvas, entry1, entry2, entry3, entry4
    window = Tk()
    window.geometry("700x700")
    window.title("GUI grafi")
    window.resizable(0, 0)
    window.config(background="#1c1c1c")

    label = Label(window, text="  Choose your \n figure to draw", fg="white", bg="#1c1c1c", font=("Verdana", 15)).place(
        x=515, y=60)
    label_point1 = Label(window, text="X0:", fg="white",
                         bg="#1c1c1c", font=("Verdana", 15)).place(x=15, y=15)
    label_point2 = Label(window, text="Y0:", fg="white",
                         bg="#1c1c1c", font=("Verdana", 15)).place(x=120, y=15)
    label_point3 = Label(window, text="X1:", fg="white",
                         bg="#1c1c1c", font=("Verdana", 15)).place(x=220, y=15)
    label_point4 = Label(window, text="Y1:", fg="white",
                         bg="#1c1c1c", font=("Verdana", 15)).place(x=320, y=15)
    entry1 = Entry(window, width=5)
    entry1.place(x=60, y=23)

    entry2 = Entry(window, width=5)
    entry2.place(x=160, y=23)

    entry3 = Entry(window, width=5)
    entry3.place(x=265, y=23)

    entry4 = Entry(window, width=5)
    entry4.place(x=360, y=23)

    buton_square = Button(window, text="Square", font=(
        "Comic Sans", 15), width=10, command=drawsquare)
    buton_square.place(x=540, y=150)

    buton_square = Button(window, text="Triangle",
                          font=("Comic Sans", 15), width=10, command=draw_triangle)
    buton_square.place(x=540, y=200)

    buton_square = Button(window, text="Circle",
                          font=("Comic Sans", 15), width=10)
    buton_square.place(x=540, y=250)

    button_save = Button(window, text="Save",
                         font=("Comic Sans", 15), width=10, command=savefile)
    button_save.place(x=540, y=300)
    button_save = Button(window, text="Save Points",
                         font=("Comic Sans", 10), width=10, command=setpoints)
    button_save.place(x=400, y=20)
    frame = Frame(window, width=500, height=600, bg="white")
    frame.pack(side=LEFT)
    canvas = BresenhamCanvas(frame, width=500, height=600)
    canvas.pack(side=LEFT)

    window.mainloop()


if __name__ == '__main__':
    main()
