import math
import tkinter as tk

class GUI(tk.Canvas):
    '''
        When creating an instance of this class, pass tkinter.Tk() to it like this:
        gui = GUI(tkinter.Tk()
    '''
    def __init__(self,master,*args,**kwargs):
        self.win_x = 800
        self.win_y = 800
        self.canvas_origin_x = (self.win_x / 2)
        self.canvas_origin_y = (self.win_y / 2)
        self.std_rad = 200*2

        tk.Canvas.__init__(self, master=master, width=self.win_x, height=self.win_y, borderwidth=0, highlightthickness=0, bg="white")
        self.pack()

    def display_individual(self,dataset):
        tk.Canvas.delete(self,"all")
        individual=[]
        for coord in dataset[0]:
            individual.append(coord[0])
            individual.append(coord[1])
        self.draw_polygon(individual)
        dataset[1] *= 100
        dataset[1] = round(dataset[1], 2)
        dataset[1] = str(dataset[1]) + "%"
        self.create_text(self.canvas_origin_x, self.canvas_origin_y, fill='black', text=dataset[1])

        tk.Canvas.update_idletasks(self)
        tk.Canvas.update(self)

    def draw_polygon(self, individual):
        fix_A = individual[0] - 90
        A = [individual[0], individual[1]]
        A = self.convert_to_canvas_coords(A, fix_A)

        B = [individual[2], individual[3]]
        B = self.convert_to_canvas_coords(B, fix_A)

        C = [individual[4], individual[5]]
        C = self.convert_to_canvas_coords(C, fix_A)

        converted_coords = [A[0], A[1], B[0], B[1], C[0], C[1]]

        self.create_circle(self.canvas_origin_x, self.canvas_origin_y, self.std_rad, fill="white", outline="#000",width=2)
        self.create_polygon(converted_coords, outline='red', fill='white', width=2)

        tk.Canvas.update_idletasks(self)
        tk.Canvas.update(self)

    def convert_to_canvas_coords(self, coord, fix_A):
        coord[0] -= fix_A
        coord[0] = (coord[0] * 2 * math.pi) / 360

        cart_x = coord[1] * math.cos(coord[0])
        cart_y = coord[1] * math.sin(coord[0])

        pixel_x = self.canvas_origin_x + (cart_x * self.std_rad)
        pixel_y = self.canvas_origin_y - (cart_y * self.std_rad)

        coord[0] = pixel_x
        coord[1] = pixel_y

        return coord

    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

'''
polygon = GUI(tk.Tk())

def draw(scale):
    r1 = 0
    r2 = scale
    r3 = scale + scale
    TEST_individual = [[[r1, 1], [r2, 1], [r3, 1]], scale]

    polygon.display_individual(TEST_individual)

derp = 1
while derp < 1800:
    draw(derp)
    derp += 1

'''
