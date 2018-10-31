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
import time

import numpy as np
from interp.spline import Spline
from interp.bspline import CubicBSpline
from interp.bezier import Bezier


class Preferences(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master=master)
        self.paramVar = tkinter.IntVar(master=master)
        self.delimVar = tkinter.StringVar(master=master)

        self.leftFrame = tkinter.Frame(master)
        self.rightFrame = tkinter.Frame(master)
        self.popupLabel = tkinter.Label(self.leftFrame, text='Разделитель csv', wraplength=300)
        self.popupMenu = tkinter.OptionMenu(self.leftFrame, self.delimVar, *{' ', ';', ','})
        self.delimVar.set(' ')
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
        # derivatives choice
        self.DFirstVar = tkinter.StringVar(master=master, value='0.0')
        self.DSecondVar = tkinter.StringVar(master=master, value='0.0')
        self.paramDFirstLabel = tkinter.Label(self.paramFrame, text='Производная слева')
        self.paramDFirstEntry = tkinter.Entry(self.paramFrame, textvariable=self.DFirstVar)
        self.paramDSecondLabel = tkinter.Label(self.paramFrame, text='Производная справа')
        self.paramDSecondEntry = tkinter.Entry(self.paramFrame, textvariable=self.DSecondVar)
        self.paramComputeBtn = tkinter.Button(
            self.paramFrame, text='Построить', command=self.calculate_and_show, state=tkinter.DISABLED)
        self.paramShowCfBtn = tkinter.Button(
            self.paramFrame, text='Коэффициенты', command=self.show_coefficient, state=tkinter.DISABLED)

        # calculated values table's frame
        self.tableFrame = tkinter.Frame(self.leftFrame)
        self.timeLabel = tkinter.Label(self.tableFrame, text='Время расчета коэффициентов')
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
        self.popupLabel.pack(side=tkinter.TOP)
        self.popupMenu.pack(side=tkinter.TOP)
        self.openFileBtn.pack(side=tkinter.TOP)
        self.fileLabel.pack(side=tkinter.TOP)
        self.paramFrame.pack(side=tkinter.TOP, pady=10)
        self.tableFrame.pack(side=tkinter.TOP, pady=10)
        # pack into frame paramFrame's widgets
        self.paramLabel.pack()
        self.paramRadiobtnSpline.pack()
        self.paramRadiobtnBezier.pack()
        self.paramRadiobtnBSpl.pack()
        self.paramDFirstLabel.pack()
        self.paramDFirstEntry.pack()
        self.paramDSecondLabel.pack()
        self.paramDSecondEntry.pack()
        self.paramComputeBtn.pack()
        self.paramShowCfBtn.pack()
        # pack into frame table's widgets
        self.timeLabel.pack()
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

        csvfile = tkinter.filedialog.askopenfile()
        if csvfile is not None:
            reader = csv.DictReader(csvfile, delimiter=self.delimVar.get(), fieldnames=('knot', 'value'))
            for row in reader:
                self.knots.append(float(row['knot']))
                self.values.append(float(row['value']))
            self.paramComputeBtn.config(state=tkinter.NORMAL)
            self.tableAddBtn.config(state=tkinter.DISABLED)
            self.fileLabel.config(text=csvfile.name)
        else:
            self.fileLabel.config(text='Ошибка при открытии файла')

    def calculate_and_show(self):
        self.d = [
            float(self.paramDFirstEntry.get()), 
            float(self.paramDSecondEntry.get()),
        ]
        if self.paramVar.get() == 1:
            # spline
            self.spl = Spline()
        elif self.paramVar.get() == 2:
            # bezier
            self.spl = Bezier()
        else:
            # bspline
            self.spl = CubicBSpline()

        first_time = time.perf_counter()
        self.spl = self.spl.fit(self.knots, self.values, self.d[0], self.d[-1])
        elapsed_time = time.perf_counter() - first_time
        self.timeLabel.config(text='Время расчетов коэффициентов: \
            %f с' % (elapsed_time, ))
        x_list = np.linspace(min(self.knots), max(self.knots), len(self.knots) * 10)
        y_list = [self.spl.value(x) for x in x_list]
        self.paramShowCfBtn.config(state=tkinter.NORMAL)
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

    def show_coefficient(self):
        with tkinter.filedialog.asksaveasfile() as file:
            if isinstance(self.spl, Spline):
                t = 'Cubic spline'
            elif isinstance(self.spl, Bezier):
                t = 'Bezier'
            elif isinstance(self.spl, CubicBSpline):
                t = 'Cubic B Spline'
            x = self.spl.A
            np.savetxt(fname=file.name, X=x, fmt='%10.5f', header=t)
        

if __name__ == '__main__':
    app = tkinter.Tk()
    Preferences(app)
    app.mainloop()