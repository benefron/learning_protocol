import matplotlib.pyplot as plt
import matplotlib
from Calculations_functions import *
import time
import numpy as np
import yaml
from SimulatedTrace import *
file_path = 'Recording_cfg.yaml'
%matplotlib Qt5Agg


from SimulatedTrace import *
stim_time = 600
matrix = vector_to_matrix(256)
stim_electrode = [1,2,3,4,5,6,7,8,9,10]


run_pyqt_app(stim_time,matrix,stim_electrode)