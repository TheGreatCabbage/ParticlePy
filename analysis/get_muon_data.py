import os
import matplotlib.pyplot as plt

data_folder = 'data'

def get_cyl_data(set_number):
    '''
    Returns nested lists of the muon counts:
    [[count],[timestamp]]
    '''

    cyl_data = [[],[]]
    for file in os.listdir(data_folder):
        contained_string = "{}.data".format(set_number)
        if contained_string in file:  # Only use files with the correct names.
            with open("{}/{}".format(data_folder, file), 'r') as f:
                for line in f:
                    line_data = line.split(" ")
                    #count
                    count = int(line_data[0]) - 40000
                    cyl_data[0].append(count) if count > 0  else cyl_data[0].append(0)
                    #time
                    cyl_data[1].append(float(line_data[1]))

    return cyl_data

def get_pi_data():
    '''
    Returns nested lists of the muon detection times:
    [[threshold 1],[threshold 3.3]]
    '''
    set_1 = set()
    set_3_3 = set()
    pi_data = [set_1,set_3_3]
    
    threshold_1_files = ['pi_data_0.txt','pi_data_1.txt','pi_data_2.txt']

    #threshold_3_3_files = ['pi_data_3.txt']
    threshold_3_3_files = []
   
    for filename in threshold_1_files:
        with open("{}/{}".format(data_folder, filename), 'r') as f:
            for line in f:
                line_data = line.split(':')
                pi_data[0].add(float(line_data[1]))
    
    for filename in threshold_3_3_files:
        with open("{}/{}".format(data_folder, filename), 'r') as f:
            for line in f:
                line_data = line.split(':')
                pi_data[1].add(float(line_data[1]))
    
    return pi_data

def average_minutes_prior_to_x_cyl(dataset,x):
    '''
    Returns nested lists of the muon counts averaged over x mins prior to the timestamp:
    [[counts],[timestamps]]
    '''
    this_average = []

    counts = []
    timestamps = []
    x_mins = 60*x
    for i in range(len(dataset[1])):
        this_average.append(dataset[0][i])
        if (int(dataset[1][i]) % x_mins) == 0:
            average = sum(this_average)/len(this_average)
            
            timestamps.append(dataset[1][i])
            counts.append(average)

            this_average = []
    
    return [counts, timestamps]

def average_minutes_prior_to_x_pi(times_list,x):
    '''
    Returns nested lists of the muon count rates averaged over x mins prior to the timestamp:
    [[rate],[imestamps]]
    '''
    averages = []
    timestamps = []
    x_mins = 60*x
    counts = 0
    initial_time = times_list[0] - (times_list[0] % x_mins)

    for i in range(len(times_list)):
        if times_list[i] < (initial_time + x_mins):
            counts += 1
        else:
            timestamps.append(times_list[i] - (times_list[i] % x_mins))
            averages.append(counts/(x_mins))
            
            initial_time = times_list[i]
            counts = 1
    return [averages, timestamps]


