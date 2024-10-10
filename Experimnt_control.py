## This function will run the experiment protocol

# imports
import time

# this class should hold functions to do the following:
# 1. Generate the sparrow configuration based on the yaml files
# 2. Stop the acquistion of data from sparrow
# 3. Run the acquistion protocol (threaded)
# 4. Run the calculations and visulaization based on the recorded data



class ExperimentControl:
    def __init__(self, experiment_gui):
        # Should read the yaml files and generate the sparrow configuration
        