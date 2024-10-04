import numpy as np
import pandas as pd

def generate_random_vector(length=300000, low=-0.1, high=0.1):
    return np.random.uniform(low, high, length)

def insert_peaks(num_peaks=40, peak_length=20, peak_height=2):
    vector = generate_random_vector(length=300000, low=-0.1, high=0.1)
    peak = np.concatenate([np.linspace(0, peak_height, peak_length // 2), np.linspace(peak_height, 0, peak_length // 2)])
    peak_indices = np.random.choice(len(vector) - peak_length, num_peaks, replace=False)
    
    for idx in peak_indices:
        vector[idx:idx + peak_length] = peak
    
    return vector

def vector_to_matrix(vector, rows=300, cols=1000):
    if len(vector) != rows * cols:
        raise ValueError("The length of the vector does not match the specified dimensions.")
    return vector.reshape((rows, cols))

vector = insert_peaks()
matrix = vector_to_matrix(vector)


