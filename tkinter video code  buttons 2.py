from tkinter import *

root = Tk()

def myClick():
    myLabel = Label(root, text="Look I clicked button 2")
    myLabel.pack()

myButton1 = Button(root, text="Click me", state=DISABLED, padx=50, pady=10, bg="#000000")#pad changes size around text bg changes background color 
myButton2 = Button(root, text="Click me 2", command=myClick, fg="blue", bg="red")#note no () after myClick because it will run myClick automatically when the program is run and not when clicked

myButton1.pack()
myButton2.pack()
#myButton1.grid(row=0, column=0)
#myButton2.grid(row=1, column=0)



root.mainloop()