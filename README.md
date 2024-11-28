# Learning on MEA

This repository holds the functions and protocol to run an experiment based on the work of *Shahaf and Marom 2001* testing the network activity of a neuronal culture on an MEA undergoing a stimulation protocol for uninstructed learning.

## Outline of Experiment

- Record ongoing activity on the entire chip to establish pre-learning baseline.
- Running a stimulation protocol to identify target electrode and establish baseline response.
- Choose electrode with **R/S < 1**.
- Run the learning paradigm to reach **R/S < 2**.
- If criteria is reached the protocol stops for 5 minutes.
- After n > 30 repetitions (or if learning plateau reached).
- Record ongoing activity on the entire chip to evaluate changes due to learning.
- Run stimulation protocol and record from all chip to evaluate learning induced changes.
- **Optional:** move to next active area to run protocol.

## Project Structure

- **`main.py`**: The entry point of the application. It initializes the GUI and starts the Tkinter main loop.
- **`GUIs.py`**: Contains the `ExperimentGUI` class, which manages the graphical user interface for the experiment. It includes methods for logging, saving parameters, handling YAML files, and updating plots.
- **`Experiment_control.py`**: Contains the `ExperimentControl` class, which manages the experiment's execution. It includes methods for generating Sparrow configurations, running baseline and experiment acquisitions, and handling stimulation protocols.
- **`SimulatedTrace.py`**: Contains functions for generating simulated data traces, such as `insert_peaks` and `generate_random_vector`.
- **`Calculations_functions.py`**: Contains functions for performing calculations on the recorded data.
- **`SparrowRpcService.py`**: Contains the `SparrowRpcService` class, which provides an API for communicating with the Sparrow application using gRPC.
- **`contracts.proto`**: Defines the gRPC service and messages used for communication between the client and the Sparrow application.
- **`contracts_pb2.py` and `contracts_pb2_grpc.py`**: Generated gRPC code based on `contracts.proto`.
- **`README.md`**: Provides an overview of the experiment and the project files.
- **`Protocol.tex`**: A LaTeX document describing the experiment protocol in detail.

## Key Components and Their Roles

### Graphical User Interface (GUI)
- The `ExperimentGUI` class in `GUIs.py` creates and manages the GUI for the experiment. It includes input fields for experiment parameters, buttons for starting and stopping the experiment, and areas for logging messages and displaying plots.
- Methods like `get_parameters`, `save_parameters`, `save_log`, and `open_yaml_file` handle user interactions and file operations.

### Experiment Control
- The `ExperimentControl` class in `Experiment_control.py` manages the experiment's execution, including running baseline and experiment acquisitions and handling stimulation protocols.
- Methods like `run_basleine`, `run_preExperiment_stimulation`, and `run_Experiment_stimulation` simulate the experiment's execution and log messages to the GUI.

### Simulated Data
- The `SimulatedTrace.py` file contains functions for generating simulated data traces, such as `insert_peaks` and `generate_random_vector`. These functions are used to create synthetic data for testing and visualization purposes.

### Calculations
- The `Calculations_functions.py` file contains functions for performing calculations on the recorded data. These functions are used to analyze the data and evaluate the experiment's results.

### Sparrow Communication
- The `SparrowRpcService.py` file contains the `SparrowRpcService` class, which provides an API for communicating with the Sparrow application using gRPC. This class includes methods for various operations, such as starting and stopping acquisitions, creating configurations, and exporting data.
- The `contracts.proto` file defines the gRPC service and messages used for communication between the client and the Sparrow application. The `contracts_pb2.py` and `contracts_pb2_grpc.py` files are generated gRPC code based on `contracts.proto`.

### Experiment Protocol
- The `Protocol.tex` file is a LaTeX document that describes the experiment protocol in detail. It includes sections on the experiment's overview, baseline recording, stimulation recording, and learning protocol.

## Workflow

### Initialization
- The `main.py` script initializes the GUI and starts the Tkinter main loop.
- The user interacts with the GUI to set experiment parameters and start the experiment.

### Experiment Execution
- The `ExperimentControl` class manages the experiment's execution, including running baseline and experiment acquisitions and handling stimulation protocols.
- Simulated data is generated using functions from `SimulatedTrace.py`.

### Data Analysis
- Calculations are performed on the recorded data using functions from `Calculations_functions.py`.
- Results are displayed in the GUI and logged for further analysis.

### Communication with Sparrow
- The `SparrowRpcService` class provides an API for communicating with the Sparrow application using gRPC.
- The experiment protocol is defined in `Protocol.tex` and followed during the experiment.

This project provides a comprehensive framework for running and analyzing experiments on neuronal network activity using an HD-MEA.
