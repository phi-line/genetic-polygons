#!/usr/bin/env python

from random import *
from copy import deepcopy
from operator import itemgetter
from math import *

class GA:
   RADIUS = 1
   DEG_SIG = 5
   FIT_SIG = 5
   DO_MUTATE = True
   MUTATION_RATE = .2  # rate in which pop will be mutated
   MUTATION_AMT = 10.0  # +/- random range for mutation
   BAD_SAMPLE_RATE = 0

   def __init__(self):
      self.gen_count = 1
      self.current_gen = []
      self.best_polygon = []
      self.best_fitness = 0

   @staticmethod
   def convertFitPolygon(simplyPolygon):
      return [ [simplyPolygon[0], GA.RADIUS],
               [simplyPolygon[1], GA.RADIUS],
               [simplyPolygon[2], GA.RADIUS] ]

   def polygon(self):
      '''
      returns a list with a series of three theta radius pairs
      :return: list[ [0,R], [0,R], [0,R]
      '''
      cir = 360.0
      rand_angles = GA.gen_pairs(cir)
      formattedRandAngles = GA.convertFitPolygon(rand_angles)
      while(rand_angles[0] == rand_angles[1] or
            rand_angles[0] == rand_angles[2] or
            rand_angles[1] == rand_angles[2] or
            self.fitness(formattedRandAngles) < self.BAD_SAMPLE_RATE):
         rand_angles = GA.gen_pairs(cir)
         formattedRandAngles = GA.convertFitPolygon(rand_angles)

      vertz = []
      for i in range(0, len(rand_angles)):
         vertz.append([rand_angles[i],self.RADIUS])
      return vertz

   @staticmethod
   def gen_pairs(angle):
      pairs = [uniform(0, angle), uniform(0, angle), uniform(0, angle)]
      for i in range(0, len(pairs)):
         pairs[i] = round(pairs[i],GA.DEG_SIG)
      pairs.sort()
      return pairs

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
      poly = deepcopy(polygon)

      thetaA = poly[0][0]+(360-poly[2][0])
      thetaB = poly[1][0] - poly[0][0]
      thetaC = poly[2][0] - poly[1][0]

      thetaA = abs(thetaA - 120)
      thetaB = abs(thetaB - 120)
      thetaC = abs(thetaC - 120)
      angle_sum = thetaA + thetaB + thetaC
      angle_sum = angle_sum/360.0

      coordA = GA.convert_to_canvas_coords(poly[0])
      coordB = GA.convert_to_canvas_coords(poly[1])
      coordC = GA.convert_to_canvas_coords(poly[2])

      AB = GA.mag(coordA[0], coordB[0], coordA[1], coordB[1])
      BC = GA.mag(coordB[0], coordC[0], coordB[1], coordC[1])
      CA = GA.mag(coordC[0], coordA[0], coordC[1], coordA[1])
      side_list = sorted([AB, BC, CA], reverse=True)
      side_avg = 1 - (side_list[1] + side_list[2]) / (2 * side_list[0])

      total_sum =round(side_avg * 0.0 +
                        angle_sum * 1.0, GA.FIT_SIG)

      #return round(angle_sum, GA.FIT_SIG)
      return total_sum

   @staticmethod
   def convert_to_canvas_coords(coord):
      coord[0] = (coord[0] * 2 * pi) / 360

      cart_x = coord[1] * cos(coord[0])
      cart_y = coord[1] * sin(coord[0])
      return [cart_x, cart_y]

   @staticmethod
   def mag(x1, x2, y1, y2):
      return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

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
      # for i in range(1, len(pop)):
      #    new_pop[i] = self.splice_polygon(pop[i-1], pop[i])
      #    new_pop = GA.sortByFitness(new_pop)
      pop_set = set()
      for i in range(0, len(pop)):
         pop_set.add(i)
      index = sample(pop_set, len(pop)) #gen unique numbers n - len(pop)
      for i in range(1, len(pop)):
         new_pop[i] = self.splice_polygon(pop[index[i-1]], pop[index[i]])

      if self.DO_MUTATE:
         self.mutation(new_pop)
      self.current_gen = new_pop
      self.best_polygon = new_pop[0]
      self.best_fitness = new_pop[0][len(new_pop[0]) - 1]
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
      count = int(len(new_polygon)/2) # 3
      for i in range(0, pairs_len - count):
         new_polygon[i][0] = polygonA[index[i]][0]
      for i in range(0, count):
         new_polygon[i][0] = polygonB[index[i]][0]
      # sorts pairs and recomputes fitness
      GA.sortPairs(new_polygon)
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

   @staticmethod
   def sortPairs(polygon):
      pairs = []
      pairs_len = len(polygon) - 1
      for i in range(0, pairs_len):
         pairs.append(polygon[i])
      pairs = sorted(pairs)
      for i in range(0, pairs_len):
         polygon[i] = pairs[i]
      return polygon

   @staticmethod
   def convertPolygon(polygon):
      return [[polygon[0], polygon[1], polygon[2]], polygon[3]]

   def mutation(self, gen):
      infect_rate = uniform(0,self.MUTATION_RATE)
      for i in range(0, int(infect_rate* len(gen)) ):
         index = randrange(0, len(gen))
         self.infect(gen[index])


   def infect(self, polygon):
      pairs_len = len(polygon) - 1
      for i in range (0, pairs_len):
         index = randrange(0, pairs_len)
         polygon[index][0] += uniform(-self.MUTATION_AMT, self.MUTATION_AMT)
         if polygon[index][0] >= 360:
            polygon[index][0] -= 360
         elif polygon[index][0] < 0:
            polygon[index][0] += 360
      return GA.sortPairs(polygon)

def main():
   '''
   test code for genetic algo
   :return:
   '''
   seed()
   ga = GA()

   p = ga.pop(100)
   for i in p:
      # print(i)
      pass

   print("\n")

   p = ga.selection(p)
   for i in p:
      # print(i)
      pass

   print("\n")

   new_gen = ga.propagate_gen(p)
   for i in new_gen:
      # print(i)
      pass
   count = 0
   exptime = 1000
   while (GA.getFitness(new_gen) > 0.001) and count <= exptime:
      new_gen = ga.propagate_gen(p)
      count += 1
      if(count % (exptime/10) == 0):
         print(new_gen[0])
         print("\n GENERATION " + str(count))



if __name__ == '__main__':
   main()