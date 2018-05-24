#!/usr/bin/env python

from random import *
from copy import deepcopy
from operator import itemgetter
from math import *

class GA:
   RADIUS = 1
   DEG_SIG = 15
   FIT_SIG = 15
   DO_MUTATE = True
   MUTATION_RATE = .1  # rate in which pop will be mutated
   MUTATION_AMT = .2  # +/- random range for mutation
   BAD_SAMPLE_RATE = 0.60
   DIFF_ANGLE = 0.005

   def __init__(self, verts = 3):
      self.gen_count = 1
      self.current_gen = []
      self.best_polygon = []
      self.best_fitness = 0
      self.verts = verts

   @staticmethod
   def convertFitPolygon(simplyPolygon):
      lst = []
      for i in range(0, len(simplyPolygon)):
         lst.append([simplyPolygon[i], GA.RADIUS])
      return lst

   def polygon(self):
      '''
      returns a list with a series of three theta radius pairs
      :return: list[ [0,R], [0,R], [0,R]
      '''
      cir = 360.0
      rand_angles = self.gen_pairs(cir)
      formattedRandAngles = GA.convertFitPolygon(rand_angles)

      diff_bool = False
      num_angles = len(rand_angles)
      for i in range(1, num_angles):
         if abs(rand_angles[0] - rand_angles[i]) <= GA.DIFF_ANGLE:
            diff_bool = True
            break
      if abs(rand_angles[1] - rand_angles[num_angles - 1]) <= GA.DIFF_ANGLE:
         diff_bool = True

      while(diff_bool or self.fitness(formattedRandAngles) < self.BAD_SAMPLE_RATE):
         rand_angles = self.gen_pairs(cir)
         formattedRandAngles = self.convertFitPolygon(rand_angles)

      verts = []
      for i in range(0, len(rand_angles)):
         verts.append([rand_angles[i],self.RADIUS])
      return verts

   def gen_pairs(self, angle):
      pairs = []
      for i in range(0, self.verts):
         pairs.append(uniform(0, angle))
      # pairs = [uniform(0, angle), uniform(0, angle), uniform(0, angle)]
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
   def diffAngle(fAngle, sAngle):
      diff = abs(fAngle - sAngle)
      if(diff > 180):
         return abs(360 - diff)
      return diff

   def fitness(self, polygon):
      '''
      returns a fitness for an polygon
      :param polygon:
      :return:
      '''
      poly = deepcopy(polygon)
      thetaLst = []
      for i in range (0, self.verts):
         j = i - 1
         if j == -1:
            j = self.verts - 1
         thetaLst.append(self.diffAngle(poly[i][0], poly[j][0]))
      angle_sum = 0
      for i in range(len(thetaLst)):
         angle_sum += abs(thetaLst[i] - 360.0/self.verts)
      angle_sum = angle_sum/360.0

      return round(angle_sum, GA.FIT_SIG)

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
         popLen = len(pop[i])
         if popLen == self.verts:
            pop[i].append(fitVal)
         else:
            pop[i][self.verts] = fitVal
         # pop[i] = [pop[i][0], pop[i][1], pop[i][2], fitVal]

      return sorted(pop, key = itemgetter(self.verts))

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

   def splice_polygon(self, polygonA, polygonB):
      new_polygon = deepcopy(polygonA)
      pairs_len = len(new_polygon) - 1
      setA = set()
      for i in range(0, pairs_len):
         setA.add(i)
      index = sample(setA, pairs_len)
      # needs to be dynamic
      count = int(len(new_polygon) / 2)
      for i in range(0, count):
         new_polygon[i][0] = polygonA[index[i]][0]
      for i in range(count, pairs_len):
         new_polygon[i][0] = polygonB[index[i]][0]
      # sorts pairs and recomputes fitness
      self.sortPairs(new_polygon)
      new_polygon[pairs_len] = self.fitness(new_polygon)
      return new_polygon

   @staticmethod
   def getKey(item):
      return item[0]

   @staticmethod
   def getFitness(gen):
      return gen[0][len(gen[0]) - 1]

   def sortByFitness(self, gen):
      return sorted(gen, key = itemgetter(self.verts))

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

   def convertPolygon(self, polygon):
      pairsLst = []
      for i in range(0, self.verts):
         pairsLst.append(polygon[i])
      polyLst = []
      polyLst.append(pairsLst)
      polyLst.append(polygon[self.verts])
      return polyLst
      # return [[polygon[0], polygon[1], polygon[2]], polygon[3]]

   def mutation(self, gen):
      infect_rate = uniform(0,self.MUTATION_RATE)
      for i in range(0, int(infect_rate* len(gen)) ):
         index = randrange(0, len(gen))
         self.infect(gen[index])


   def infect(self, polygon):
      pairs_len = len(polygon) - 1
      for i in range (0, pairs_len):
         index = randrange(0, pairs_len)
         mutate = round(uniform(-self.MUTATION_AMT, self.MUTATION_AMT),GA.DEG_SIG)
         polygon[index][0] += mutate
         if polygon[index][0] >= 360:
            polygon[index][0] -= 360
         elif polygon[index][0] < 0:
            polygon[index][0] += 360
      return GA.sortPairs(polygon)
