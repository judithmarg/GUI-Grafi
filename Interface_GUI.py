from tkinter import *


class BresenhamCanvas(Canvas):
    def draw_point(self, x, y, color="red"):
        self.create_line(x, y, x+1, y+1, fill=color, width=2)

    def draw_line(self, x0, y0, x1, y1, color="red"):
        stepy = 0
        stepx = 0
        dx = abs(x1-x0)
        dy = abs(y1-y0)
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
        if dx > dy:
            p = 2 * dy - dx
            incE = 2*dy
            incNE = 2*(dy-dx)
            while x != x1:
                x = x + stepx
                if p < 0:
                    p = p + incE
                else:
                    y = y + stepy
                    p = p + incNE
                self.draw_point(x, y, color=color)
        else:
            p = 2 * dy - dx
            incE = 2*dy
            incNE = 2*(dy-dx)
            while y != y1:
                y = y + stepy
                if p < 0:
                    p = p + incE
                else:
                    x = x + stepx
                    p = p + incNE
                self.draw_point(x, y, color=color)


def drawsquare():
    canvas = BresenhamCanvas(window, width=500, height=700)
    canvas.pack(side=LEFT)
    canvas.draw_line(100, 100, 200, 100, color="blue")
    canvas.draw_line(100, 100, 200, 200, color="blue")
    canvas.draw_line(200, 100, 200, 200, color="blue")
    canvas.draw_line(200, 100, 200, 100, color="blue")


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
