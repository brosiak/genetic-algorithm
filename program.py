import Individual
import pandas as pd
from os import strerror

'''variables'''
approach_name = "approach_initial.txt"
departure_name = "departure_initial.txt"
delta_t = 120
'''variables'''




if __name__ == "__main__":
    try:    
        approach_data = pd.read_table(approach_name)
        departure_data = pd.read_table(departure_name)
    except IOError as exc:
        print("Error occured ", strerror(exc.errno))
        exit(exc.errno)
    individual = Individual.Individual()
    individual.init_all_flights(approach_data, departure_data)
    print(individual.calc_flight_losses(delta_t))
    print(individual.calc_robustness(delta_t))    
    print("robustness is ",round(individual.get_robustness_percentage(), 2),"%")