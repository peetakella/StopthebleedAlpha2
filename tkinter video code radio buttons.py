from tkinter import *

root = Tk()
root.title('radio')

#r = IntVar() #integer variable, allows it to keep track of changes over time. Call x.get to find current value
# x=StringVar() string variable can be passed. but you need to have it in parintahsis when you do so under value = "string"
#r.set("2")

TOPPINGS = [
    ("Pep","pep"),
    ("Cheese","cheese"),
    ("Pineapple","pineapple"),
    ("Green Chili","green chili")
    ]

pizza = StringVar()
pizza.set("Pep")

for text, topping in TOPPINGS:
    Radiobutton(root, text=text, variable=pizza, value=topping).pack(anchor=W)


def clicked(value):
    myLabel = Label(root, text= value).pack(anchor=E)
    
  
    
#one way to do it
#Radiobutton(root, text="option 1", variable=r, value=1, command=lambda:clicked(r.get())).pack()
#Radiobutton(root, text="option 2", variable=r, value=2, command=lambda:clicked(r.get())).pack()
#Radiobutton(root, text="option 3", variable=r, value=3, command=lambda:clicked(r.get())).pack()
#Radiobutton(root, text="option 4", variable=r, value=4, command=lambda:clicked(r.get())).pack()
my_button=Button(root, text="enter", command=lambda:clicked(pizza.get()))
my_button.pack()
root.mainloop()