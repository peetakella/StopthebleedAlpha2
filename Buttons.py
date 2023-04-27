import tkinter as tk

# Create the main window
root = tk.Tk()

# Create a function to handle button 1 click
def open_window_1():
    # Create a new window
    window_1 = tk.Toplevel(root)
    window_1.title("Window 1")
    
    # Add a label and text box to the window
    label = tk.Label(window_1, text="Text Box 1:")
    label.pack()
    text_box = tk.Text(window_1)
    text_box.pack()

# Create a function to handle button 2 click
def open_window_2():
    # Create a new window
    window_2 = tk.Toplevel(root)
    window_2.title("Window 2")
    
    # Add two buttons to the window
    button_a = tk.Button(window_2, text="Button A")
    button_a.pack()
    button_b = tk.Button(window_2, text="Button B")
    button_b.pack()



# Add two buttons to the main window
button_1 = tk.Button(root, text="Button 1", command=open_window_1)
button_1.pack()
button_2 = tk.Button(root, text="Button 2", command=open_window_2)
button_2.pack()

# Start the main event loop
root.mainloop()
