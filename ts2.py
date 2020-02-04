# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 14:46:28 2019

@author: benji
"""

import numpy as np
import matplotlib.pyplot as plt
import numpy.random as random
import csv
import smopy
import panda

lats,lons,cities = [],[],[]

with open('csv(1).ipynb') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if linecount ==0:
                    line_count += 1
                else:
                    cities.append(row[0])
                    linecount +=1

with open('csv(1).ipynb') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if linecount ==0:
                    line_count += 1
                else:
                    cities.append(row[0])
                    linecount +=1


class SalesmanAnneal:
    '''Solves the TSM problem using a simulated annealing approach'''
    
    def __init__(self, lats, lons, cities, basemap,T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1 ):
        '''initialise the solver, loads city coordinates/names from arguments '''
       
        self.lats=
        self.lons=
        self.cities=np.random(csv_list(1).ipynb)
        self.basemap=np.loadtxt(simplemaps-worldcities-basic.csv)

        
        
        self.changeable = self.inputgrid == 0
        self.poss = np.arange(1, dim*dim+1, 1)
        self.currentgrid = np.copy(self.inputgrid)
        
        # fill in empty sites of currentgrid with integers
        self.create_first_guess()
        self.bestgrid = np.copy(self.currentgrid)
        
        #'fitness' or energy of solutions
        self.cur_fitness = self.fitness(self.currentgrid)
        self.initial_fitness = self.cur_fitness
        self.best_fitness = self.cur_fitness
        self.fitness_list = [self.cur_fitness]
        
        #annealing parameters (use defaults if not set...)
        self.T = 1.0E6 if T == -1 else T
        self.alpha = 0.999 if alpha == -1 else alpha
        self.stopping_temperature = 0.0001 if stopping_T == -1 else stopping_T
        self.stopping_iter = 100000 if stopping_iter == -1 else stopping_iter
        self.iteration = 1
    
    
    def create_first_guess(self):
        '''Random sequence of cities'''
         #loop over the sub-blocks
        for bi in range(self.dim):
            for bj in range(self.dim):
                
                # list of possible entries...
                block_poss = self.poss[:]
                
                # creates a new array to store the current block
                block_elems=self.currentgrid[bi*self.dim:(bi+1)*self.dim, bj*self.dim:(bj+1)*self.dim]
                
                # shuffled list of numbers missing from this block
                tobeplaced = np.setdiff1d(block_poss, block_elems)
                random.shuffle(tobeplaced)

                # places missing numbers in the "0" sites
                sites = np.where(block_elems == 0)
                block_elems[sites] = tobeplaced
                
                #places the new block into the current grid
                self.currentgrid[bi*self.dim:(bi+1)*self.dim, bj*self.dim:(bj+1)*self.dim] = block_elems.reshape((3,3))
                
                #salesman soln
        """
        Greedy algorithm to get an initial solution (closest-neighbour).
        """
        cur_node = random.choice(self.nodes)  # start from a random node
        solution = [cur_node]

        free_nodes = set(self.nodes)
        free_nodes.remove(cur_node)
        while free_nodes:
            next_node = min(free_nodes, key=lambda x: self.dist(cur_node, x))  # nearest neighbour
            free_nodes.remove(next_node)
            solution.append(next_node)
            cur_node = next_node

        cur_fit = self.fitness(solution)
        if cur_fit < self.best_fitness:  # If best found so far, update best fitness
            self.best_fitness = cur_fit
            self.best_solution = solution
        self.fitness_list.append(cur_fit)
        return solution, cur_fit
    
    
    def fitness(self, grid):
        '''returns the "fitness", i.e. total RETURN path length.'''
    
    
    def anneal(self):
        '''simulated annealing to find solution'''
        
        # loop until stopping conditions are met
        #while  ?????:
            
            # generate a new candidate solution
            
            # accept the new candidate?
            
            # update conditions
            
            
    
    def accept(self, candidate):
        '''sets the acceptance rules for a new candidate'''
                
                
    def print_grid(self, route):
        '''Outputs a pretty map showing a particular route'''
               
    #other methods (e.g. GCD between two points, path route....)
    