#!/usr/bin/env python
import sys
from argparse import ArgumentParser

import math
import tkinter as tk
from graphic import GUI
from GA import GA
from random import *
import time

DELAY = 1
DEMO = True

def runGA(verts, population, demo = False):
   '''
   test code for genetic algo
   :return:
   '''
   # time.sleep(1000)

   gui = GUI(tk.Tk())

   seed()
   ga = GA(verts=verts)

   p = ga.pop(population)
   p = ga.selection(p)
   p = ga.propagate_gen(p)

   t = time.time()

   count = 1
   exptime = 10000
   while (count <= exptime):
      if(ga.best_polygon[len(ga.best_polygon)-1] > .01):
         #print(count)
         p = ga.selection(p)
         p = ga.propagate_gen(p)
         # print(ga.convertPolygon(ga.best_polygon))
         if(DEMO):
            gui.display_individual(ga.convertPolygon(ga.best_polygon), count)
            if count is 1:
                time.sleep(5)
            time.sleep(DELAY / count)
         count += 1
      else:
         if not DEMO:
            break

   return [ (time.time() - t), count, ga.best_fitness]


def main(verts=None, population=None):
   if verts is None:
       verts = 3
   if population is None:
       population = 50

   if(DEMO):
      runGA(verts, population, True)

   else:
      avgTime = 0.0
      avgError = 0.0
      run = 10
      SIG = 15
      for i in range(0, run):
         res = runGA(False)
         timeSpent = res[0] + res[1] * DELAY
         avgTime += timeSpent
         avgError += res[2]*100.0
         print("time spent(s):", round(timeSpent, 5))
         print("error:", round(res[2]*100.0*1000000, SIG), "%*10^-6")
      print("average time(s):", round(avgTime/run, 5))
      print("average error:", round(avgError/run, SIG), "%")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-v", "--verts", dest="verts", nargs='?', const=3, type=int,
                        help="How many vertices should each generation run")
    parser.add_argument("-p", "--population", dest="population", nargs='?', const=50, type=int,
                        help="What population should each generation contain")

    args = vars(parser.parse_args())
    main(verts=args['verts'], population=args['population'])
