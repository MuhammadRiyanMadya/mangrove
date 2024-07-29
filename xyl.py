import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (QWidget,QApplication, QMainWindow,
                               QGridLayout, QLineEdit, QSpinBox,
                               QGroupBox, QDialog, QVBoxLayout,
                               QPushButton, QLabel, QHBoxLayout,
                               QSpinBox, QTabWidget, QSizePolicy,
                               QTableWidget)
import pyqtgraph as pg
import sys


import os

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




def xyleneOpener(path):
    numberDB = np.array([])
    tdDB = np.array([])
    xylDB = np.array([])
    counter = 1
    for docs in os.listdir(path):
        newpath = os.chdir(path + '\\' + docs)
            
        for file in os.listdir(newpath):
            if '.xlsx' in file:

                np.append(numberDB, counter)
                
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
            
    print(counter)
                
    return numberDB, tdDB, xylDB

def dataNormalizer(data):    
    i = 0
    index = 0
    while i < len(data):
        if not np.isnan(data[i]):
            index = i
            print(index)
        else:
            data[i] = data[index]
        i += 1
    return data

numDB, tdrDB, xylDB = xyleneOpener(r'C:\Users\mrm\Desktop\Catalyst Change\Inline History\2024')

xyleneDB = np.asarray(numDB, tdrDB, xylDB)
np.savetext('xyleneDB.csv', xyleneDB, delimiter=",")
tdrDB = dataNormalizer(tdrDB)
xylDB = dataNormalizer(xylDB)
tdr = list(tdr)
xyl = list(xyl)

print(tdrDB)
print(xylDB)

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
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("History Peaks")
        layout = QGridLayout(self)
        layout.setContentsMargins(10,10,10,10)
        layout.addWidget(self.graphConfig())
        
    def setData(self, xdata, ydata1, ydata2):

        self.v1.addItem(pg.PlotCurveItem(xdata, ydata1, pen='#2E2EFE'))
        self.v2.addItem(pg.PlotCurveItem(xdata, ydata2, pen='#2EFEF7'))

        self.v1.setYRange(0,400, padding = 0.1)
        self.v2.setYRange(0,6, padding = 0.1)

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
        self.l.addItem(self.p1, row = 2, col = 3, rowspan = 2, colspan = 1)

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
        self.a2.setLabel('Xylene %', color='#FEFE2E')
        self.v1.enableAutoRange(axis= pg.ViewBox.XYAxes, enable=True)
        self.v1.sigResized.connect(self.updateViews)
        self.updateViews()

        return self.graph
    
    def updateViews(self):
        self.v2.setGeometry(self.v1.sceneBoundingRect())

        return
import time
timestamp1 = time.mktime(time.strptime('2024-7-25 00:00:00', '%Y-%m-%d %H:%M:%S'))


##timer = np.linspace(timestamp1, timestamp1+24*3600, 24)
##timer = list(timer)
##print(timer)




##
##if __name__ == "__main__":
##    app = QApplication(sys.argv)
##    window = mainWindow()
##    window.setData(timer, tdr, xyl)
##    window.show()
##    sys.exit(app.exec())
