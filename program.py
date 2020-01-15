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
mutation_probability = -0.1
generation_gap = 0.9
elimination_rate = 0.2
alfa = 0.2
population_size = 10
lambda_parameter = 100
ro_parameter = 10
error = 100
k = 1.5
vk_min = 1
vk_max = 30
time_interval = 120
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
    ga = Genetic_algorithm.Genetic_algorithm(crossover_probability = crossover_probability, mutation_probability = mutation_probability, \
        generation_gap = generation_gap, elimination_rate = elimination_rate, alfa = alfa, population_size = population_size, \
            error = error, k = k, vk_min = vk_min, vk_max = vk_max, delta_t = delta_t, runways = runways, time_interval = time_interval)
    ga.assign_initial_data(approach_name, departure_name)
    ga.initialize_population(approach_name, departure_name)
    ga.calc_actual_time_population(ga.population)
    ga.call_all_objectives_population(ga.population)
    ga.assign_rankings(objective_functions, ga.population)
    ga.calc_fitness_population(ga.population, k, population_size)
    flight_losses = []
    while(ga.terminal_condition()):
        offspring = Genetic_algorithm.prepare(lambda_parameter)
        for i in range(lambda_parameter):
            ga.marriage(ro_parameter)
            test = ga.single_point_crossover()
            offspring[i] = copy.copy(test)
            ga.mutation_swap(offspring[i])

            #print(offspring[i].get_queue())
        ga.calc_actual_time_population(offspring)
        ga.call_all_objectives_population(offspring)
        ga.assign_rankings(objective_functions, offspring)
        ga.calc_fitness_population(offspring, k, lambda_parameter)
        flight_losses.append(min(individual.flight_losses for individual in offspring))
        ga.population = ga.roulette_selection(offspring, population_size)
        ga.generation_number += 1
    for number, individual in enumerate(ga.population):
        print('\n')
        print('individual number:'+str(number))
        print('fitness value: ' + str(individual.fitness))
        individual.get_queue_runways()
        print('robustness: '+str(individual.robustness))
        print('flight losses: '+ str(individual.flight_losses))
        print('runway throughtput: ' + str(individual.runway_throughput))
    print('minimal flight losses:' +str(min(flight_losses)))
        #print(individual.get_times_runways())
    # ga.call_all_objectives_population()
    # ga.assign_rankings(objective_functions, ga.population)
    # ga.marriage(ro = 2)
    # print(ga.parents[0].get_queue())
    # ga.mutation_shift(ga.parents[0])
    # print(ga.parents[0].get_queue())
    # genetic_algorithm.population[0].calculate_fitness(k = k, N = population_size)
    # genetic_algorithm.population[1].calculate_fitness(k = k, N = population_size)
    # genetic_algorithm.population[2].calculate_fitness(k = k, N = population_size)
    # print(genetic_algorithm.population[0].fitness)
    # genetic_algorithm.marriage(ro = 2)
    # for i in range(2):
    #     print(genetic_algorithm.parents[i].get_queue())
    # genetic_algorithm.single_point_crossover()
    # print("\n\n")
    # for i in range(2):
    #     print(genetic_algorithm.parents[i].get_queue())
    # print(genetic_algorithm.calc_selection_probability(genetic_algorithm.population[0],genetic_algorithm.population))
            
  