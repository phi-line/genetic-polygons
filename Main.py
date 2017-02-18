#!/usr/bin/env python

import math
import tkinter as tk
from Graphic import GUI
from GA import GA
from random import *

def main():
   '''
   test code for genetic algo
   :return:
   '''

   gui = GUI(tk.Tk())

   seed()
   ga = GA()

   p = ga.pop(50)
   p = ga.selection(p)
   new_gen = ga.propagate_gen(p)
   for i in new_gen:
      # print(i)
      pass
   count = 0
   exptime = 10000
   while (GA.getFitness(new_gen) > 0.001) and count <= exptime:
      new_gen = ga.propagate_gen(p)
      count += 1
      #if (count % (exptime / 10) == 0):
         #print(new_gen[0])
      gui.display_individual(GA.convertPolygon(ga.best_polygon))
         #print("\n GENERATION " + str(count))

main()
