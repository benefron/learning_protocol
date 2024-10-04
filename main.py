import tkinter as tk
from GUIs import ExperimentGUI  # Import your ExperimentGUI class from the file where it is defined
from SimulatedTrace import generate_random_vector, insert_peaks
#from Experimnt_control import generate_random_number_after_delay
#import time

def main():
    # Retrive chip number from sparrow
    chip_number = str('SP105')
    choosen_electorde = None

    
    # Create the root window
    root = tk.Tk()

    # Initialize the GUI with the root window
    experiment_gui = ExperimentGUI(root, chip_number,choosen_electorde)

    # Use the `get_parameters` method to retrieve parameters in other parts of your code
    parameters = experiment_gui.get_parameters()
    experiment_gui.log_message(f"Initial Parameters: {parameters}")

  
    # Start the Tkinter main loop to display the GUI
    root.mainloop()
    

if __name__ == "__main__":
    main()
