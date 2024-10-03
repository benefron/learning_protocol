import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import queue
import os

class ExperimentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Experiment GUI")

        # User inputs
        self.well_number = tk.IntVar(value=1)
        self.max_time = tk.IntVar(value=10)
        self.rest_time = tk.IntVar(value=10)
        self.criterion = tk.IntVar(value=2)
        self.simulating_electrode = tk.IntVar(value=120)
        self.target_electrode = tk.StringVar(value="")  # New field for target electrode
        self.experiment_type = tk.StringVar(value="Experiment")
        self.path = tk.StringVar(value="")

        # Create input fields
        self.create_input_fields()

        # Create buttons
        self.create_buttons()

        # Create clock label
        self.clock_label = tk.Label(root, text="00:00:00")
        self.clock_label.pack()

        # Create message area
        self.message_area = tk.Text(root, height=10, state='disabled')
        self.message_area.pack()

        # Queue for thread-safe logging
        self.log_queue = queue.Queue()

        # Variable to control the clock
        self.running = False

        # Start a separate thread to handle GUI message logging
        self.root.after(100, self.process_log_queue)

    def create_input_fields(self):
        tk.Label(self.root, text="Well Number:").pack()
        tk.Entry(self.root, textvariable=self.well_number).pack()

        tk.Label(self.root, text="Max Time (minutes):").pack()
        tk.Entry(self.root, textvariable=self.max_time).pack()

        tk.Label(self.root, text="Rest Time (minutes):").pack()
        tk.Entry(self.root, textvariable=self.rest_time).pack()

        tk.Label(self.root, text="Criterion (R/S):").pack()
        tk.Entry(self.root, textvariable=self.criterion).pack()

        tk.Label(self.root, text="Simulating Electrode:").pack()
        tk.Entry(self.root, textvariable=self.simulating_electrode).pack()

        tk.Label(self.root, text="Target Electrode:").pack()  # Label for new field
        tk.Entry(self.root, textvariable=self.target_electrode).pack()  # Entry for new field

        tk.Label(self.root, text="Experiment Type:").pack()
        tk.Radiobutton(self.root, text="Experiment", variable=self.experiment_type, value="Experiment").pack()
        tk.Radiobutton(self.root, text="Control", variable=self.experiment_type, value="Control").pack()

        tk.Label(self.root, text="Path:").pack()
        self.path_label = tk.Label(self.root, textvariable=self.path)
        self.path_label.pack()

    def create_buttons(self):
        self.start_button = tk.Button(self.root, text="Start Experiment", command=self.start_experiment)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Experiment", command=self.stop_experiment)
        self.stop_button.pack()

        self.load_path_button = tk.Button(self.root, text="Load Path", command=self.load_path)
        self.load_path_button.pack()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack()

    def start_experiment(self):
        self.running = True
        self.start_button.config(state='disabled')
        self.load_path_button.config(state='disabled')
        self.disable_inputs()
        self.log_message(f"Starting experiment on well {self.well_number.get()}")
        threading.Thread(target=self.update_clock).start()

    def stop_experiment(self):
        self.running = False
        self.start_button.config(state='normal')
        self.load_path_button.config(state='normal')
        self.enable_inputs()
        self.log_message("Experiment stopped")

        # Save the log when stopping the experiment
        self.save_log()

    def load_path(self):
        path = filedialog.askdirectory()
        self.path.set(path)
        self.log_message(f"Path loaded: {path}")

    def disable_inputs(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Entry) or isinstance(widget, tk.Radiobutton):
                widget.config(state='disabled')

    def enable_inputs(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Entry) or isinstance(widget, tk.Radiobutton):
                widget.config(state='normal')

    def update_clock(self):
        start_time = time.time()
        while self.running:
            elapsed_time = time.time() - start_time
            self.clock_label.config(text=time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
            time.sleep(1)

    def log_message(self, message):
        """Log a message to the message area in a thread-safe manner."""
        self.log_queue.put(message)

    def process_log_queue(self):
        """Process the log queue and display messages in the message area."""
        while not self.log_queue.empty():
            message = self.log_queue.get()
            self.message_area.config(state='normal')
            self.message_area.insert(tk.END, message + "\n")
            self.message_area.config(state='disabled')
        self.root.after(100, self.process_log_queue)

    def update_target_electrode(self, electrode):
        """Update the target electrode field."""
        self.target_electrode.set(electrode)
        self.log_message(f"Target electrode updated to: {electrode}")

    def get_parameters(self):
        """Return the current parameters as a dictionary."""
        return {
            "well_number": self.well_number.get(),
            "max_time": self.max_time.get(),
            "rest_time": self.rest_time.get(),
            "criterion": self.criterion.get(),
            "simulating_electrode": self.simulating_electrode.get(),
            "target_electrode": self.target_electrode.get(),
            "experiment_type": self.experiment_type.get(),
            "path": self.path.get(),
        }

    def save_log(self):
        """Save the contents of the message area to a log.txt file in the specified path."""
        if self.path.get():
            log_contents = self.message_area.get("1.0", tk.END).strip()
            log_file_path = os.path.join(self.path.get(), "log.txt")

            try:
                with open(log_file_path, 'w') as log_file:
                    log_file.write(log_contents)
                self.log_message(f"Log saved successfully at {log_file_path}")
            except Exception as e:
                self.log_message(f"Failed to save log: {e}")
        else:
            self.log_message("No path specified. Please load a path to save the log.")
