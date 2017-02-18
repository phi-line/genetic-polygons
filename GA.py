#!/usr/bin/env python

from random import randint, randrange, sample
from copy import deepcopy
from operator import itemgetter

class GA:
   def __init__(self):
      self.RADIUS = 1
      self.gen_count = 1
      #self.current_gen = []
      self.best_polygon = []
      self.best_fitness = 0

   def polygon(self):
      '''
      returns a list with a series of three theta radius pairs
      :return: list[ [0,R], [0,R], [0,R]
      '''

      rand_angles = [randint(0, 360), randint(0, 360), randint(0, 360)]
      while(rand_angles[0] == rand_angles[1] or
            rand_angles[0] == rand_angles[2] or
            rand_angles[1] == rand_angles[2]):
         rand_angles = [randint(0, 360), randint(0, 360), randint(0, 360)]

      rand_angles.sort()

      vertz = []
      for i in range(0, len(rand_angles)):
         vertz.append([rand_angles[i],self.RADIUS])
      return vertz

   def pop(self, size):
      '''
      returns a set of N polygons
      :param size: integer
      :return: list[n polygons...]
      '''
      return [self.polygon() for x in range(size)]

   @staticmethod
   def fitness(polygon):
      '''
      returns a fitness for an polygon
      :param polygon:
      :return:
      '''
      '''
      thetaA = polygon[0][0]+(360-polygon[2][0])
      thetaB = polygon[1][0] - polygon[0][0]
      thetaC = polygon[2][0] - polygon[1][0]
      '''

      thetaA = 120 - abs(polygon[0][0] - polygon[2][0])
      thetaB = 120 - abs(polygon[1][0] - polygon[0][0])
      thetaC = 120 - abs(polygon[2][0] - polygon[1][0])

      sum = thetaA + thetaB + thetaC
      return round(abs(sum/360.0), 3)


   def selection(self, pop):
      '''
      appends a fitness value for each polygon
      :return:
      '''
      numElem = len(pop)
      for i in range(0, numElem):
         fitVal = self.fitness(pop[i])
         pop[i] = [pop[i][0], pop[i][1], pop[i][2], fitVal]

      '''
      print("selection:pop:")
      for p in pop:
         print(p)
      print("End---")
      '''
      return sorted(pop, key = itemgetter(3))

   def propagate_gen(self, pop):
      '''
      preforms selection on current gen.
      keeps best and splices the rest
      :param pop:
      :return:
      '''
      new_pop = deepcopy(pop)
      for i in range(1, len(pop)):
         new_pop[i] = self.splice_polygon(pop[i-1], pop[i])
         new_pop = GA.sortByFitness(new_pop)
      return new_pop

   @staticmethod
   def splice_polygon(polygonA, polygonB):
      new_polygon = deepcopy(polygonA)
      pairs_len = len(new_polygon) - 1
      setA = set()
      for i in range(0, pairs_len):
         setA.add(i)
      index = sample(setA, pairs_len)
      # needs to be dynamic
      new_polygon[0][0] = polygonA[index[0]][0]
      new_polygon[1][0] = polygonA[index[1]][0]
      new_polygon[2][0] = polygonB[index[2]][0]
      pairs = []
      for i in range(0, pairs_len):
         pairs.append(new_polygon[i])
      pairs = sorted(pairs, key = itemgetter(0))
      for i in range(0, pairs_len):
         new_polygon[i] = pairs[i]
      new_polygon[pairs_len] = GA.fitness(new_polygon)
      return new_polygon

   @staticmethod
   def getKey(item):
      return item[0]

   @staticmethod
   def getFitness(gen):
      return gen[0][3]

   @staticmethod
   def sortByFitness(gen):
      return sorted(gen, key = itemgetter(3))

   def mutation(self):
      pass

def main():
   '''
   test code for genetic algo
   :return:
   '''
   ga = GA()

   p = ga.pop(10)
   for i in p:
      print(i)

   print("\n")

   p = ga.selection(p)
   for i in p:
      print(i)

   print("\n")

   new_gen = ga.propagate_gen(p)
   for i in new_gen:
      print(i)
   count = 0
   while GA.getFitness(new_gen) > 0.001:
      new_gen = ga.propagate_gen(p)
      print(new_gen[0])
      count += 1
      print("\n GENERATION " + str(count))



if __name__ == '__main__':
   main()
