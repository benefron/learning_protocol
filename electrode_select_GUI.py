import tkinter as tk
import threading
from Check_stim_GUI import run_pyqt_app
from SimulatedTrace import *

class GridSelector:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        self.grid_size = 16
        self.buttons = []
        self.selected_cells = set()
        
        self.master.title("Grid Selector")
        
        # Create grid of labels
        for i in range(self.grid_size):
            row_labels = []
            for j in range(self.grid_size):
                lbl = tk.Label(master, bg="gray", width=2, height=1)
                lbl.grid(row=i+1, column=j+1)
                lbl.bind("<Button-1>", lambda e, i=i, j=j: self.toggle_label(i, j))
                row_labels.append(lbl)
            self.buttons.append(row_labels)

        
        # Create row selection buttons
        for i in range(self.grid_size):
            btn = tk.Button(master, text=f"Row {i+1}", command=lambda i=i: self.select_row(i))
            btn.grid(row=i+1, column=0)
        
        # Create column selection buttons
        for j in range(self.grid_size):
            btn = tk.Button(master, text=f"Col {j+1}", command=lambda j=j: self.select_column(j))
            btn.grid(row=0, column=j+1)
        
        # Create confirmation button
        confirm_btn = tk.Button(master, text="Confirm", command=self.confirm_selection)
        confirm_btn.grid(row=self.grid_size+1, columnspan=self.grid_size+2)
        
        # create single stimulation window
        stim_button = tk.Button(master, text="Single Stimulation", command=self.single_stimulation)
        stim_button.grid(row=self.grid_size+2, columnspan=self.grid_size+2)
        
    def toggle_label(self, i, j):
        lbl = self.buttons[i][j]
        current_color = lbl.cget("bg")
        new_color = "red" if current_color == "gray" else "gray"
        lbl.configure(bg=new_color)
        if new_color == "red":
            self.selected_cells.add((i, j))
        else:
            self.selected_cells.discard((i, j))
    
    def select_row(self, i):
        for j in range(self.grid_size):
            self.toggle_label(i, j)
    
    def select_column(self, j):
        for i in range(self.grid_size):
            self.toggle_label(i, j)
    
    def confirm_selection(self):
        selected_numbers = [(i * self.grid_size + j + 1) for j, i in self.selected_cells]
        self.selected_cells = selected_numbers
        self.master.destroy()
        self.callback(selected_numbers)
        
    def single_stimulation(self):
        selected_numbers = [(i * self.grid_size + j + 1) for j, i in self.selected_cells]
        matrix = vector_to_matrix(256)
        run_pyqt_app(600, matrix ,selected_numbers)
    
    
