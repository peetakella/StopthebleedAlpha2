from tkinter import *

# Create the main window
root = Tk()
root.title("Better Bleeding Control")
#root.geometry("1000x1000")

# Add a label at the top of the window
label_home = Label(root, text="Better Bleeding Control", font=("Arial", 30))
label_home.grid(row=0, column=0, columnspan=2, pady=50)

# Add two buttons underneath the label
button_scenario = Button(root, text="Choose Scenario", font=("Arial", 20))
button_scenario.grid(row=1, column=0, padx=50, pady=50)

button_retrieve = Button(root, text="Retrieve Data", font=("Arial", 20))
button_retrieve.grid(row=1, column=1, padx=50, pady=50)

root.mainloop()