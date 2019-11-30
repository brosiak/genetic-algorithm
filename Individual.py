import Flight
class Individual:
    def __init__(self):
        self.__flights = []
        self.__departure_flights = []
        self.__approach_flights = []
        self.__fitness = 0
        self.__runway_throughput = 0
        self.__flight_losses = 0
        self.__robustness = 0

    def init_all_flights(self, approach_data, departure_data):
        self.__departure_flights = init_flights(departure_data, 'departure')
        self.__approach_flights = init_flights(approach_data, 'approach')
        self.__flights = self.__approach_flights + self.__departure_flights
    


    def calc_runway_throughput(self):
        pass

    def calc_flight_losses(self, delta_t):
        losses = 0
        for i in range(len(self.__flights)):
            if(self.__flights[i].is_delayed(delta_t)):
                losses += (self.__flights[i].get_delay_time() -delta_t) * \
                    self.__flights[i].get_unit_loss()
            else:
                continue
        self.__flight_losses = losses
        return losses


    def calc_robustness(self, delta_t):
        robustness = 0
        for i in range(len(self.__flights)):
            if(self.__flights[i].is_delayed(delta_t)):
                robustness += 1
            else:
                continue
        self.__robustness = robustness
        return robustness

    def calculate_fitness(self):
        #self.fitness = self.calc_runway_throughput() + self.calc_flight_losses() + self.calc_robustness()
        pass

    def get_fintess(self):
        return self.__fitness

    def get_runway_throughput(self):
        return self.__runway_throughput

    def get_flight_losses(self):
        return self.__flight_losses

    def get_robustness(self):
        return self.__robustness

    def get_robustness_percentage(self):
        return ((self.get_robustness() / len(self.__flights)) *100)

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

