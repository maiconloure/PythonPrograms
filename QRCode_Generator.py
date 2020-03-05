import tkinter as tk
import pyqrcode

win = tk.Tk()
win.title("QR CODE Generator")


def generator():
    url = entry.get()
    qr = pyqrcode.create(url)
    save = qr.svg('myqrcode.svg', scale=12)


label1 = tk.Label(win, text='Enter URL')
label1.grid(row=0, column=0)

entry = tk.Entry(win)
entry.grid(row=1, column=0)

button = tk.Button(win, text='Generate', command=generator())
button.grid(row=3, column=0)

win.mainloop()