from tkinter import *

# Create a new tkinter window
root = Tk()
root.title("Better Bleeding Control")

# Create a top frame that fills 1/3 of the screen
top_frame = tk.Frame(root, width=1000, height=333)
top_frame.grid(row=0, column=0, columnspan=2)

# Add a label to the top frame
label1 = tk.Label(top_frame, text="Better Bleeding Control", font=("Arial Bold", 30))
label1.place(relx=0.5, rely=0.5, anchor="center")

# Create a bottom frame
bottom_frame = tk.Frame(window, width=1000, height=667)
bottom_frame.grid(row=1, column=0, columnspan=2)



# Function to open a new window when button1 is clicked
def choose_scenario():
    scenario_window = tk.Toplevel(window)
    scenario_window.title("Choose Scenario")

    # Add a title bar to the scenario window
    title_bar = tk.Frame(scenario_window, width=1000, height=250, bg="#5c5c5c")
    title_bar.grid(row=0, column=0, columnspan=3)

    # Add a label to the title bar
    label = tk.Label(title_bar, text="Choose Scenario", font=("Arial Bold", 20), fg="white", bg="#5c5c5c")
    label.place(relx=0.5, rely=0.5, anchor="center")

    # Add a left section with a label and 3 checkboxes
    left_frame = tk.Frame(scenario_window, width=333, height=417)
    left_frame.grid(row=1, column=0)

    label2 = tk.Label(left_frame, text="Wound Choice")
    label2.place(relx=0.5, rely=0.1, anchor="center")

    JW = tk.IntVar()
    AW = tk.IntVar()
    BOH = tk.IntVar()

    checkbox1 = tk.Checkbutton(left_frame, text="Junction Wound", variable=JW)
    checkbox1.place(relx=0.5, rely=0.3, anchor="center")

    checkbox2 = tk.Checkbutton(left_frame, text="Arm Wound", variable=AW)
    checkbox2.place(relx=0.5, rely=0.5, anchor="center")

    checkbox3 = tk.Checkbutton(left_frame, text="Blown Off Hand", variable=BOH)
    checkbox3.place(relx=0.5, rely=0.7, anchor="center")

    # Add a middle section with a label and a toggle switch
    middle_frame = tk.Frame(scenario_window, width=333, height=417)
    middle_frame.grid(row=1, column=1)

    label3 = tk.Label(middle_frame, text="Sound")
    label3.place(relx=0.5, rely=0.1, anchor="center")

    sound = tk.IntVar()

    toggle_switch = tk.Checkbutton(middle_frame, text="On/Off", variable=sound, onvalue=1, offvalue=0)
    toggle_switch.place(relx=0.5, rely=0.1, anchor="center")
    
# Add two buttons to the bottom frame
button1 = tk.Button(bottom_frame, text="Choose Scenario", width=20, height=5, command=choose_scenario)
button1.grid(row=0, column=0)

button2 = tk.Button(bottom_frame, text="Retrieve Data", width=20, height=5)
button2.grid(row=0, column=1)
