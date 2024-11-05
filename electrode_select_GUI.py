import tkinter as tk

class GridSelector:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        self.grid_size = 16
        self.buttons = []
        self.selected_cells = set()
        
        self.master.title("Grid Selector")
        
        # Create grid of buttons
        for i in range(self.grid_size):
            row_buttons = []
            for j in range(self.grid_size):
                btn = tk.Button(master, bg="gray", width=2, height=1, command=lambda i=i, j=j: self.toggle_button(i, j))
                btn.grid(row=i+1, column=j+1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
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
        
    def toggle_button(self, i, j):
        btn = self.buttons[i][j]
        if btn["bg"] == "gray":
            btn["bg"] = "blue"
            self.selected_cells.add((i, j))
        else:
            btn["bg"] = "gray"
            self.selected_cells.discard((i, j))
    
    def select_row(self, i):
        for j in range(self.grid_size):
            self.toggle_button(i, j)
    
    def select_column(self, j):
        for i in range(self.grid_size):
            self.toggle_button(i, j)
    
    def confirm_selection(self):
        selected_numbers = [(i * self.grid_size + j + 1) for j, i in self.selected_cells]
        self.selected_cells = selected_numbers
        self.master.destroy()
        self.callback(selected_numbers)
