from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
file_names_500 = [
    '500_inversion_10.txt',
    '500_inversion_20.txt',
    '500_inversion_50.txt',
    '500_inversion_100.txt',
    '500_swap_10.txt',
    '500_swap_20.txt',
    '500_swap_50.txt',
    '500_swap_100.txt',
    '500_scramble_10.txt',
    '500_scramble_20.txt',
    '500_scramble_50.txt',
    '500_scramble_100.txt',
    '500_shift_10.txt',
    '500_shift_20.txt',
    '500_shift_50.txt',
    '500_shift_100.txt',
    
]

file_names_1000 = [
    '1000_inversion_10.txt',
    '1000_inversion_20.txt',
    '1000_inversion_50.txt',
    '1000_inversion_100.txt',
    '1000_swap_10.txt',
    '1000_swap_20.txt',
    '1000_swap_50.txt',
    '1000_swap_100.txt',
    '1000_scramble_10.txt',
    '1000_scramble_20.txt',
    '1000_scramble_50.txt',
    '1000_scramble_100.txt',
    '1000_shift_10.txt',
    '1000_shift_20.txt',
    '1000_shift_50.txt',
    '1000_shift_100.txt',
    
]

labels=[
        'Mutacja odwracania',
        'Mutacja zamiany',
        'Mutacja przemieszania',
        'Mutacja przesunięcia'
        ]

class baseClass:
    def __init__(self, robustness=[], flight_losses=[], throughput=[], execution_time=[]):
        self.robustness = robustness
        self.flight_losses = flight_losses
        self.throughput = throughput
        self.execution_time = execution_time

baseClasses = []
if __name__ == "__main__":
    for counter, file_name in enumerate(file_names_1000):
        data = pd.read_table(file_name) #usecols=['Robustness', 'Flight losses', 'Runway throughput', 'Execution time'])
        column = data.columns[0]
        data[['Robustness', 'Flight losses', 'Runway throughput', 'Execution time']] = data['Robustness  Flight losses   Runway throughput   Execution time'].str.split("  ", expand=True)
        baseClasses.append(baseClass(
            robustness = data['Robustness'],
            flight_losses= data["Flight losses"],
            throughput = data['Runway throughput'],
            execution_time = data['Execution time']
            ))
    
    for base in baseClasses:
        for i,execution in enumerate(base.execution_time):
            execution = "".join(execution.split())
            base.execution_time[i] = execution
        base.robustness = list(map(int, base.robustness))
        base.execution_time = list(map(float, base.execution_time)) 
        base.flight_losses = list(map(float, base.flight_losses)) 
        base.throughput = list(map(int, base.throughput))  
    rob_list=[[],[],[],[]]
    time_list=[[],[],[],[]]
    losses_list=[[],[],[],[]]
    throughput_list =[[],[],[],[]]
    counter = 0
    for i,_ in enumerate(baseClasses, 1):
        time_list[counter].append(np.mean(_.execution_time))
        rob_list[counter].append(np.mean(_.robustness))
        losses_list[counter].append(np.mean(_.flight_losses))
        throughput_list[counter].append(np.mean(_.throughput))
        if i>0 and i%4==0:
            counter += 1
        
    x=[10,20,50,100]
    xi = list(range(len(x)))
    plt.figure
    plt.xticks(xi, x)
    plt.xlabel('Wielkość populacji')
    plt.ylabel('Przepustowość[s]')
    for plot in throughput_list:
        plt.plot(plot)
    plt.legend(labels)
    plt.savefig('1000_throughput', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    plt.close