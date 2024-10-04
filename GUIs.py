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

        # Configure grid layout for the root window
        self.root.columnconfigure(0, weight=1)  # Left frame column
        self.root.columnconfigure(1, weight=1)  # Right frame column
        self.root.rowconfigure(0, weight=1)  # Top row (Left and Right)
        self.root.rowconfigure(1, weight=1)  # Bottom row

        # Create main frames and use grid layout
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.right_frame = tk.Frame(root)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # User inputs
        self.well_number = tk.IntVar(value=1)
        self.max_time = tk.IntVar(value=10)
        self.rest_time = tk.IntVar(value=10)
        self.criterion = tk.IntVar(value=2)
        self.simulating_electrode = tk.IntVar(value=120)
        self.target_electrode = tk.StringVar(value="")  # New field for target electrode
        self.experiment_type = tk.StringVar(value="Experiment")
        self.path = tk.StringVar(value="")
        self.path_save = tk.StringVar(value="")
        self.exp_path_storage = tk.StringVar(value="")
        self.exp_path_streaming = tk.StringVar(value="")

        # Create input fields
        self.create_input_fields()

        # Create buttons
        self.create_buttons()

        # Create clock label
        #self.clock_header = tk.Label(self.right_frame, text="Elapsed Time:")
        #self.clock_header.pack(pady=10)
        self.clock_label = tk.Label(self.right_frame, text="Elapsed Time: 00:00:00")
        self.clock_label.pack(pady=10)

        # Create message area
        self.message_area = tk.Text(self.bottom_frame, height=10, state='disabled')
        self.message_area.pack(fill=tk.BOTH, expand=True)

        # Queue for thread-safe logging
        self.log_queue = queue.Queue()

        # Variable to control the clock
        self.running = False

        # Start a separate thread to handle GUI message logging
        self.root.after(100, self.process_log_queue)

    def create_input_fields(self):
        tk.Label(self.left_frame, text="Experiment Parameters:").pack(anchor='w')

        tk.Label(self.left_frame, text="Well Number:").pack(anchor='w')
        tk.Entry(self.left_frame, textvariable=self.well_number, width=10).pack(anchor='w')

        tk.Label(self.left_frame, text="Max Time (minutes):").pack(anchor='w')
        tk.Entry(self.left_frame, textvariable=self.max_time, width=10).pack(anchor='w')

        tk.Label(self.left_frame, text="Rest Time (minutes):").pack(anchor='w')
        tk.Entry(self.left_frame, textvariable=self.rest_time, width=10).pack(anchor='w')

        tk.Label(self.left_frame, text="Criterion (R/S):").pack(anchor='w')
        tk.Entry(self.left_frame, textvariable=self.criterion, width=10).pack(anchor='w')

        tk.Label(self.left_frame, text="Simulating Electrode:").pack(anchor='w')
        tk.Entry(self.left_frame, textvariable=self.simulating_electrode, width=10).pack(anchor='w')

        tk.Label(self.left_frame, text="Target Electrode:").pack(anchor='w')  # Label for new field
        tk.Entry(self.left_frame, textvariable=self.target_electrode, width=10).pack(anchor='w')  # Entry for new field

        tk.Label(self.left_frame, text="Experiment Type:").pack(anchor='w')
        experiment_types = ["Experiment", "Control"]  # List of options for the drop-down menu
        self.experiment_type_menu = tk.OptionMenu(self.left_frame, self.experiment_type, *experiment_types)
        self.experiment_type_menu.pack(anchor='w')

    def create_buttons(self):
        self.start_button = tk.Button(self.right_frame, text="Start Experiment", command=self.start_experiment)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.right_frame, text="Stop Experiment", command=self.stop_experiment)
        self.stop_button.pack(pady=5)

        self.load_path_button = tk.Button(self.right_frame, text="Load Stream Path", command=self.load_path)
        self.load_path_button.pack(pady=5)

        self.load_path_button_storage = tk.Button(self.right_frame, text="Load Storage Path", command=self.load_path_storage)
        self.load_path_button_storage .pack(pady=5)

        self.quit_button = tk.Button(self.right_frame, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=5)

        tk.Label(self.right_frame, text="Path stream (fast):").pack(anchor='w', pady=5)
        self.path_label = tk.Label(self.right_frame, textvariable=self.path)
        self.path_label.pack(anchor='w')

        tk.Label(self.right_frame, text="Path storage (slow):").pack(anchor='w', pady=5)
        self.path_save_label = tk.Label(self.right_frame, textvariable=self.path_save)
        self.path_save_label.pack(anchor='w')

    def start_experiment(self):
        if self.path_save.get():
            a=1
        else:
            messagebox.showwarning("Warning", "Please load a storage path before starting the experiment.")
            return
        if self.path.get():
            self.running = True
            prefix = "SP101"  # You can change this prefix later
            today_date = time.strftime("%d%m%Y")
            well_number = self.well_number.get()
            dir_name = f"{prefix}_{today_date}_well{well_number}"

            # Create the directory in the streaming path
            exp_path_streaming = os.path.join(self.path.get(), dir_name)
            os.makedirs(exp_path_streaming, exist_ok=True)
            self.exp_path_streaming.set(exp_path_streaming)

            # Create the directory in the storage path
            exp_path_storage = os.path.join(self.path_save.get(), dir_name)
            os.makedirs(exp_path_storage, exist_ok=True)
            self.exp_path_storage.set(exp_path_storage)

            self.log_message(f"Experiment directories created: {exp_path_streaming} and {exp_path_storage}")
            self.start_button.config(state='disabled')
            self.load_path_button_storage.config(state='disabled')
            self.load_path_button.config(state='disabled')
            self.quit_button.config(state='disabled')
            self.disable_inputs()
            self.experiment_type_menu.config(state='disabled')
            self.log_message(f"Starting experiment on well {self.well_number.get()}")
            parameters = self.get_parameters()
            self.log_message(f"Experiment Parameters: {parameters}")
            threading.Thread(target=self.update_clock).start()
        else:
            messagebox.showwarning("Warning", "Please load a streaming path before starting the experiment.")

    def stop_experiment(self):  
        self.running = False
        self.start_button.config(state='normal')
        self.load_path_button.config(state='normal')
        self.load_path_button_storage.config(state='normal')
        self.enable_inputs()
        self.log_message("Experiment stopped")
        self.quit_button.config(state='normal')

        # Save the log when stopping the experiment
        self.save_log()

    def load_path(self):
        path = filedialog.askdirectory()
        self.path.set(path)
        self.log_message(f"Streaming Path loaded: {path}")

    def load_path_storage(self):
        path_save = filedialog.askdirectory()
        self.path_save.set(path_save)
        self.log_message(f"Storage Path loaded: {path_save}")

    def disable_inputs(self):
        for widget in self.left_frame.winfo_children():
            if isinstance(widget, tk.Entry) or isinstance(widget, tk.Radiobutton):
                widget.config(state='disabled')

    def enable_inputs(self):
        for widget in self.left_frame.winfo_children():
            if isinstance(widget, tk.Entry) or isinstance(widget, tk.Radiobutton):
                widget.config(state='normal')

    def update_clock(self):
        start_time = time.time()
        while self.running:
            elapsed_time = time.time() - start_time
            self.clock_label.config(text=time.strftime("Elapsed Time: %H:%M:%S", time.gmtime(elapsed_time)))
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
        if self.exp_path_storage.get():
            log_contents = self.message_area.get("1.0", tk.END).strip()
            log_file_path = os.path.join(self.exp_path_storage.get(), "log.txt")

            try:
                with open(log_file_path, 'w') as log_file:
                    log_file.write(log_contents)
                self.log_message(f"Log saved successfully at {log_file_path}")
            except Exception as e:
                self.log_message(f"Failed to save log: {e}")
        else:   
            self.log_message("No storage path specified. Please load a path to save the log.")
        if self.exp_path_streaming.get():
            log_contents = self.message_area.get("1.0", tk.END).strip()
            log_file_path = os.path.join(self.exp_path_streaming.get(), "log.txt")

            try:
                with open(log_file_path, 'w') as log_file:
                    log_file.write(log_contents)
                self.log_message(f"Log saved successfully at {log_file_path}")
            except Exception as e:
                self.log_message(f"Failed to save log: {e}")
        else:
            self.log_message("No streaming path specified. Please load a path to save the log.")
