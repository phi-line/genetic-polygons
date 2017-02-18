import math
from random import randint
import tkinter as tk
root = tk.Tk()

# TEST DATA
r1 = randint(0,358)
r2 = randint(r1,359)
r3 = randint(r2,360)
TEST_individual = [r1,1,r2,1,r3,1]
#TEST_individual = [45,1,105,1,215,1]

# GLOBAL VARIABLES
win_x = 600
win_y = 600

canvas_origin_x = (win_x / 2)
canvas_origin_y = (win_y / 2)

std_rad = 200

canvas = tk.Canvas(root, width=win_x, height=win_y, borderwidth=0, highlightthickness=0, bg="white")

class GUI(tk.Canvas):
    '''inherits Canvas class (all Canvas methodes, attributes will be accessible)
       You can add your customized methods here.
    '''
    def __init__(self,master,*args,**kwargs):
        tk.Canvas.__init__(self, master=master, width=win_x, height=win_y, borderwidth=0, highlightthickness=0, bg="white")

    def draw_polygon(self, individual):
        A = [individual[0],individual[1]]
        A = self.convert_to_canvas_coords(A)

        B = [individual[2], individual[3]]
        B = self.convert_to_canvas_coords(B)

        C = [individual[4], individual[5]]
        C = self.convert_to_canvas_coords(C)

        converted_coords=[A[0],A[1],B[0],B[1],C[0],C[1]]

        self.create_polygon(converted_coords,outline='red',fill='white',width=2)

    def convert_to_canvas_coords(self,coord):
        coord[0] = (coord[0]*2*math.pi)/360

        cart_x = coord[1]*math.cos(coord[0])
        cart_y = coord[1]*math.sin(coord[0])

        pixel_x = canvas_origin_x + (cart_x*std_rad)
        pixel_y = canvas_origin_y - (cart_y * std_rad)

        coord[0] = pixel_x
        coord[1] = pixel_y

        return coord

    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

polygon = GUI(root)
#polygon.create_polygon([150,75,225,0,300,75,225,150],outline='gray',fill='gray', width=2)
polygon.create_circle(canvas_origin_x,canvas_origin_y,std_rad,fill="white",outline="#000", width=2)
polygon.draw_polygon(TEST_individual)

polygon.pack()
root.mainloop()
