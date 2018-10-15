#!/usr/bin/python3
#-*- coding: UTF-8 -*-

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib import style

style.use("ggplot")

import tkinter
import tkinter.filedialog
import tkinter.ttk

import csv
import numpy as np
from interp.spline import Spline
from interp.bspline import CubicBSpline
from interp.bezier import Bezier


class Preferences(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master=master)
        self.paramVar = tkinter.IntVar(master=master)

        self.leftFrame = tkinter.Frame(master)
        self.rightFrame = tkinter.Frame(master)
        self.openFileBtn = tkinter.Button(self.leftFrame, text='Открыть файл', command=self.load_file)
        self.fileLabel = tkinter.Label(self.leftFrame, text='Файл не загружен', wraplength=300)

        # parameter widget frame
        self.paramFrame = tkinter.Frame(self.leftFrame)
        self.paramLabel = tkinter.Label(self.paramFrame, text='Параметры')
        # parameter radiogroup
        self.paramRadiobtnSpline = tkinter.Radiobutton(
            self.paramFrame, text='Куб. сплайн', variable=self.paramVar, value=1)
        self.paramRadiobtnBezier = tkinter.Radiobutton(
            self.paramFrame, text='Кривые Безье', variable=self.paramVar, value=2)
        self.paramRadiobtnBSpl = tkinter.Radiobutton(
            self.paramFrame, text='Куб. В-сплайн', variable=self.paramVar, value=3)
        self.paramVar.set(1)
        self.paramComputeBtn = tkinter.Button(
            self.paramFrame, text='Построить', command=self.calculate_and_show, state=tkinter.DISABLED)

        # calculated values table's frame
        self.tableFrame = tkinter.Frame(self.leftFrame)
        self.tableTree = tkinter.ttk.Treeview(self.tableFrame, columns=('value', 'type'))
        self.tableTree.heading('#0', text='X')
        self.tableTree.heading('value', text='Y')
        self.tableTree.heading('type', text='Метод')
        self.tableTree.column('#0', width=100)
        self.tableTree.column('value', width=100)
        self.tableTree.column('type', width=100)
        self.tableAddBtn = tkinter.Button(
            self.tableFrame, text='Добавить значение', command=self.calculate_at, state=tkinter.DISABLED)

        # pack into master's widget
        self.rightFrame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)
        self.leftFrame.pack(side=tkinter.LEFT, padx=10, pady=10)
        # pack into left frame
        self.openFileBtn.pack(side=tkinter.TOP)
        self.fileLabel.pack(side=tkinter.TOP)
        self.paramFrame.pack(side=tkinter.TOP, pady=10)
        self.tableFrame.pack(side=tkinter.TOP, pady=10)
        # pack into frame paramFrame's widgets
        self.paramLabel.pack()
        self.paramRadiobtnSpline.pack()
        self.paramRadiobtnBezier.pack()
        self.paramRadiobtnBSpl.pack()
        self.paramComputeBtn.pack()
        # pack into frame table's widgets
        self.tableTree.pack()
        self.tableAddBtn.pack()
        # plots
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot([1, 2, 3, 4, 5, 6, 7, 8], [3, 1, 7, 3, 5, 9, 10, 3])
        self.canvas = FigureCanvasTkAgg(self.fig, self.rightFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.rightFrame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()

    def load_file(self):
        self.knots = []
        self.values = []
        self.d = [0, 0]
        csvfile = tkinter.filedialog.askopenfile()
        if csvfile is not None:
            reader = csv.DictReader(csvfile, delimiter=' ', fieldnames=('knot', 'value'))
            for row in reader:
                self.knots.append(float(row['knot']))
                self.values.append(float(row['value']))
            self.paramComputeBtn.config(state=tkinter.NORMAL)
            self.tableAddBtn.config(state=tkinter.DISABLED)
            self.fileLabel.config(text=csvfile.name)

    def calculate_and_show(self):
        if self.paramVar.get() == 1:
            # spline
            self.spl = Spline()
        elif self.paramVar.get() == 2:
            # bezier
            self.spl = Bezier()
        else:
            # bspline
            self.spl = CubicBSpline()

        self.spl = self.spl.fit(self.knots, self.values, self.d[0], self.d[-1])
        x_list = np.linspace(min(self.knots), max(self.knots), len(self.knots) * 10)
        y_list = [self.spl.value(x) for x in x_list]
        self.tableAddBtn.config(state=tkinter.NORMAL)
        self.ax.clear()
        self.ax.plot(x_list, y_list)
        self.ax.plot(self.knots, self.values, 'bo')
        self.canvas.draw()

    def calculate_at(self):
        x = tkinter.simpledialog.askfloat("title", "x:")
        if x is not None:
            y = self.spl.value(x)
            if isinstance(self.spl, Spline):
                t = 'Куб. сплайн'
            elif isinstance(self.spl, Bezier):
                t = 'Кривые Безье'
            elif isinstance(self.spl, CubicBSpline):
                t = 'В-сплайн'
            else:
                t = '???'
            self.tableTree.insert('', 0, text=str(x), values=(str(y), t))


def main():
    app = tkinter.Tk()
    Preferences(app)
    app.mainloop()

if __name__ == '__main__':
    main()