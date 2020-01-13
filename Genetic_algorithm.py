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

    def calc_fitness_population(self, population, k, N):
        length = len(population)
        for i in range(length):
            population[i].calculate_fitness(k, N)
        


    def single_point_crossover(self, ):
        if(self.mutation_probability < np.random.uniform(0.0, 1.0)):
            point = np.random.randint(0,len(self.population[0].flights))
            print(point)
            randoms = random.sample((0,len(self.parents)-1), 2)
            self.parents[randoms[0]].flights[point:], self.parents[randoms[1]].flights[point:] = \
                 self.parents[randoms[1]].flights[point:], self.parents[randoms[0]].flights[point:]
            flight_queue = [self.parents[randoms[i]].get_queue() for i in range(2)]
            while(len(self.parents[randoms[0]].get_queue()) != len(set(self.parents[randoms[0]].get_queue()))):
                seen = [[] for i in range(2)]
                indexes = [[] for i in range(2)]
                for value, value2 in zip(flight_queue[0][point:], flight_queue[1][point:]):
                   seen[0].append(value)
                   seen[1].append(value2)
                for i, [value, value2] in enumerate(zip(flight_queue[0][0:point],flight_queue[1][0:point])):
                    if value in seen[0]:
                        indexes[0].append(i)
                    if value2 in seen[1]:
                        indexes[1].append(i)
                for i,value in enumerate(flight_queue[0][0:point]):
                    if value in seen[0]:
                        second_point = [random.choice(indexes[i]) for i in range(2)]
                        indexes[0].remove(second_point[0])
                        indexes[1].remove(second_point[1])
                        self.parents[randoms[0]].flights[second_point[0]], self.parents[randoms[1]].flights[second_point[1]] = \
                            self.parents[randoms[1]].flights[second_point[1]], self.parents[randoms[0]].flights[second_point[0]]

    

    def calc_population_fitness(self, population):
        return(sum(individual.fitness for individual in population))


    def calc_selection_probability(self, individual, population):
        return(individual.fitness/self.calc_population_fitness(population))

    def calc_selection_probability_population(self,population):
        length = len(population)
        probabilities = prepare(length)
        for i in range(length):
            probabilities[i] = self.calc_selection_probability(population[i], population)
        return probabilities


    def selection(self, population, lambda_parameter):
        probabilities = self.calc_selection_probability_population(population)
        #end_probabilities = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
        end_population = prepare(lambda_parameter)
        length = len(population)
        for i in range(lambda_parameter):
            rand_number = np.random.uniform(0.0, 1.0)
            for j in range(length):
                if rand_number <= max(probabilities):
                    index = probabilities.index(max(probabilities))
                    end_population[i] = population[index]
                    break
        return end_population



    def sum_fitness_collection(self, collection):
        f_sum = 0
        for i in range(len(collection)):
            f_sum += collection[i].fitness
        return f_sum

    def calc_selection_probability(self, individual, collection):
        return(individual.fitness/self.sum_fitness_collection(collection))

    


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
