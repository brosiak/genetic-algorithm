import Flight
class Individual:
    def __init__(self):
        self.flights = []
        self.fitness = 0
        self.runway_throughput = 0
        self.flight_losses = 0
        self.robustness = 0

    def calc_runway_throughput(self):
        pass
    def calc_flight_losses(self):
        pass
    def calc_robustness(self):
        pass
    def calculate_fitness(self):
        self.fitness = self.calc_runway_throughput() + self.calc_flight_losses() + self.calc_robustness()
        return self.fitness


        
    