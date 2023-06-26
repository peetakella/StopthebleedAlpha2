from tkinter import *

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
# Implement the default Matplotlib key bindings.
from matplotlib.figure import Figure
from time import sleep
import numpy as np

x=0
root = Tk()
root.wm_title("Embedding in Tk")

#Add Title frame
while x<100:
    frame1 = LabelFrame(root, padx=50, pady=10,fg="black", bg="gray75")
    frame1.grid(row=0, column=0,columnspan=2,pady=20, padx=25)

    label_home = Label(frame1, text="Hemorrhage Control Trainer", font=("Arial", 50), fg="black", bg="gray75")
    label_home.grid(row=0, column=0,  pady=20, padx=10)

    sleep(1)
    plt = Figure()
    t=[]
    t = x
    m=[]
    m= 2 * np.sin(2 * np.pi * t)
    plt.add_subplot(111).plot(t, m)


    canvas = FigureCanvasTkAgg(plt, master=frame1)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(row=1,column=1)

    x+=1
mainloop()
