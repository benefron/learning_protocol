import numpy as np
import yaml

class data_calculation:
    def __init__(self, num_runs=30, length=100, stimulation_time=10, target_time=[40, 60],yaml_file='config.yaml'):
        
        with open(yaml_file, 'r') as file:
            self.config = yaml.safe_load(file)
        self.electrode_screen = np.zeros(())

   