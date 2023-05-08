from tkinter import *
from time import sleep
# Create the main window
root = Tk()
root.title("Better Bleeding Control")
root.geometry("1024x600")

# Add a label at the top of the window
label_home = Label(root, text="Better Bleeding Control", font=("Arial", 30))
label_home.grid(row=0, column=0, columnspan=2, pady=50)

def open_data_window():
    data_window = Toplevel(root)
    data_window.title("Data")
    data_window.geometry("1024x600")

    # Add a label at the top of the window
    label_scenario = Label(data_window, text="View Data", font=("Arial", 30))
    label_scenario.grid(row=0, column=0, columnspan=3, pady=50)

# Create a function to open the scenario window
def open_scenario_window():
    # Create the scenario window
    scenario_window = Toplevel(root)
    scenario_window.title("Choose Scenario")
    scenario_window.geometry("1024x600")

    # Add a label at the top of the window
    label_scenario = Label(scenario_window, text="Choose Scenario", font=("Arial", 30))
    label_scenario.grid(row=0, column=0, columnspan=3, pady=35)

    #Add left frame
    frameL = LabelFrame(scenario_window, text= "this is my frame", padx=50, pady=5)
    frameL.grid(row=1, column=0,padx=50,pady=25)
    
    
    #Add Middle frame
    frameM = LabelFrame(scenario_window, text= "this is my frame", padx=50, pady=5)
    frameM.grid(row=1, column=1,padx=0,pady=25)    
    
    
    #Add Right Frame
    frameR = LabelFrame(scenario_window, text= "this is my frame", padx=50, pady=5)
    frameR.grid(row=1, column=2,padx=50,pady=25)



    # Add the left section with wound choice checkboxes
    label_wound_choice = Label(frameL, text="Wound Choice", font=("Arial", 20))
    label_wound_choice.grid(row=0, column=0, pady=50)

    # Add the checkboxes for wound choice
    WP = IntVar()
    TQ = IntVar()
    DP = IntVar()

    checkbox_junction = Checkbutton(frameL, text="Wound Packing", variable=WP)
    checkbox_junction.grid(row=1, column=0)

    checkbox_arm = Checkbutton(frameL, text="Tourniquet", variable=TQ)
    checkbox_arm.grid(row=2, column=0)

    checkbox_hand = Checkbutton(frameL, text="Direct Pressure", variable=DP)
    checkbox_hand.grid(row=3, column=0)

    # Add the middle section with sound toggle switch
    label_sound = Label(frameM, text="Sound", font=("Arial", 20))
    label_sound.grid(row=0, column=0, pady=25)

    # Add the sound toggle switch
    sound = IntVar()

    toggle_switch = Checkbutton(frameM, text="On/Off", variable=sound, onvalue=1, offvalue=0)
    toggle_switch.grid(row=1, column=0)

     # Add the middle section with liquid toggle switch
    label_liquid = Label(frameM, text="liquid", font=("Arial", 20))
    label_liquid.grid(row=2, column=0, pady=25)

    # Add the liquid toggle switch
    liquid = IntVar()

    toggle_switch = Checkbutton(frameM, text="On/Off", variable=liquid, onvalue=1, offvalue=0)
    toggle_switch.grid(row=3, column=0)

    # Add the right section with bleed out time checkboxes
    label_bleed_out = Label(frameR, text="Bleed out time", font=("Arial", 20))
    label_bleed_out.grid(row=0, column=0, pady=15)

    # Add the checkboxes for bleed out time
    speed = IntVar()

    checkbox_2_30 = Radiobutton(frameR, text="2:30", variable=speed, value=1)
    checkbox_2_30.grid(row=1, column=0)

    checkbox_3_00 = Radiobutton(frameR, text="3:00", variable=speed, value=2)
    checkbox_3_00.grid(row=2, column=0)

    checkbox_3_30 = Radiobutton(frameR, text="2:30", variable=speed, value=3)
    checkbox_3_30.grid(row=3, column=0)

    checkbox_4_00 = Radiobutton(frameR, text="3:00", variable=speed, value=4)
    checkbox_4_00.grid(row=4, column=0)

    checkbox_4_30 = Radiobutton(frameR, text="2:30", variable=speed, value=5)
    checkbox_4_30.grid(row=5, column=0)

    checkbox_5_00 = Radiobutton(frameR, text="3:00", variable=speed, value=6)
    checkbox_5_00.grid(row=6, column=0)
    
    print ('Wound Pack', WP.get())
    print ('Tourniquet', TQ.get())
    print ('Direct Pressure', DP.get())
    print ('Sound', sound.get())
    print ('liquid', liquid.get())
    print ('Speed', speed.get())
    
    #add function for enter button into the scenereo
    def open_sim_window():
        sim_window = Toplevel(scenario_window)
        sim_window.title("Choose Scenario")
        sim_window.geometry("1024x600")
        sleep(.5)
        
        print ('Wound Pack', WP.get())
        print ('Tourniquet', TQ.get())
        print ('Direct Pressure', DP.get())
        print ('Sound', sound.get())
        print ('liquid', liquid.get())
        print ('Speed', speed.get())

        # Add a label at the top of the window
        label_scenario = Label(sim_window, text="simulation", font=("Arial", 30))
        label_scenario.grid(row=0, column=0, columnspan=3, pady=50)
        
        #
        #
        #code for controlling motors and solenoids based on pressure goes here
        #code foe displaying data in a graph goes here
        #
        #
    # Add a button to the scenereo window to begin
    
    
    button_scenario = Button(scenario_window, text="Begin", command=open_sim_window,  font=("Arial", 20))
    button_scenario.grid(row=2, column=1, padx=50, pady=5)
    
    
# Add two buttons underneath the label of home page
button_scenario = Button(root, text="Choose Scenario", command=open_scenario_window,  font=("Arial", 20))
button_scenario.grid(row=1, column=0, padx=50, pady=50)

button_retrieve = Button(root, text="Retrieve Data", command=open_data_window, font=("Arial", 20))
button_retrieve.grid(row=1, column=1, padx=50, pady=50)


root.mainloop()
