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


if __name__ == "__main__":
    CANVAS_SIZE = 600
    root = Tk()
    canvas = BresenhamCanvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE)
    canvas.pack()
    #canvas.draw_line(100, 100, 200, 100, color="blue")
    #canvas.draw_line(200, 100, 300, 350, color="blue")
    canvas.draw_line(200, 100, 300, 30, color="blue")
    root.mainloop()
