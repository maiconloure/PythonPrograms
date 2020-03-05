from tkinter import *
from time import strftime

win = Tk()
win.title("Digital Clock")
win.geometry("350x200")


def digital_clock():
    time1 = strftime("%H:%M:%S")
    current_time.config(text=time1)
    current_time.after(250, digital_clock)


digi_clock = Label(win, text="Digital Clock", font=("arial", 20, "bold"))
digi_clock.grid(row=0, column=0)

current_time = Label(win, font=("times new roman", 35, "bold"), bg="red")
current_time.grid(row=1, column=0, padx=80, pady=50)
digital_clock()

win.mainloop()
