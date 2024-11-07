from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget
import sys
import pyqtgraph as pg
import numpy as np

# Define the main window class
class PyQtWindow(QMainWindow):
    def __init__(self, stim_time, activity_mat, stim_electrode):
        super().__init__()
        self.stim_time = stim_time  # Stimulation time
        self.activity_mat = activity_mat  # Activity matrix
        self.stim_electrode = stim_electrode  # List of stimulation electrodes
        self.selected_squares = set()  # Set to keep track of selected squares
        self.initUI()  # Initialize the UI

    def initUI(self):
        self.setWindowTitle("Single stimulation")  # Set window title
        self.setGeometry(100, 100, 1000, 800)  # Set window size and position

        # Create and configure the plot widget
        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setGeometry(300, 50, 650, 700)  # Set plot widget size and position
        self.plot_widget.setBackground('w')  # Set background to white
        self.plot_widget.showAxis('left', show=False)  # Hide the y-axis
        self.plot_widget.addLine(x=self.stim_time/30000, pen=pg.mkPen('r', width=2))  # Add a red line at stim_time

        # Create and configure the clear button
        self.clear_button = QPushButton('Clear', self)
        self.clear_button.setGeometry(50, 750, 100, 30)  # Set button size and position
        self.clear_button.clicked.connect(self.clear_plot)  # Connect button to clear_plot method

        # Create and configure the close button
        self.close_button = QPushButton('Close', self)
        self.close_button.setGeometry(200, 750, 100, 30)  # Set button size and position
        self.close_button.clicked.connect(self.close)  # Connect button to close method

        # Create and configure the grid layout
        self.grid_layout = QGridLayout()
        self.grid_widget = QWidget(self)
        self.grid_widget.setGeometry(50, 50, 200, 200)  # Set grid widget size and position
        self.grid_widget.setLayout(self.grid_layout)

        # Create buttons for the grid
        for i in range(16):
            for j in range(16):
                btn = QPushButton('', self)
                btn.setFixedSize(20, 20)  # Set button size
                btn.setStyleSheet("background-color: white; border: 1px solid black")  # Set button color to white and add black border
                btn.clicked.connect(self.make_toggle_callback(j * 16 + i + 1, btn))  # Connect button to toggle callback
                self.grid_layout.addWidget(btn, i, j)  # Add button to grid layout

        self.grid_layout.setHorizontalSpacing(10)  # Set horizontal spacing between buttons
        self.grid_layout.setVerticalSpacing(10)  # Set vertical spacing between buttons

        # Highlight stimulation electrodes in red
        for electrode in self.stim_electrode:
            row = (electrode - 1) % 16  # Calculate row
            col = (electrode - 1) // 16  # Calculate column
            button = self.grid_layout.itemAtPosition(row, col).widget()
            button.setStyleSheet("background-color: red; border: 1px solid black")  # Set color to red
            button.setEnabled(False)  # Make button inactive

    # Create a callback function for toggling button state
    def make_toggle_callback(self, index, button):
        def toggle():
            if index in self.selected_squares:
                self.selected_squares.remove(index)  # Remove index from selected squares
                button.setStyleSheet("background-color: white; border: 1px solid black")  # Set button color to white
                self.remove_trace(index)  # Remove trace from plot
            else:
                self.selected_squares.add(index)  # Add index to selected squares
                self.plot_widget.clear()  # Clear the plot
                self.plot_widget.addLine(x=self.stim_time/30000, pen=pg.mkPen('r', width=2))  # Add red line at stim_time
                sorted_squares = sorted(self.selected_squares)  # Sort selected squares
                button.setStyleSheet("background-color: green; border: 1px solid black")  # Set button color to green
                self.count = 0
                for idx in sorted_squares:
                    self.add_trace(idx)  # Add trace to plot
                    self.count += 1
        return toggle

    # Add a trace to the plot
    def add_trace(self, index):
        trace = self.activity_mat[index - 1]  # Get trace data
        offset = self.count * 5  # Calculate offset
        time_vector = np.linspace(0,len(trace),len(trace))/30000 # Create time vector
        self.plot_widget.plot(time_vector,trace + offset, pen=pg.mkPen('b', width=1))  # Plot trace with offset

    # Remove a trace from the plot
    def remove_trace(self, index):
        self.plot_widget.clear()  # Clear the plot
        self.plot_widget.addLine(x=self.stim_time/30000, pen=pg.mkPen('r', width=2))  # Add red line at stim_time
        self.selected_squares.discard(index)  # Remove the index from selected squares
        selected_squares_copy = sorted(self.selected_squares)  # Create a copy of selected squares
        self.selected_squares.clear()  # Clear selected squares
        self.count = 0
        for idx in selected_squares_copy:
            self.selected_squares.add(idx)  # Re-add selected squares to update the plot
            self.add_trace(idx)  # Re-add traces for remaining selected squares
            self.count += 1

    # Clear the plot and reset button states
    def clear_plot(self):
        self.plot_widget.clear()  # Clear the plot
        self.plot_widget.addLine(x=self.stim_time, pen=pg.mkPen('r', width=2))  # Add red line at stim_time
        self.selected_squares.clear()  # Clear selected squares
        for i in range(16):
            for j in range(16):
                btn = self.grid_layout.itemAtPosition(i, j).widget()
                if btn.styleSheet() == "background-color: green; border: 1px solid black":
                    btn.setStyleSheet("background-color: white; border: 1px solid black")  # Reset button color to white

# Function to run the PyQt application
def run_pyqt_app(stim_time, activity_mat, stim_electrode):
    app = QApplication.instance()  # Check if QApplication already exists
    if not app:  # If no instance exists, create a new one
        app = QApplication(sys.argv)
    window = PyQtWindow(stim_time, activity_mat, stim_electrode)  # Create main window
    window.show()  # Show main window
    app.exec_()  # Execute application
