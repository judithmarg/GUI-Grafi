import cv2 as cv
import numpy as np


def bresenham(x0, y0, x1, y1):
    blank = np.zeros((700, 700, 3), dtype="uint8")
    dx = abs(x1-x0)
    dy = abs(y1-y0)
    p = 2 * dy - dx
    incE = 2*dy
    incNE = 2*(dy-dx)
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
    for i in range(start, end):
        blank[x, y] = (51, 222, 255)
        print('x =', x, 'y =', y)
        x = x+1 if x < x1 else x - 1
        if p < 0:
            p += incE
        else:
            y = y+1 if y < y1 else y - 1
            p += incNE

    cv.imshow("Yellow", blank)
    cv.waitKey(0)
