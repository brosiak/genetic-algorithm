import datetime
import time
class Flight:
    def __init__(self, flight_type = '', airline = '', sequence_number = 0, flight_number = '', airplane_type = '', unit_loss = 0, estimated_time = 0, actual_time = 0, runway = -1, delay_losses = -1, relation = {} ):
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
        self.delay_time = 0
        self.relation = relation
    
    # def get_type(self):
    #     return(self.flight_type)

    # def get_runway(self):
    #     return(self.runway)

    # def get_delay_time(self):
    #     return(self.delay_time)
    
    # def get_actual_time_s(self):
    #     return self.hms_to_s(self.actual_time)
    
    # def get_estimated_time(self):
    #     return self.hms_to_s(self.estimated_time)

    def get_actual_time_s(self):
        return self.actual_time
    
    def get_estimated_time(self):
        return self.estimated_time

    # def get_unit_loss(self):
    #     return(self.unit_loss)

    # def get_actual_time(self):
    #     return(self.actual_time)
    
    # def get_sequence_number(self):
    #     return(self.sequence_number)

    def hms_to_s(self, hms_time):
        """changes time string in format hours:minutes:seconds to seconds
        
        Arguments:
            hms_time {string} -- h:m:s 
        
        Returns:
            int -- seconds
        """
        hours, minutes, seconds = hms_time.split(':')
        secs = int(datetime.timedelta(hours = int(hours), minutes = int(minutes), seconds = int(seconds)).total_seconds())
        return secs
    
    def s_to_hms(self, secs):
        return(time.strftime('%H:%M:%S', time.gmtime(secs)))

    # def calc_delay(self):
    #     """calculating delay of flight
    #     """
    #     a_secs = self.hms_to_s(self.actual_time)
    #     e_secs = self.hms_to_s(self.estimated_time)
    #     self.delay_time = a_secs - e_secs
    #     return(self.delay_time)

    def calc_delay(self):
        """calculating delay of flight
        """
        self.delay_time = self.actual_time - self.estimated_time
        return(self.delay_time)

    def is_delayed(self, delta_t):
        if(delta_t < self.calc_delay()):
            return True
        else:
            return False
    
    