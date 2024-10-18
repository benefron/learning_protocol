import numpy as np
import pandas as pd

def generate_random_vector(length=15000, low=-0.1, high=0.1):
    return np.random.uniform(low, high, length)

def insert_peaks(max_num_peaks=2, peak_length=20, peak_height=2, iteration_numer=1,repition=1):
    num_peaks = np.random.randint(0, max_num_peaks + 1)
    vector = generate_random_vector(length=15000, low=-0.1, high=0.1)
    peak = np.concatenate([np.linspace(0, peak_height, peak_length // 2), np.linspace(peak_height, 0, peak_length // 2)])
    peak_indices = np.random.choice(len(vector) - peak_length, num_peaks, replace=False)
    num_rep = np.random.randint(2,10)
    for idx in peak_indices:
        if ~repition == 0:
            if iteration_numer > 90:
                vector[idx:idx + peak_length] = peak
        else:
            vector[idx:idx + peak_length] = peak
        if repition == 1 and iteration_numer > 35:
            if iteration_numer % 3 == 0:
                vector[2100:2100 + peak_length] = peak
        elif repition >=num_rep and iteration_numer > 4:
            if iteration_numer % 2 == 0:
                vector[2100:2100 + peak_length] = peak
        else:
            vector[idx:idx + peak_length] = peak
    return vector

def vector_to_matrix(elec_num):
    for i in range(elec_num):
        if i == 0:
            matrix = insert_peaks()
        else:
            matrix = np.vstack((matrix, insert_peaks())) 

    return matrix
    

def Single_electrode(iteration_number=1,rep_num = 1):
    vector = insert_peaks(3,20,2,iteration_number, rep_num)

    return vector

#def Multi_electrode(num_electrodes=100):
   # matrix = vector_to_matrix(num_electrodes)

   #return matrix
    


