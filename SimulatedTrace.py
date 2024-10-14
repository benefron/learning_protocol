import numpy as np
import pandas as pd

def generate_random_vector(length=3000, low=-0.1, high=0.1):
    return np.random.uniform(low, high, length)

def insert_peaks(max_num_peaks=3, peak_length=20, peak_height=2):
    num_peaks = np.random.randint(0, max_num_peaks + 1)
    vector = generate_random_vector(length=3000, low=-0.1, high=0.1)
    peak = np.concatenate([np.linspace(0, peak_height, peak_length // 2), np.linspace(peak_height, 0, peak_length // 2)])
    peak_indices = np.random.choice(len(vector) - peak_length, num_peaks, replace=False)
    
    for idx in peak_indices:
        vector[idx:idx + peak_length] = peak
    
    return vector

def vector_to_matrix(elec_num):
    for i in range(elec_num):
        if i == 0:
            matrix = insert_peaks()
        else:
            matrix = np.vstack((matrix, insert_peaks())) 

    return matrix
    

def Single_electrode():
    vector = insert_peaks()

    return vector

#def Multi_electrode(num_electrodes=100):
   # matrix = vector_to_matrix(num_electrodes)

   #return matrix
    




