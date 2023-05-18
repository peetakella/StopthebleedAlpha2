import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time


def graph_data():
    root = tk.Tk()
    root.title("Real-time Data Graph")
    
    # Create a Figure object and add an Axes object to it
    fig = plt.Figure()
    ax = fig.add_subplot(1, 1, 1)
    
    # Create an empty line object for plotting the data
    line, = ax.plot([], [], '-o')
    
    # Configure the Axes object
    ax.set_xlim(0, 1000)  # Initial x-axis limits
    ax.set_ylim(0, 1000000)  # Initial y-axis limits
    
    # Create a Tkinter canvas for displaying the graph
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def update_graph():
        # Generate sample data
        x = np.arange(1, 1001)
        y = (x*x)
        
        # Update the data for the line object
        line.set_data(x, y)
        
        # Auto scale the graph based on the data range
        ax.relim()
        ax.autoscale_view()
        
        # Redraw the graph
        canvas.draw()
        
        # Schedule the next update
        root.after(500000, update_graph)  # Update every 0.05 seconds (50 milliseconds)
    
    # Start the initial graph update
    update_graph()
    
    # Run the Tkinter event loop
    root.mainloop()


# Call the function to start the graphing application
graph_data()