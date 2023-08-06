#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 14:46:20 2019
Windows for plot
@author: juliengautier
"""

import pyqtgraph as pg # pyqtgraph biblio permettent l'affichage 

import qdarkstyle # pip install qdakstyle https://github.com/ColinDuquesnoy/QDarkStyleSheet  sur conda
from PyQt5.QtWidgets import QApplication,QHBoxLayout,QWidget
from PyQt5.QtGui import QIcon
import sys,time

import pathlib,os

class GRAPHCUT(QWidget):
    
    def __init__(self,symbol=True,title='Plot'):
        super(GRAPHCUT, self).__init__()
        p = pathlib.Path(__file__)
        sepa=os.sep
        self.title=title
        self.icon=str(p.parent) + sepa+'icons' +sepa
        self.winPLOT = pg.GraphicsLayoutWidget()
        self.isWinOpen=False
        self.symbol=symbol
        self.setup()
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon+'LOA.png'))
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        
        
    def setup(self):
        hLayout2=QHBoxLayout()
        hLayout2.addWidget(self.winPLOT)
        self.setLayout(hLayout2)
        self.pCut=self.winPLOT.addPlot(1,0)
        
#    def Display(self,cutData) :
#        pass
        
    def PLOT(self,cutData,axis=None,symbol=True,pen=True,label=None):
        
        self.pen=pen
        if self.pen ==None:
            self.symbol=symbol
            if axis==None:
                if self.symbol==True:
                    self.pCut.plot(cutData,clear=True,symbol='t',pen=self.pen)
                else:
                    self.pCut.plot(cutData,clear=True,pen=self.pen)
            else:
                if self.symbol==True:
                    self.pCut.plot(axis,cutData,clear=True,symbol='t',pen=self.pen)
                else:
                    self.pCut.plot(axis,cutData,clear=True,pen=self.pen)
        else:
            self.symbol=symbol
            if axis==None:
                if self.symbol==True:
                    self.pCut.plot(cutData,clear=True,symbol='t')
                else:
                    self.pCut.plot(cutData,clear=True)
            else:
                if self.symbol==True:
                    self.pCut.plot(axis,cutData,clear=True,symbol='t')
                else:
                    self.pCut.plot(axis,cutData,clear=True)
            
        if label!=None:
            self.pCut.setLabel('bottom',label)
              
            
    def SetTITLE(self,title):
        self.setWindowTitle(title)
    
    def closeEvent(self, event):
        """ when closing the window
        """
        self.isWinOpen=False
        time.sleep(0.1)
        event.accept()
    
    
if __name__ == "__main__":
    appli = QApplication(sys.argv) 
    appli.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    e = GRAPHCUT()  
    e.show()
    appli.exec_()     
        
