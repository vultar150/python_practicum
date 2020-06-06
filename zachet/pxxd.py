from tkinter import *
import os
import subprocess
import sys
from tkinter import filedialog as fd
from tkinter import messagebox as mb


def undo():
    try:
        text.edit_undo()
    except Exception as ex:
        mb.showinfo("Error", ex)

def redo():
    try:
        text.edit_redo()
    except Exception as ex:
        mb.showinfo("Error", ex)

def open_file():
    global open_name
    try:
        if not open_name:
            open_name = fd.askopenfilename()
        output = subprocess.check_output(["xxd", "-g1", open_name])
        text.delete(1.0, END)
        text.insert(1.0, output)
    except Exception as ex:
        mb.showinfo("Error", ex)


def save_text():
    global open_name, save_name
    try:
        s = text.get(1.0, END)
        f = open("tmp.txt", "w")
        f.write(s)
        f.close()
        output = subprocess.check_output(["xxd", "-r", "tmp.txt"])
        if save_name:
            f = open(save_name, "wb")
        else:
            f = open(open_name, "wb")
        f.write(output)
        f.close()
    except Exception as ex:
        mb.showinfo("Error", ex)


def save_text_as():
    global save_name
    try:
        save_name = fd.asksaveasfilename()
        s = text.get(1.0, END)
        f = open("tmp.txt", "w")
        f.write(s)
        f.close()
        output = subprocess.check_output(["xxd", "-r", "tmp.txt"])
        f = open(save_name, "wb")
        f.write(output)
        f.close()
    except Exception as ex:
        mb.showinfo("Error", ex)


root = Tk()

text = Text(width=80, height=40, undo=True)
text.grid(row=0, column=1, sticky="NEWS")
text.pack()

scroll = Scrollbar(command=text.yview)
scroll.pack(side=LEFT, fill=Y)

text.config(yscrollcommand=scroll.set)
 
frame = Frame()
frame.pack()

open_name, save_name = None, None

if len(sys.argv) == 2:
    open_name = sys.argv[1]
elif len(sys.argv) == 3:
    open_name = sys.argv[1]
    save_name = sys.argv[2]

b_open = Button(frame, text="Open", width=10, command=open_file)
b_open.grid(row=1, column=0, sticky='NEWS')

b_save = Button(frame, text="Save", width=10, command=save_text)
b_save.grid(row=1, column=1, sticky='NEWS')

b_save_as = Button(frame, text="Save as", width=10, command=save_text_as)
b_save_as.grid(row=1, column=2, sticky='NEWS')

b_undo = Button(frame, text="Undo", width=10, command=undo)
b_undo.grid(row=2, column=1, sticky='NEWS')

b_redo = Button(frame, text="Redo", width=10, command=redo)
b_redo.grid(row=2, column=2, sticky='NEWS')
 
root.mainloop()