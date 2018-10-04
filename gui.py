#!/usr/bin/python3
#-*- coding: UTF-8 -*-

import tkinter
import tkinter.ttk

root = tkinter.Tk()
paramVar = tkinter.IntVar()

openFileBtn = tkinter.Button(root, text='Open file')

# parameter widget frame
paramFrame = tkinter.Frame(root)
paramLabel = tkinter.Label(paramFrame, text='Parameters')

# parameter radiogroup
paramRadiobtnSpline = tkinter.Radiobutton(paramFrame, text='Spline', variable=paramVar, value=1)
paramRadiobtnBezier = tkinter.Radiobutton(paramFrame, text='Bezier', variable=paramVar, value=2)
paramRadiobtnBSpl = tkinter.Radiobutton(paramFrame, text='B-Spline', variable=paramVar, value=3)
paramVar.set(1)
paramComputeBtn = tkinter.Button(paramFrame, text='Calculate')

# calculated values table's frame
tableFrame = tkinter.Frame(root)
tableTree = tkinter.ttk.Treeview(tableFrame, columns=('value'))
tableTree.heading('value', text='Y')
tableAddBtn = tkinter.Button(tableFrame, text='Add value')

# pack into grid()
openFileBtn.grid(row=0, rowspan=1, column=0, columnspan=1)
paramFrame.grid(row=1, rowspan=5, column=0, columnspan=2)
tableFrame.grid(row=6, rowspan=5, column=0, columnspan=2)

# pack into frame paramFrame's widgets
paramLabel.grid(row=0, column=0)
paramRadiobtnSpline.grid(row=1, column=0)
paramRadiobtnBezier.grid(row=2, column=0)
paramRadiobtnBSpl.grid(row=3, column=0)
paramComputeBtn.grid(row=4, column=0)

# pack into frame table's widgets
tableTree.grid(row=0, rowspan=4, column=0, columnspan=2)
tableAddBtn.grid(row=5, rowspan=1, column=0, columnspan=1)

root.mainloop()
