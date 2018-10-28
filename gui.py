#! /usr/bin/env python3

import sys
import random
from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import *

class MyScene(QtWidgets.QGraphicsScene):
    def __init__(self, s, grids):
        QtWidgets.QGraphicsScene.__init__(self)
        self.grids = grids
        self.s = s
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_next)
        self.timer.start(500)
        self.display_next()
    def display_all(self):
        for grid in self.grids:
            display(self.s, grid, self)
    def display_next(self):
        if self.grids:
            curr = self.grids.pop(0)
            self.display(curr)
        else:
            self.timer.stop()
    def display(self, grid):
        self.clear()
        for y in range(self.s):
            for x in range(self.s):
                if grid[x][y] != 0:
                    self.addText("{}".format(grid[x][y])).setPos(y * 100, x * 100)
                    self.addRect(y * 100, x * 100, 100, 100)

def display_all(s, grids):
    app = QtWidgets.QApplication([])
    scene = MyScene(s, grids)
    view = QtWidgets.QGraphicsView(scene)
    view.resize(800, 800)
    view.show()
    sys.exit(app.exec_())
        