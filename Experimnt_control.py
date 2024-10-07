## This function will run the experiment protocol

# imports
import time
# The protocol will first run a continuous recording from all active areas 
# of the chip establishing a baseline for the experiment.

# define a function to run the baseline

def run_baseline(exp):
    # run the baseline
    time.sleep(10)
    message = "Baseline established"
    return message

def run_stimulation(exp):
    # run the stimulation
    target_electrode = 10
    time.sleep(10)
    message = f"Target electrode {target_electrode} chosen"
    return target_electrode , message

