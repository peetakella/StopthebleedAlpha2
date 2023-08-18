from tkinter import *

from time import sleep



print ("opened Opening_page_test")

root = Tk()
root.title("Better Bleeding Control")
root.configure(bg="grey75")
#root.attributes("-zoomed", True)  # Maximizes the window
#root.attributes("-fullscreen", True)  # substitute `Tk` for whatever your `Tk()` object is called

global largetitletext, mediumtitletext, mediumtext, smalltext
largetitletext = 80
mediumtitletext = 60
mediumtext = 30
smalltext = 25

    
#Add Title frame
frame1 = LabelFrame(root, padx=50, pady=10,fg="black", bg="gray75")
frame1.grid(row=0, column=0,columnspan=2,pady=20, padx=25)

# Add a label at the top of the window
label_home = Label(frame1, text="Hemorrhage Control Trainer", font=("Arial", largetitletext), fg="black", bg="gray75")
label_home.grid(row=0, column=0,  pady=20, padx=10)
# Add two buttons underneath the label of home page

button_scenario = Button(root, text="Choose \n Scenario", command = lambda: [open_scenario_window()], bg="firebrick3",fg="white",  font=("Arial", largetitletext))
button_scenario.grid(row=1, column=0)
button_retrieve = Button(root, text="Retrieve Data", command = lambda: [open_data_window()],bg="firebrick3",fg="white", font=("Arial", largetitletext))
button_retrieve.grid(row=1, column=1)

def open_scenario_window():
    sleep(10)
    #Add Title frame
    open_scenario_window = Toplevel(root)
    open_scenario_window.title("Data")
    open_scenario_window.geometry("1024x600")
    open_scenario_window.configure(bg="grey75")
    
    frame2 = LabelFrame(open_scenario_window, padx=50, pady=10,fg="black", bg="gray75")
    frame2.grid(row=0, column=0,columnspan=2,pady=20, padx=25)

    # Add a label at the top of the window
    label_home = Label(open_scenario_window, text="Hemorrhage Control Trainer", font=("Arial", largetitletext), fg="black", bg="gray75")
    label_home.grid(row=0, column=0,  pady=20, padx=10)
    # Add two buttons underneath the label of home page

    button_scenario = Button(open_scenario_window, text="Choose \n Scenario", command = lambda: [open_data_window()], bg="firebrick3",fg="white",  font=("Arial", largetitletext))
    button_scenario.grid(row=1, column=0)
    button_retrieve = Button(open_scenario_window, text="Retrieve Data", command = lambda: [open_data_window()],bg="firebrick3",fg="white", font=("Arial", largetitletext))
    button_retrieve.grid(row=1, column=1)
    

def open_data_window():
    sleep(10)
    #Add Title frame
    open_data_window = Toplevel(root)
    open_data_window.title("Data")
    open_data_window.geometry("1024x600")
    open_data_window.configure(bg="grey75")
    
    frame2 = LabelFrame(open_data_window, padx=50, pady=10,fg="black", bg="gray75")
    frame2.grid(row=0, column=0,columnspan=2,pady=20, padx=25)

    # Add a label at the top of the window
    label_home = Label(open_data_window, text="Hemorrhage Control Trainer", font=("Arial", largetitletext), fg="black", bg="gray75")
    label_home.grid(row=0, column=0,  pady=20, padx=10)
    # Add two buttons underneath the label of home page

    button_scenario = Button(open_data_window, text="Choose \n Scenario", command = lambda: [open_scenario_window()], bg="firebrick3",fg="white",  font=("Arial", largetitletext))
    button_scenario.grid(row=1, column=0)
    button_retrieve = Button(open_data_window, text="Retrieve Data", command = lambda: [open_scenario_window()],bg="firebrick3",fg="white", font=("Arial", largetitletext))
    button_retrieve.grid(row=1, column=1)
root.mainloop()    
