from tkinter import *


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
        if dx > dy :
            start = x
            end = xend 
        else:
            start = y
            end = yend
            
        self.draw_point(x, y, color=color)
        for i in range(start,end):
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
    canvas = BresenhamCanvas(window, width=500, height=700)
    canvas.pack(side=LEFT)
    canvas.draw_line(100, 100, 200, 100, color="blue")
    canvas.draw_line(100, 100, 100, 200, color="blue")
    canvas.draw_line(200, 100, 200, 200, color="blue")
    canvas.draw_line(100, 200, 200, 200, color="blue")


def main():
    global window
    window = Tk()
    window.geometry("700x700")
    window.title("GUI grafi")
    window.resizable(0, 0)
    window.config(background="#1c1c1c")

    label = Label(window, text="  Choose your \n figure to draw", fg="white", bg="#1c1c1c", font=("Verdana", 15)).place(
        x=515, y=60)

    buton_square = Button(window, text="Square", font=(
        "Comic Sans", 15), width=10, command=drawsquare)
    buton_square.place(x=540, y=150)

    buton_square = Button(window, text="Triangle",
                          font=("Comic Sans", 15), width=10)
    buton_square.place(x=540, y=200)

    buton_square = Button(window, text="Circle",
                          font=("Comic Sans", 15), width=10)
    buton_square.place(x=540, y=250)

    window.mainloop()


if __name__ == '__main__':
    main()
