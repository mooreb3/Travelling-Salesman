# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import numpy as np
import matplotlib.pyplot as plt
import numpy.random as random

import csv
import smopy

#smopy tile server and basic options
smopy.TILE_SERVER = "http://tile.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png"
smopy.TILE_SIZE = 512

worldmap = smopy.Map((0, -120, 65, 120), z=2)
x=[]

class SalesmanAnneal:
    '''Solves the TSM problem using a simulated annealing approach'''
    
    def __init__(self, lats, lons, cities, basemap, T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
        '''initialise the solver, loads city coordinates/names from arguments '''
        self.cities = cities
        self.lats=lats
        self.lons=lons
        self.N = len(cities)
        self.basemap =basemap
        
        self.initial_route = np.random.permutation(np.arange(self.N))
        self.currentgrid=np.copy(self.initial_route)
        self.bestgrid=np.copy(self.initial_route)
        self.fitnesslist=[]
        self.cur_fitness = self.fitness(self.currentgrid)
        self.initial_fitness = self.cur_fitness
        self.best_fitness = self.cur_fitness
        self.fitness_list = [self.cur_fitness]
        
        self.T = 1.0E6 if T == -1 else T
        self.alpha = 0.9994 if alpha == -1 else alpha
        self.stopping_temperature = 0.00001 if stopping_T == -1 else stopping_T
        self.stopping_iter = 30000 if stopping_iter == -1 else stopping_iter
        self.iteration = 1
        
    def fitness(self, route):
        H=0
        c=0
        '''returns the "fitness", i.e. total RETURN path length.'''
        for i in range(self.N):
            for j in range(self.N):
                if j%self.N-i%self.N==1:
                    c=1
                    H += c*self.gcd(route[i],route[j])
        return H
                
    
    
    def anneal(self):
        '''simulated annealing to find solution'''
        self.currentroute=self.initial_route
        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter:
            bi,bj=random.randint(0,self.N),random.randint(0,self.N)
            candidate = np.copy(self.currentgrid)
            candidate[bi],candidate[bj]=candidate[bj],candidate[bi]
            self.accept(candidate)
            self.T *= self.alpha
            self.iteration += 1
            
            # add current fitness to list
            self.fitness_list.append(self.cur_fitness)
        self.print_route(self.bestgrid)
        x=self.fitness_list
        plt.figure(3)
        plt.xlabel("iterations")
        plt.ylabel("total distance")
        plt.plot(x)
        plt.show()
        
            
    
    def accept(self, candidate):
        '''sets the acceptance rules for a new candidate'''
        candidate_fitness = self.fitness(candidate)
        
        # probability 1 for a lower energy candidate
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness = candidate_fitness
            self.currentgrid = candidate
            
            #is the new candidate the best so far?
            if candidate_fitness < self.best_fitness:
                self.best_fitness = candidate_fitness
                self.bestgrid = candidate
                
        # otherwise accept with a probability given by the boltzmann-like term
        else:
            if np.random.random() < np.exp( - abs( candidate_fitness -self.cur_fitness) / self.T):
                self.cur_fitness = candidate_fitness
                self.currentgrid = candidate
                
                
    def print_route(self, route):
        '''Outputs a pretty map showing a particular route'''
        
        #base map to print our route on
        fig, ax = plt.subplots(figsize=(8, 5))
        ax = plt.subplot(111)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        ax.set_xlim(0, self.basemap.w)
        ax.set_ylim(self.basemap.h, 0)
        ax.axis('off')
        plt.tight_layout()
        ax.imshow(self.basemap.img)
        
        #cities
        px, py = [], []
        for i in range(self.N):
            plotx, ploty = self.basemap.to_pixels(self.lats[i], 
                                                 self.lons[i])
            px.append(plotx)
            py.append(ploty)
            
        
        ax.plot(px, py, 'or')
        
        #include labels
        [ax.annotate(self.cities[i], xy=(px[i], py[i]), 
                     xytext=(px[i]+1, py[i]), color='k', size=8) 
         for i in range(0, self.N)]
        gcd_trip = [ self.gcd_path(route[i-1], route[i], ppl) 
                    for i in range(1, self.N) 
                   ] + [self.gcd_path(route[self.N-1], route[0], ppl)]
        
        px1, py1 = [], []
        for leg_lat, leg_lon in gcd_trip:
            for pt in np.arange(len(leg_lat)):
                plotx, ploty = self.basemap.to_pixels(leg_lat[pt], 
                                                      leg_lon[pt])
                px1.append(plotx)
                py1.append(ploty)
                
                
        ax.plot(px1, py1, 'or', ms=0.3)
        #plt.xlim(480,500)
        #plt.ylim(340,320)
        
        return fig, ax
        
               
    #other methods (e.g. GCD between two points, path route....)
    # The length of the shortest path between a and b
    def gcd(self, a, b):
        lat1 = np.radians(self.lats[a])
        lat2 = np.radians(self.lats[b])
        lon1 = np.radians(self.lons[a])
        lon2 = np.radians(self.lons[b])

        dlon = lon2 - lon1 
        dlat = lat2 - lat1 

        hav = (np.sin(dlat/2))**2 + np.cos(lat1) * np.cos(lat2) * (np.sin(dlon/2))**2 
        c = 2 * np.arctan2( np.sqrt(hav), np.sqrt(1-hav) ) 
        return 6371* c 


# A function that returns "num" points on the shortest path between a and b
    def gcd_path(self, a, b, num):
        lat1 = np.radians(self.lats[a])
        lat2 = np.radians(self.lats[b])
        lon1 = np.radians(self.lons[a])
        lon2 = np.radians(self.lons[b])

        d=self.gcd(a, b)
        f= np.linspace(0, 1, num)

        delta = d / 6371
        alpha = np.sin((1-f)*delta) / np.sin(delta)
        beta = np.sin(f*delta) / np.sin(delta)

        x = alpha * np.cos(lat1) * np.cos(lon1) + beta * np.cos(lat2) * np.cos(lon2)
        y = alpha * np.cos(lat1) * np.sin(lon1) + beta * np.cos(lat2) * np.sin(lon2)
        z = alpha * np.sin(lat1) + beta * np.sin(lat2)

        newlats = (np.arctan2(z, np.sqrt(x**2 + y**2)))
        newlons = (np.arctan2(y, x))
        return np.degrees(newlats), (np.degrees(newlons) +540)%360 -180

## Full lists of cities
full_names, full_lats, full_lons, country = [],[],[],[]
path_names,path_lats,path_lons=[],[],[]

# Open CSV file, scan line-by-line and populate lists
#path = r'C:\Users\mooreb3\Downloads\simplemaps-worldcities-basic(1).csv'    
    
with open('simplemaps-worldcities-basic(1).csv', encoding="utf8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    
    #skip the first line, which contains the legend
    next(readCSV)
    
    #add elements row-wise
    for row in readCSV:
        city = row[1]
        lat = float(row[2])
        lon = float(row[3])
        cntry= row[5]
        
        full_names.append(city)
        full_lats.append(lat)
        full_lons.append(lon)
        country.append(cntry)
        
# Exercise 1 -- 30 random cities from the list
path_length = 30
path_indices = np.random.choice ( np.arange( len(full_names) ), path_length, replace=False    )
    
path_names = [full_names[i] for i in path_indices]
path_lats = [full_lats[i] for i in path_indices]
path_lons = [full_lons[i] for i in path_indices]
"""  

random_solution=SalesmanAnneal(path_lats, path_lons, path_names, worldmap)
fig, ax = random_solution.print_route(random_solution.initial_route)

random_solution.anneal() 

                                       
for i in range(len(full_names)):
    if country[i]=='Ireland':
        path_names.append(full_names[i])
        path_lats.append(full_lats[i])
        path_lons.append(full_lons[i])

random_solution=SalesmanAnneal(path_lats, path_lons, path_names, worldmap)
fig, ax = random_solution.print_route(random_solution.initial_route)

random_solution.anneal()
"""

# Lists which we want to fill
top_lats, top_lons, citynames, populations=[], [], [], []
# Open CSV file, scan line-by-line and populate lists
with open('simplemaps-worldcities-basic(1).csv', encoding="utf8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    
    #skip the first line, which contains the legend
    next(readCSV)
    
    #add elements row-wise
    for row in readCSV:
        city = row[1]
        pop = int(float((row[4])))    # rounding of populations with .5s)
        country = row[5]
        lat = float(row[2])
        lon = float(row[3])
        if(pop>=6879087):
            citynames.append(city)
            populations.append(pop)
            top_lats.append(lat)
            top_lons.append(lon)
        
sorting = np.argsort(populations)[::-1]
citysort, popsort  = np.array(citynames)[sorting], np.array(populations)[sorting]  

top_lats, top_lons = np.array(top_lats)[sorting],  np.array(top_lons)[sorting]

for city, pop in zip(citysort, popsort):
    print ('%-18s %8i' % (city, pop) )

path_length = 25
random_solution=SalesmanAnneal(top_lats, top_lons, citysort, worldmap)
fig, ax = random_solution.print_route(random_solution.initial_route)

random_solution.anneal()