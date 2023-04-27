from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title('Large Image')
#root.iconbitmap('file for icon')

my_img1 = ImageTk.PhotoImage(Image.open("img1.png"))
my_img3 = ImageTk.PhotoImage(Image.open("img3.png"))
my_img4 = ImageTk.PhotoImage(Image.open("img4.png"))

image_list =[my_img1 , my_img3 , my_img4]
#image_list[0] calls from list starting from zero


img_number=0

my_label = Label(image=image_list[img_number])
my_label.grid(row=0, column=0, columnspan=3)


def forward(img_number):
    
    print (img_number)
    global my_label
    global button_back
    global button_next
    my_label.grid_forget()
    my_label = Label(image=image_list[img_number-1])
    my_label.grid(row=0, column=0, columnspan=3)
    
    if img_number == 2:
        button_next = Button(root, text="next", state=DISABLED)
        
    print (img_number)
    button_next = Button(root, text="next", command=lambda:forward(img_number + 1)).grid(row=1, column=2)
    button_back = Button(root, text="back", command=lambda:back(img_number - 1)).grid(row=1, column=0)
    
    print (img_number)
    if img_number == 2:
        button_next = Button(root, text="next", state=DISABLED)
    if img_number == 0:
        button_back = Button(root, text="back", state=DISABLED)
    
    return

def back(img_number):
    
    print (img_number)
    global my_label
    global button_back
    global button_next
    my_label.grid_forget()
    my_label = Label(image=image_list[img_number-2])
    
    print (img_number)
    button_next = Button(root, text="next", command=lambda:forward(img_number + 1)).grid(row=1, column=2)
    button_back = Button(root, text="back", command=lambda:back(img_number)).grid(row=1, column=0)
    my_label.grid(row=0, column=0, columnspan=3)

    return

button_back = Button(root, text="back", command=back, state=DISABLED).grid(row=1, column=0)
button_next = Button(root, text="next", command=lambda:forward(0)).grid(row=1, column=2)
quit_button = Button(root, text="Exit Program", command=root.destroy).grid(row=1, column=1)


root.mainloop()



