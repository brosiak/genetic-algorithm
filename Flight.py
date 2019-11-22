class Flight:
    def __init__(self, flight_type = '', airline = '', sequence_number = 0, flight_number = '', airplane_type = '', unit_loss = 0, estimated_time = 0, actual_time = 0, runway = -1, delay_losses = -1 ):
        """Intialization of flight
        
        Keyword Arguments:
            flight_type {str} -- approach or departure (default: {''})
            airline {str} -- name of airline (default: {''})
            sequence_number {int} -- sequence number of flight (default: {0})
            flight_number {str} -- airline's flight number (default: {''})
            airplane_type {str} -- type of airplane (default: {''})
            unit_loss {int} -- unit time delay loss (default: {0})
            estimated_time {int} -- estimated approach/departure time (default: {0})
            actual_time {int} -- actual approach/departure time (default: {0})
            runway {int} -- number of runway (default: {-1})
            delay_losses {int} -- delay losses (default: {-1})
        """
        self.flight_type = flight_type
        self.airline = airline
        self.sequence_number = sequence_number
        self.flight_number = flight_number
        self.airplane_type = airplane_type
        self.unit_loss = unit_loss
        self.estimated_time = estimated_time
        self.actual_time = actual_time
        self.runway = runway
        self.delay_losses = delay_losses


def init_flights(app_num, dep_num):
    flights = []
    for i in range(app_num):
        flights.append(Flight(flight_type = 'approach'))
    for j in range(dep_num):
        flights.append(Flight(flight_type = 'departure'))
    return flights