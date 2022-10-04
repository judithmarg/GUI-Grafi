from tkinter import *


class BresenhamCanvas(Canvas):
    def draw_point(self, x, y, color="red"):
        self.create_line(x, y, x+1, y+1, fill=color, width=2)

    def draw_line(self, x0, y0, x1, y1, color="red"):
        dx = abs(x1-x0)
        dy = abs(y1-y0)
        p = 2 * dy - dx
        incE = 2*dy
        incNE = 2*(dy-dx)
        if x0 > x1:
            x = x1
            y = y1
            xend = x0
        else:
            x = x0
            y = y0
            xend = x1
        for i in range(x, xend):
            print('x =', x, 'y =', y)
            x = x+1 if x < x1 else x - 1
            if p < 0:
                p += incE
                self.draw_point(x, y, color=color)
            else:
                y = y+1 if y < y1 else y - 1
                p += incNE
                self.draw_point(x, y, color=color)


if __name__ == "__main__":
    CANVAS_SIZE = 600
    root = Tk()
    canvas = BresenhamCanvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE)
    canvas.pack()
    canvas.draw_line(100, 100, 200, 100, color="blue")
    canvas.draw_line(200, 100, 300, 350, color="blue")
    root.mainloop()
