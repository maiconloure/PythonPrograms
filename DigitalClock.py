from tkinter import Label
from time import strftime

clock = Label()

clock.pack()
clock['font'] = 'Helvetica 120 bold'
clock['text'] = strftime('%H:%M:%S')

def tictac():
    now = strftime('%H:%M:%S')
    if now != clock['text']:
        clock['text'] = now
    clock.after(100, tictac)

tictac()
clock.mainloop()
