#!/usr/bin/env python

from random import randint, random

class GA:
   def __init__(self):
      self.RADIUS = 1
      self.gen_count = 1
      self.current_gen = []
      self.best_polygon = []
      self.best_fitness = 0

   def polygon(self):
      '''
      returns a list with a series of three theta radius pairs
      :return: list[ [0,R], [0,R], [0,R]
      '''

      rand_angles = [randint(0, 359), randint(0, 359), randint(0, 359)]
      while(rand_angles[0] == rand_angles[1] ||
            rand_angles[0] == rand_angles[2] ||
            rand_angles[1] == rand_angles[2]):
         rand_angles = [randint(0, 359), randint(0, 359), randint(0, 359)]

      rand_angles.sort()

      vertz = []
      for i in len(rand_angles):
         vertz.append([rand_angles[i],self.RADIUS])
      return vertz

   def pop(self, size):
      '''
      returns a set of N polygons
      :param size: integer
      :return: list[n polygons...]
      '''
      return [self.polygon() for x in range(size)]

   def fitness(self, polygon):
      '''
      returns a fitness for an polygon
      :param polygon:
      :return:
      '''
      thetaA = 120-polygon[0][0]
      thetaB = 120-polygon[1][0]
      thetaC = 120-polygon[2][0]
      sum = thetaA + thetaB + thetaC
      return float(sum/360.0)


   def selection(self, pop):
      '''
      appends a fitness value for each polygon
      :return:
      '''
      for i in len(pop):
         fitVal = self.fitness(pop[i])
         pop[i] = [pop[i][0], pop[i][1], pop[i][2], fitVal]
      pop.sort(self, key = fitVal)
      pass

   def propagate_gen(self, pop):
      '''
      preforms selection on current gen.
      keeps best and splices the rest
      :param pop:
      :return:
      '''
      for i in range(1, len(pop)):
         pop[i] = self.splice_polygon(pop[i-1], pop[i])
         pass

   @staticmethod
   def splice_polygon(polygonA, polygonB):
      new_polygon = polygonA
      index = random.sample(randint(0,2), len(polygonA))
      new_polygon[0][0] = polygonA[index[0]][0]
      new_polygon[1][0] = polygonA[index[1]][0]
      new_polygon[2][0] = polygonB[index[2]][0]
      return new_polygon

   def mutation(self):
      pass
