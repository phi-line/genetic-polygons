#!/usr/bin/env python

import math
import tkinter as tk
from Graphic import GUI
from GA import GA
from random import *
import time

DELAY = 0.01
DEMO = True

def runGA(demo = False):
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

   t = time.time()

   count = 0
   exptime = 10000
   while (count <= exptime):
      if(ga.best_polygon[3] > 2.0/100.0):
         p = ga.selection(p)
         p = ga.propagate_gen(p)
         count += 1
         if(demo):
            gui.display_individual(GA.convertPolygon(ga.best_polygon))
            time.sleep(DELAY)
      else:
         if(not demo):
            break

   return [ (time.time() - t), count, ga.best_fitness]


def main():
   if(DEMO):
      runGA(True)

   else:
      avgTime = 0.0
      avgError = 0.0
      run = 10
      for i in range(0, run):
         res = runGA(False)
         timeSpent = res[0] + res[1] * DELAY
         avgTime += timeSpent
         avgError += res[2]*100.0
         print("time spent(s):", round(timeSpent, 2))
         print("error:", round(res[2]*100.0, 2), "%")
      print("average time(s):", round(avgTime/run, 2))
      print("average error:", round(avgError/run, 2), "%")


main()
