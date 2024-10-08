
# Learning on MEA

This repository holds the functions and protocol to run an experiment based on the work of *Shahaf and Marom 2001* testing the network activity of a neuronal culture on an MEA undergoing a stimulation protocol for uninstructed learning

## Outline of experiment

- Record ongoing activity on the entire chip to establish pre-learning baseline
- Running a stimulation protocol to identify target electrode and establish baseline response
- Choose electrode with **R/S < 1**
- Run the learning paradigm to reach **R/S < 2**
- If criteria is reached the protocol stops for 5 minutes
- After n > 30 reptitions (or if learning plato reached)
- Record ongoing actitivy on the entire chip to evaluate changes due to learning
- Run stimulation protocol and record from all chip to evaluate learning induced changes
- **Optional:** move to next active area to run protocol

## Files and codes

- User input parameters
- Communication functions with sparrow app
- Functions for computation evaluating criteria
- Masseges to email user
  

