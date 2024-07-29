import pandas as pd
import numpy as np

from PySide6.QtWidgets import (QWidget,QApplication, QMainWindow,
                               QGridLayout, QLineEdit, QSpinBox,
                               QGroupBox, QDialog, QVBoxLayout,
                               QPushButton, QLabel, QHBoxLayout,
                               QSpinBox, QTabWidget, QSizePolicy,
                               QTableWidget)
import pyqtgraph as pg
from pyqtgraph import QtCore
import sys
import time

import os
from datetime import datetime

##def find(path, dire):
##    for folder in os.listdir(path):
##        try:
##            if folder == dire:
##                os.chdir(path + '\\' + dire)
##                print('+-> ' + os.getcwd())
##            elif '.' not in folder:
##                find(path + '\\' + folder,dire)
##            elif '.' in folder:
##                continue
##            else:
##                break
##        except:
##            print('+-> ' + folder + ' does not allow to be searched')
##            continue
##    return
##
##find(r'C:\Users\mrm\Documents', 'python')

import time
timestamp1 = time.mktime(time.strptime('2024-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
timestamp2 = time.mktime(time.strptime('2024-08-01 00:00:00', '%Y-%m-%d %H:%M:%S'))

date = []
while timestamp1 < timestamp2:
    date.append(timestamp1)
    timestamp1 = timestamp1+3600
print()
print(datetime.fromtimestamp(date[-1]).strftime('%Y-%m-%d %H:%M:%S'))

def xyleneOpener(path):
    tdDB = np.array([])
    xylDB = np.array([])
    counter = 1
    for docs in os.listdir(path):
        newpath = os.chdir(path + '\\' + docs)
            
        for file in os.listdir(newpath):
            if '.xlsx' in file or '.XLSx':

                df = pd.read_excel(file, header = 0, usecols="B:O")

                xylBool = df == 'XYL'
                if len(np.nonzero(xylBool.values)[1]) == 0:
                    xylBool = df == 'xyl'
                xylindex = np.nonzero(xylBool.values)[1][0]

                tdBool = df == 'T/D Ratio'
                if len(np.nonzero(tdBool.values)[1]) == 0:
                    tdBool = df == 'T/D ratio'
                tdindex = np.nonzero(tdBool.values)[1][0]

                df = df.values
                tdDB = np.append(tdDB, df[:,tdindex][15:39])
                xylDB = np.append(xylDB, df[:,xylindex][15:39])

                counter += 1
    numberDB = np.linspace(1,len(tdDB),len(tdDB))
    
    for val in xylDB:
        if type(val) == str:
            valindex = np.where(xylDB == val)
            xylDB[valindex[0][0]] = np.nan

    for val in tdDB:
        if type(val) == str:
            valindex = np.where(tdDB == val)
            tdDB[valindex[0][0]] = np.nan
            
                
    return numberDB, tdDB, xylDB

def dataNormalizer(data):    
    i = 0
    index = 0
    while i < len(data):
        if not np.isnan(data[i]):
            index = i
        else:
            data[i] = data[index]
        i += 1
    return data

##numDB, tdrDB, xylDB = xyleneOpener(r'C:\Users\ssv\Documents\MRM\PP\2024')
##
##
##xyleneDB = np.vstack((numDB, tdrDB, xylDB)).T
##np.savetxt(r'C:\Users\ssv\Documents\MRM\PP\xyleneDB.csv', xyleneDB, delimiter=",")


df = pd.read_csv(r'C:\Users\ssv\Documents\MRM\PP\xyleneDB.csv', header = None)
numDB = df.values.T[0]
tdrDB = df.values.T[1]
xylDB = df.values.T[2]

tdrDB = dataNormalizer(tdrDB)
xylDB = dataNormalizer(xylDB)
tdr = list(tdrDB)
xyl = list(xylDB)

xylHigh = []
xylLow = []
for i in numDB:
    xylHigh.append(5)
    xylLow.append(2.5)

##for i in range(len(xyl)):
##    if xyl[i] < 2.5:
##        print(i)
##        print(xyl[i])
##        print(datetime.fromtimestamp(date[i]).strftime('%Y-%m-%d %H:%M:%S'))
##        print()




##def plotter(xdata, ydata1, ydata2):    
##    fig, ax1 = plt.subplots()
##    
##    color = 'tab:red'
##    ax1.set_xlabel('hours')
##    ax1.set_ylabel('T/D Ratio', color = color)
##    ax1.plot(xdata, ydata1, color = color)
##    ax1.tick_params(axis='y', labelcolor=color)
##
##    ax2 = ax1.twinx()
##
##    color = 'tab:blue'
##    ax2.set_ylabel('Xylene %', color = color)
##    ax2.plot(xdata, ydata2, color = color)
####    ax2.tick_params(axis='y', labelcolor=color)
##
##    fig.tight_layout()
##    plt.show()
##
##plotter(time, tdr, xyl)

class mainWindow(QWidget):
    
    def __init__(self, xdata, ydata1, ydata2):
        super().__init__()
        self.setWindowTitle("History Peaks")
        layout = QGridLayout(self)
##        layout.setContentsMargins(10,10,10,10)

        self.xdata = xdata
        self.ydata1 = ydata1
        self.ydata2 = ydata2

        layout.addWidget(self.graphConfig())
    def setItem(self, pos):
        pos = time.mktime(time.strptime(pos, '%Y-%m-%d %H:%M:%S'))
        self.v1.addItem(pg.InfiniteLine(pos, angle=90, movable = False,name='HR -> ZN', pen=pg.mkPen('g', width=1, style=QtCore.Qt.SolidLine)))
        
    def graphConfig(self):
        self.graph = pg.GraphicsView()
        self.graph.setWindowTitle('History Peaks')
        self.graph.show()
        self.l = pg.GraphicsLayout()
        self.graph.setCentralWidget(self.l)
        
        #v2 and a2 for additional graph and y axis
        self.a2 = pg.AxisItem('left')
        self.a2.setRange(-5,15)
        self.v2 = pg.ViewBox()
        self.l.addItem(self.a2, row = 2, col = 2, rowspan = 2, colspan = 1)
        
        # blank x-axis to alignment
##        ax = pg.AxisItem(orientation='bottom')
##        ax.setPen('#000000')
##        pos = (3,3)
##        self.l.addItem(ax, *pos)
        
        #v1 is the main plot, it has its own box
        self.p1 = pg.PlotItem()
        self.v1 = self.p1.vb
        self.l.addItem(self.p1, row = 2, col = 0, rowspan = 2, colspan = 1)

        # time axis
        self.timeAxis = pg.DateAxisItem(orientation='bottom')
        self.p1.setAxisItems({'bottom': self.timeAxis})

        
        #grid
        self.p1.showGrid(x=True, y=True)
        #Link between v1 and v2
        self.l.scene().addItem(self.v2)
        self.a2.linkToView(self.v2)
        self.v2.setXLink(self.v1)
        #Axis label
        self.p1.getAxis('left').setLabel('TD ratio', color='#2E2EFE')
        self.p1.getAxis('bottom').setLabel('Time', color='#000000')
        self.a2.setLabel('Xylene %', color='#FEFE2E')
        self.v1.enableAutoRange(axis= pg.ViewBox.XYAxes, enable=True)
        self.v1.sigResized.connect(self.updateViews)
        self.updateViews()

        self.v1.addItem(pg.PlotCurveItem(self.xdata, self.ydata1, pen='#2E2EFE'))
        self.v2.addItem(pg.PlotCurveItem(self.xdata, self.ydata2, pen='#FEFE2E'))
        self.v2.addItem(pg.PlotCurveItem(self.xdata, xylHigh, pen='#FEFE2E'))
        self.v2.addItem(pg.PlotCurveItem(self.xdata, xylLow, pen='#FEFE2E'))

##        self.v1.setXRange(min(self.xdata), max(self.xdata))
##        self.v1.setYRange(0,400, padding = 0.1)
##        self.v2.setYRange(0,6, padding = 0.1)
        region = pg.LinearRegionItem()
        region.setZValue(1000)
        self.v1.addItem(region, ignoreBounds = True)
        

        return self.graph
    
    def updateViews(self):
        self.v2.setGeometry(self.v1.sceneBoundingRect())

        return

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow(date, tdr, xyl)
    window.setItem('2024-07-26 00:00:00')
    window.show()
    sys.exit(app.exec())
