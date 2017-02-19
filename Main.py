#!/usr/bin/env python

import math
import tkinter as tk
from Graphic import GUI
from GA import GA
from random import *
import time

def main():
   '''
   test code for genetic algo
   :return:
   '''

   gui = GUI(tk.Tk())

   seed()
   ga = GA()

   p = ga.pop(20)
   p = ga.selection(p)
   p = ga.propagate_gen(p)

   count = 0
   exptime = 10000
   while (count <= exptime):
      if(GA.getFitness(p) > 0.025):
         p = ga.selection(p)
         p = ga.propagate_gen(p)
         count += 1
         #if (count % (exptime / 10) == 0):
         #print(new_gen[0])
         gui.display_individual(GA.convertPolygon(ga.best_polygon))
         time.sleep(0.03)
         #print("\n GENERATION " + str(count))

main()
