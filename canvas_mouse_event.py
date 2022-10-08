import tkinter as tk


class Aplication:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=600, height=400, bg="black")
        self.canvas.grid(column=0, row=0)
        self.canvas.bind("<Motion>", self.move_mouse)
        self.canvas.bind("<Button-1>", self.press_button_mouse)
        self.window.mainloop()

    def move_mouse(self, event):
        self.window.title(str(event.x)+'-' + str(event.y))

    def press_button_mouse(self, event):
        self.canvas.create_oval(event.x-5, event.y-5,
                                event.x+5, event.y+5, fill="red")


aplication1 = Aplication()
