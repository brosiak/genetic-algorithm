import Individual
import Genetic_algorithm
import pandas as pd
import copy
from os import strerror
import time

'''variables'''
approach_name = "approach_initial.txt"
departure_name = "departure_initial.txt"
delta_t = 120
runways = 2
crossover_probability = 0.9
mutation_probability = 0.1
generation_gap = 0.9
elimination_rate = 0.2
alfa = 0.2
population_size = 100
error = 2500
k = 1.5
vk_min = 1
vk_max = 30
objective_functions = ['runway_throughput', 'flights_losses', 'robustness']
'''variables'''




if __name__ == "__main__":
    # try:    
    #     approach_data = pd.read_table(approach_name)
    #     departure_data = pd.read_table(departure_name)
    # except IOError as exc:
    #     print("Error occured ", strerror(exc.errno))
    #     exit(exc.errno)
    # individual = Individual.Individual()
    # individual.init_all_flights(approach_data, departure_data)
    # print(individual.calc_flight_losses(delta_t))
    # print(individual.calc_robustness(delta_t))    
    # print("robustness is ",round(individual.get_robustness_percentage(), 2),"%")
    # print(individual.calc_runway_throughput())
    # print(individual.get_queue())
    # start = time.time()
    # population = Individual.initialize_population(population_size, approach_data, departure_data)
    # end = time.time()
    # print("without copying: ",end-start)
    # print(population[0].get_queue())
    genetic_algorithm = Genetic_algorithm.Genetic_algorithm(crossover_probability = crossover_probability, mutation_probability = mutation_probability, \
        generation_gap = generation_gap, elimination_rate = elimination_rate, alfa = alfa, population_size = population_size, \
            error = error, k = k, vk_min = vk_min, vk_max = vk_max, delta_t = delta_t, runways = runways)
    genetic_algorithm.assign_initial_data(approach_name, departure_name)
    genetic_algorithm.initialize_population(approach_name, departure_name)
    genetic_algorithm.call_all_objectives_population()
    genetic_algorithm.assign_rankings(objective_functions, genetic_algorithm.population)
    genetic_algorithm.population[0].calculate_fitness(k = k, N = population_size)
    print(genetic_algorithm.population[0].fitness)
    
            
  