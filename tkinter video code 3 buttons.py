from tkinter import *

root = Tk()

#button name = function(location, "text")
myButton1 = Button(root, text="Click me")
myButton2 = Button(root, text="Click me")
myButton3 = Button(root, text="Click me")
myButton4 = Button(root, text="Click me")
myButton5 = Button(root, text="Click me")
myButton6 = Button(root, text="Click me")
myButton1.grid(row=0, column=0)
myButton2.grid(row=1, column=0)
myButton3.grid(row=1, column=1)
myButton4.grid(row=2, column=0)
myButton5.grid(row=2, column=1)
myButton6.grid(row=2, column=2)



root.mainloop()