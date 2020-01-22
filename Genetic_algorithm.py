import Individual
import random
from copy import copy
import numpy as np
from os import strerror
import pandas as pd
from scipy.stats import rankdata
from collections import Counter 
from numpy.random import choice

class Genetic_algorithm:

    def __init__(self, approach_data = [], departure_data = [], \
         crossover_probability = 0, mutation_probability = 0, generation_gap = 0, \
             elimination_rate = 0, alfa = 0, population_size = 0, error = 0, k = 0, \
                 vk_min = 0, vk_max = 0, delta_t = 0, runways = 0, time_interval = 0):
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
        self.time_interval = 120
        
    
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
            self.parents[i] = copy(self.population[selected_individuals[i]])
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
            for flight in individual.flights:
                flight.estimated_time = flight.hms_to_s(flight.estimated_time)
                flight.actual_time = flight.hms_to_s(flight.actual_time)
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


    def call_all_objectives_population(self, population):
        for i in range(len(population)):
            population[i].calc_flight_losses(self.delta_t)
            population[i].calc_runway_throughput()
            population[i].calc_robustness(self.delta_t)

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
            randoms = random.sample([i for i in range(len(self.parents)-1)], 2)
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
            return self.parents[randoms[0]]
        else:
            return self.parents[random.randint(0,len(self.parents)-1)]

    

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
            for _ in range(length):
                if rand_number <= max(probabilities):
                    index = probabilities.index(max(probabilities))
                    end_population[i] = population[index]
                    break
        return end_population
    
    def roulette_selection(self, population, lambda_parameter):
        probabilities = self.calc_selection_probability_population(population)
        indexes = choice(len(population), lambda_parameter, p = probabilities)
        return_pop = [copy(population[i]) for i in indexes]
        return return_pop

    def flight_losses_selection(self, population, lambda_parameter):
        return_pop = sorted(population, key = lambda x: x.flight_losses, reverse = False)
        return_pop = return_pop[0:lambda_parameter]
        return return_pop


    def mutation_swap(self, individual):
        indexes = random.sample([i for i in range(len(individual.flights))], 2)
        individual.flights[indexes[0]], individual.flights[indexes[1]] = individual.flights[indexes[1]], individual.flights[indexes[0]]

    # def mutation_shift(self, individual):
    #     max_range = len(individual.flights)
    #     point = random.randint( 1, max_range - 1)
    #     length = random.randint(1, max_range - point+1)
    #     first_gene = random.randint(1, max_range - length+1)
    #     diff = point - (first_gene + length)
    #     if diff == 0:
    #         return
    #     if point - length >= first_gene or point < first_gene:
    #         if diff > 0:
    #             copied = copy(individual.flights[first_gene+1 + length : first_gene+1 + length  + diff])
    #             del individual.flights[first_gene + length + 1 : first_gene + length + diff + 1]
    #             for i in reversed(copied):
    #                 individual.flights.insert(first_gene, i)
    #         elif diff < 0:
    #             diff = abs(point - first_gene)
    #             copied  = copy(individual.flights[point: point+length])
    #             del individual.flights[point: point+length]
    #             for i in reversed(copied):
    #                 individual.flights.insert(point + length + 1, i)
    #     else:
    #         individual.flights[first_gene : first_gene + length], individual.flights[point-length : point] =\
    #              individual.flights[point-length : point], individual.flights[first_gene : first_gene + length]
    
    def mutation_shift(self, individual):
        max_range = len(individual.flights)
        point = random.randint( 0, max_range - 1)
        length = random.randint(1, max_range - point+1)
        first_gene = random.randint(0, max_range - length+1)
        if point == first_gene:
            return
        if point >= first_gene + length:
            diff = point - (first_gene + length) +1
            copied = copy(individual.flights[first_gene+length : first_gene+length+diff])
            del individual.flights[first_gene+length : first_gene+length+diff]
            for flight in reversed(copied):
                individual.flights.insert(first_gene, flight)
        elif point < first_gene:
            diff = abs(first_gene - point)
            copied = copy(individual.flights[point : point + diff])
            del individual.flights[point : point + diff]
            for flight in reversed(copied):
                individual.flights.insert(first_gene + point, flight)
       

    def mutation_scramble(self, individual):
        max_range = len(individual.flights)
        point = random.randrange( 1, max_range-1)
        #print(point)
        length = random.randrange(1, max_range - point+1)
        #print("end)")
        individual.flights[point:point+length] = random.sample(copy(individual.flights[point:point+length]), length)

    def mutation_inversion(self, individual):
        max_range = len(individual.flights)
        point = random.randint( 1, max_range-1)
        length = random.randint(1, max_range - point+1)
        individual.flights[point:point+length] = reversed(individual.flights[point:point+length])

    def calc_actual_time_v2(self, individual):
        for number, flight in enumerate(individual.flights):
            flight.runway = random.randrange(2)
        flag1 = False
        flag2 = False
        for i in individual.flights:
            if i.runway == 0 and flag1 == False:
                i.actual_time = i.estimated_time + self.time_interval
                flag1 = True
            elif i.runway == 1 and flag2 == False:
                i.actual_time = i.estimated_time + self.time_interval
                flag2 = True
            if flag1 and flag2:
                break
        for number, flight in enumerate(individual.flights):
            runway = flight.runway
            lst = [idx for idx, flight in enumerate(individual.flights[0:number]) if flight.runway == runway]
            if len(lst)>0:
                index = max(lst)
                flight.actual_time = individual.flights[index].actual_time + self.time_interval
            else:
                flight.actual_time = flight.estimated_time# + self.time_interval


    def calc_actual_time(self, individual):
        indexes = np.random.permutation(2)
        for number,flight in enumerate(individual.flights[0:2]):
            flight.actual_time = flight.estimated_time# + self.time_interval
            flight.runway = indexes[number]
        for number, flight in enumerate(individual.flights[2:],2):
            flight.runway = random.randrange(2)
            runway = flight.runway
            index = max(idx for idx, flight in enumerate(individual.flights[0:number]) if flight.runway == runway)
            flight.actual_time = individual.flights[index].actual_time + self.time_interval

    def calc_actual_time_population(self, population):
        for individual in population:
            self.calc_actual_time(individual)



    def terminal_condition(self,):
        result = False
        if self.generation_number <= self.error:
            result = True
        return result

    def do_calcs(self, population, lambda_parameter, k, objective_functions):
        self.calc_actual_time_population(population)
        self.call_all_objectives_population(population)
        self.assign_rankings(objective_functions, population)
        self.calc_fitness_population(population, k, lambda_parameter)
                        
                

        
        
def prepare(n):
    population = [0 for i in range(n)]
    return population

def rank(vec):
    """
    
    :param vec: Rating
    :return: Ranking
    """
    return rankdata(vec, method = 'min').astype(int) 
