import Individual
import random
import copy
import numpy as np
from os import strerror
import pandas as pd
from scipy.stats import rankdata
from collections import Counter 
class Genetic_algorithm:

    def __init__(self, approach_data = [], departure_data = [], \
         crossover_probability = 0, mutation_probability = 0, generation_gap = 0, \
             elimination_rate = 0, alfa = 0, population_size = 0, error = 0, k = 0, \
                 vk_min = 0, vk_max = 0, delta_t = 0, runways = 0):
        self.approach_data = approach_data
        self.departure_data = departure_data
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.generation_gap = generation_gap
        self.elimination_rate = elimination_rate
        self.alfa = alfa
        self.population_size = population_size
        self.error = error
        self.k = k
        self.vk_min = vk_min
        self.vk_max = vk_max
        self.delta_t = delta_t
        self.runways = runways
        self.population = []
        self.parents = []
        self.ranking = {}
        self.generation_number = 0
        
    
    def read_data(self, file_name):
        try:    
            data = pd.read_table(file_name)
        except IOError as exc:
            print("Error occured ", strerror(exc.errno))
            exit(exc.errno)
        return data

    def assign_initial_data(self, approach_name, departure_name):
        self.approach_data  = self.read_data(approach_name)
        self.departure_data = self.read_data(departure_name)

    def marriage(self, ro):
        self.parents = prepare(ro)
        selected_individuals = np.random.permutation(len(self.population))
        for i in range(ro):
            self.parents[i] = self.population[selected_individuals[i]]
        return self.parents



    def initialize_population(self,approach_name, departure_name):
        self.approach_data = self.read_data(approach_name)
        self.departure_data = self.read_data(departure_name)
        self.population = prepare(self.population_size)
        for i in range(self.population_size):
            individual = Individual.Individual()
            individual.init_all_flights(self.approach_data, self.departure_data)
            a = individual.flights
            a = random.sample(a,len(a))
            individual.flights = a
            self.population[i] = individual
    
    def initialize_parents(self, parents_size):
        self.parents = prepare(parents_size)


    def get_runway_throughput(self, collection):
        size = len(collection)
        values = prepare(size)
        for i in range(size):
            values[i] = collection[i].runway_throughput
        return values
    
    def get_robustness(self, collection):
        size = len(collection)
        values = prepare(size)
        for i in range(size):
            values[i] = collection[i].robustness
        return values

    def get_flight_losses(self,collection):
        size = len(collection)
        values = prepare(size)
        for i in range(size):
            values[i] = collection[i].flight_losses
        return values


    def rank_objectives(self, objective_functions, collection):
        ranks = []
        ranks_dict = {}
        ranks.append(self.get_runway_throughput(collection))
        ranks.append(self.get_flight_losses(collection))
        ranks.append(self.get_robustness(collection))
        for i in range(len(ranks)):
            ranks[i] = rank(ranks[i])
        for i, value in  enumerate(objective_functions):
            ranks_dict[value] = ranks[i]
        return ranks_dict

    def assign_rankings(self, objective_functions, collection):
        ranking = self.rank_objectives(objective_functions, collection)
        size = len(collection)
        for i in range(size):
            for j in ranking:
                collection[i].individual_ranking[j] = ranking.get(j)[i]


    def call_all_objectives_population(self,):
        for i in range(self.population_size):
            self.population[i].calc_flight_losses(self.delta_t)
            self.population[i].calc_runway_throughput()
            self.population[i].calc_robustness(self.delta_t)

    def call_all_objectives_individual(self, index, population):
        population[index].calc_flight_losses(self.delta_t)
        population[index].calc_runway_throughput()
        population[index].calc_robustness(self.delta_t)

    def calc_fitness(self, index, population):
        pass

    def single_crossover_mutation(self, ):
        if(self.mutation_probability < np.random.uniform(0.0, 1.0)):
            point = np.random.randint(0,len(self.population[0].flights))
            randoms = random.sample((0,len(self.parents)), 2)
            self.parents[randoms[0]].flights[point:], self.parents[randoms[1]].flights[point:] = \
                 self.parents[randoms[1]].flights[point:], self.parents[randoms[0]].flights[point:]
            flight_queue = self.parents[randoms[0]].get_queue()
            #flight_queue = flight_queue[0:point]
            while(len(self.parents[randoms[0]].get_queue()) != len(set(self.parents[randoms[0]].get_queue()))):
                seen = []
                for value in (flight_queue):
                    if value not in seen:
                        seen.append(value)

                for i,value in enumerate(flight_queue[0:point]):
                    if value in seen:
                        while(value in seen):
                            second_point = np.random.randint(0,len(flight_queue))
                            sequence_number = self.parents[randoms[1]].flights[second_point].sequence_number
                            if(sequence_number not in seen):
                                seen[i] = sequence_number
                                self.parents[randoms[0]].flights[i], self.parents[randoms[1]].flights[second_point] = \
                                    self.parents[randoms[1]].flights[second_point], self.parents[randoms[0]].flights[i]
                            else:
                                continue

    


    def terminal_condition(self,):
        result = False
        if self.generation_number >= self.error:
            result = True
        return result

                        
                

        
        
def prepare(n):
    population = [0 for i in range(n)]
    return population

def rank(vec):
    """
    
    :param vec: Rating
    :return: Ranking
    """
    return rankdata(vec, method = 'min').astype(int) 
