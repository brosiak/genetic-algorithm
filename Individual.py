import Flight
import random
import copy
import numpy as np
class Individual:
    def __init__(self):
        self.flights = []
        self.departure_flights = []
        self.approach_flights = []
        self.fitness = 0
        self.runway_throughput = 0
        self.flight_losses = 0
        self.robustness = 0
        self.runway_throughput_ranking = 0
        self.flight_losses_ranking = 0
        self.robustness_ranking = 0
        self.individual_ranking = {}

    def init_all_flights(self, approach_data, departure_data):
        self.departure_flights = init_flights(departure_data, 'departure')
        self.approach_flights = init_flights(approach_data, 'approach')
        self.flights = self.approach_flights + self.departure_flights
    
    # def set_flights(self, flights):
    #     self.__flights = flights
    
    # def get_flights(self):
    #     return self.__flights

    def get_queue(self):
        flights = self.flights.copy()
        for i in range(len(flights)):
            num = flights[i].sequence_number
            flights[i] = num
        return flights
    
    
            
    

    


    def calc_runway_throughput(self):
        """calculate runway throughput of flight queue
        
        Returns:
            int -- runway throughput
        """
        self.runway_throughput = self.flights[-1].get_actual_time_s() - self.flights[0].get_actual_time_s()
        return self.runway_throughput

    def calc_flight_losses(self, delta_t):
        """calculate flight delay losses of flight queue
        
        Arguments:
            delta_t {int} -- permissible delay of flight
        
        Returns:
            double -- flight delay losses
        """
        losses = 0
        for i in range(len(self.flights)):
            if(self.flights[i].is_delayed(delta_t)):
                losses += (self.flights[i].delay_time -delta_t) * \
                    self.flights[i].unit_loss
            else:
                continue
        self.flight_losses = losses
        return losses


    def calc_robustness(self, delta_t):
        """calculate robustness of flight queue
        
        Arguments:
            delta_t {int} -- permissible delay of flight
        
        Returns:
            double -- robustness
        """
        robustness = 0
        for i in range(len(self.flights)):
            if(self.flights[i].is_delayed(delta_t)):
                robustness += 1
            else:
                continue
        self.robustness = robustness
        return robustness

    def calculate_objective_end(self, k, N, parameter):
        if parameter==1:
            return k * N ** 2
        else:
            return (N - parameter) ** 2

    def calculate_fitness(self, k, N):
        fitness = 0
        for i in self.individual_ranking:
            fitness += self.calculate_objective_end(k, N, self.individual_ranking.get(i))
        self.fitness = fitness
        #if(check_parameter(self.runway_throughput_ranking))
        #self.fitness = self.calc_runway_throughput() + self.calc_flight_losses() + self.calc_robustness()

    # def get_fintess(self):
    #     return self.__fitness

    # def get_runway_throughput(self):
    #     return self.__runway_throughput

    # def get_flight_losses(self):
    #     return self.__flight_losses

    # def get_robustness(self):
    #     return self.__robustness

    def get_robustness_percentage(self):
        return ((self.robustness / len(self.flights)) *100)

def init_flights(data, flight_type):
    flights = []
    for i in range(len(data.index)):
        try:
            flight = Flight.Flight(
                flight_type = flight_type,
                airline = data['Airline'][i],
                sequence_number = data['Sequence number'][i],
                flight_number = data['Flight number'][i],
                airplane_type = data['Type'][i],
                unit_loss = data['Unit time delay loss'][i],
                estimated_time = data['Estimated time'][i],
                actual_time = data['Actual time'][i],
                runway = data['Runway'][i],
                delay_losses = data['Delay Losses'][i])
        except KeyError as exc:
            print("Error occured, there is no column named ", str(exc))
            exit()
        except:
            print("something went wrong ")
        flights.append(flight)
    return flights

# def prepare(n):
#     population = [0 for i in range(n)]
#     return population

# def marriage(population, ro):
#     parents = prepare(ro)
#     selected_individuals = np.random.permutation(len(population))
#     for i in range(ro):
#         parents[i] = population[selected_individuals[i]]
#     return parents

# # =============================================================================
# # def initialize(population_size, individual):
# #     population = prepare(population_size)
# #     flights = individual.get_flights()
# #     for i in (random.sample(flights,len(flights))):
# #         population[i] = copy.deepcopy(individual)
# #         #flights = individual.get_flights()
# #         population[i].set_flights(flights[i])
# #     return population
# # =============================================================================

# def initialize_population(population_size, approach_data, departure_data):
#     population = []
#     for i in range(population_size):
#         individual = Individual()
#         individual.init_all_flights(approach_data, departure_data)
#         a = individual.flights
#         a = random.sample(a,len(a))
#         individual.flights = a
#         #individual.get_flights()
#         population.append(individual)
#     return population