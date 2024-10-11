import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import queue
import os
from Experimnt_control import ExperimentControl
import yaml

class ExperimentGUI:
    def __init__(self, root ):
        self.root = root
        self.root.title("Experiment GUI")
        self.chip_number = ''
        self.chosen_electrode = ''

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
        self.yaml_basline = tk.StringVar(value="")
        self.yaml_recording = tk.StringVar(value="")

        # Create input fields
        self.create_input_fields()

        # Create buttons
        self.create_buttons()

        #create a chip number label
        self.chip_number_label = tk.Label(self.right_frame, text=f"Chip Number: {self.chip_number}")
        self.chip_number_label.pack(anchor='w')
        self.electorde_label = tk.Label(self.right_frame, text=f"Target Elctrode: {self.chosen_electrode}")
        self.electorde_label.pack(anchor='w')

        # Create clock label
        #self.clock_header = tk.Label(self.right_frame, text="Elapsed Time:")
        #self.clock_header.pack(pady=10)
        self.clock_label = tk.Label(self.right_frame, text="Elapsed Time: 00:00:00")
        self.clock_label.pack(pady=10)
        self.clock_label.pack(anchor='w')

        # Create message area
        self.message_area = tk.Text(self.bottom_frame, height=10, state='disabled')
        self.message_area.pack(fill=tk.BOTH, expand=True)

        # Queue for thread-safe logging
        self.log_queue = queue.Queue()

        # Variable to control experiment run and clock update
        self.stop_event = threading.Event()
        self.running = False
        self.experiment_thread = None

        self.experiment = ExperimentControl(self)
        self.chip_number = self.experiment.chip_number
        self.chip_number_label.config(text=f"Target Elctrode: {self.chip_number}")
        self.experiment.get_comm()

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
        self.load_path_button_storage.pack(pady=5)

        self.open_yaml_button = tk.Button(self.right_frame, text="Open Configurations", command=self.open_yaml_file)
        self.open_yaml_button.pack(pady=5)
        self.open_yaml_button.config(state='disabled')

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
            self.stop_button.config(state='normal')
            self.stop_event.clear()
            self.running = True
            prefix = self.chip_number  # You can change this prefix later
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
            # pop up window to ask user to "Please make sure that the defult path in SparrowApp is set to the streaming path: {exp_path_streaming} and ask for confirmation to start the experiment"
            messagebox.showinfo("Information", f"Please make sure that the defult path in SparrowApp is set to the streaming path: {exp_path_streaming} and press OK to start the experiment")
            
            # Start the experiment in a separate thread
            self.update_parameters_experiment()
            self.experiment_thread = threading.Thread(target=self.run_experiment)
            self.experiment_thread.start()
            # Start the clock in a separate thread
            threading.Thread(target=self.update_clock).start()

        else:
            messagebox.showwarning("Warning", "Please load a streaming path before starting the experiment.")

    def stop_experiment(self): 
        self.stop_event.set() 
        self.running = False
        
        #if self.experiment_thread is not None:
          #  self.experiment_thread.join()  # Ensure the thread has completed
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
        # Copy YAML files to the storage path
        repo_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        baseline_cfg_path = os.path.join(repo_dir, "Baseline_cfg.yaml")
        recording_cfg_path = os.path.join(repo_dir, "Recording_cfg.yaml")

        if os.path.exists(baseline_cfg_path) and os.path.exists(recording_cfg_path):
            try:
                # Copy Baseline_cfg.yaml
                with open(baseline_cfg_path, 'r') as baseline_file:
                    baseline_content = baseline_file.read()
                with open(os.path.join(self.path_save.get(), "Baseline_cfg.yaml"), 'w') as baseline_file_copy:
                    baseline_file_copy.write(baseline_content)
                self.log_message("Baseline_cfg.yaml copied successfully.")
                self.yaml_basline.set(os.path.join(self.path_save.get(), "Baseline_cfg.yaml"))

                # Copy Recording_cfg.yaml
                with open(recording_cfg_path, 'r') as recording_file:
                    recording_content = recording_file.read()
                with open(os.path.join(self.path_save.get(), "Recording_cfg.yaml"), 'w') as recording_file_copy:
                    recording_file_copy.write(recording_content)
                self.log_message("Recording_cfg.yaml copied successfully.")
                self.yaml_recording.set(os.path.join(self.path_save.get(), "Recording_cfg.yaml"))
            except Exception as e:
                self.log_message(f"Failed to copy YAML files: {e}")
        else:
            self.log_message("YAML files not found in the repository directory.")
        self.open_yaml_button.config(state='normal')

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

    # Define here the main protocol running the experiemnt
    def run_experiment(self):
        
        time.sleep(1)
        while not self.stop_event.is_set():
            # run baseline function
            self.log_message("Running baseline recording")
            baseline_thread = threading.Thread(target=self.experiment.run_basleine(self.stop_event))
            baseline_thread.start()
            baseline_thread.join()  # Wait until the baseline thread finishes
            
            # check if experiment was stopped
            if self.stop_event.is_set():
                break
            self.log_message("Baseline recording completed")
            
            # Run stimulation protocol to choose target electrode below R/S criterion
            self.log_message("Determining target electrode")
            #target_electrode, message = ec.run_stimulation(self)
            #self.electorde_label.config(text=f"Target Elctrode: {target_electrode}")
            #self.target_electrode.set(target_electrode)
            #self.log_message(message)
            
            #check if experiment was stopped
            if self.stop_event.is_set():
                break
            
            # save file with parameters of experiment
            self.save_parameters()
            time.sleep(5) 
            self.log_message("Experiment completed")
            self.stop_experiment()
            time.sleep(10)
        #self.log_message("Experiment stopped")
        
        #time.sleep(10)




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
            "streaming path": self.exp_path_streaming.get(),
            "storage path": self.exp_path_storage.get(),
            "chip number": self.chip_number,

        }
    
    def dest_status(self):
        return self.running.get()
    
    def save_parameters(self):
        """Save the current parameters to a exp_parameters.txt file in the specified storage path."""
        if self.exp_path_storage.get():
            parameters = self.get_parameters()
            parameters_file_path = os.path.join(self.exp_path_storage.get(), "exp_parameters.txt")

            try:
                with open(parameters_file_path, 'w') as parameters_file:
                    for key, value in parameters.items():
                        parameters_file.write(f"{key}: {value}\n")
                self.log_message(f"Parameters saved successfully at {parameters_file_path}")
            except Exception as e:
                self.log_message(f"Failed to save parameters: {e}")
        else:
            self.log_message("No storage path specified. Please load a path to save the parameters.")

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

    def open_yaml_file(self):
        initial_dir = self.path_save.get() if self.path_save.get() else os.getcwd()
        file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("YAML files", "*.yaml")])
        if file_path:
            self.current_yaml_file_path = file_path
            with open(file_path, 'r') as file:
                yaml_content = yaml.safe_load(file)
                self.show_yaml_editor(yaml.dump(yaml_content))

    def save_yaml_file(self):
        if hasattr(self, 'yaml_editor'):
            yaml_content = self.yaml_editor_text.get(1.0, tk.END)
            with open(self.current_yaml_file_path, 'w') as file:
                yaml.safe_dump(yaml.safe_load(yaml_content), file)
            self.log_message(f"YAML file saved successfully at {self.current_yaml_file_path}")
            self.yaml_editor.destroy()

    def show_yaml_editor(self, content):
        self.yaml_editor = tk.Toplevel(self.root)
        self.yaml_editor.title("YAML Editor")
        self.yaml_editor_text = tk.Text(self.yaml_editor, height=20, width=50)
        self.yaml_editor_text.pack(padx=10, pady=10)
        self.yaml_editor_text.insert(tk.END, content)
        save_button = tk.Button(self.yaml_editor, text="Save", command=self.save_yaml_file)
        save_button.pack(padx=10, pady=5)

    def update_parameters_experiment(self):
        self.experiment.GUI.exp_path_storage.set(self.exp_path_storage.get())
        self.experiment.GUI.exp_path_streaming.set(self.exp_path_streaming.get())
        self.experiment.GUI.yaml_basline.set(self.yaml_basline.get())
        self.experiment.GUI.yaml_recording.set(self.yaml_recording.get())
        self.experiment.GUI.well_number.set(self.well_number.get())
        self.experiment.GUI.max_time.set(self.max_time.get())
        self.experiment.GUI.rest_time.set(self.rest_time.get())
        self.experiment.GUI.criterion.set(self.criterion.get())
        self.experiment.GUI.simulating_electrode.set(self.simulating_electrode.get())
        self.experiment.GUI.experiment_type.set(self.experiment_type.get())
        self.log_message("Parameters updated successfully.")
