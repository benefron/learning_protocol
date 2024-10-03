import tkinter as tk
from GUIs import ExperimentGUI  # Import your ExperimentGUI class from the file where it is defined

def main():
    # Create the root window
    root = tk.Tk()

    # Initialize the GUI with the root window
    experiment_gui = ExperimentGUI(root)

    # Use the `get_parameters` method to retrieve parameters in other parts of your code
    parameters = experiment_gui.get_parameters()
    experiment_gui.log_message(f"Initial Parameters: {parameters}")



    # Example of logging a message from another function
    experiment_gui.log_message("This is a test message from main.py")

    # Start the Tkinter main loop to display the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
