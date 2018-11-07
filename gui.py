import sys
import random
from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import *
import numpy as np

class MyScene(QtWidgets.QGraphicsScene):
    def __init__(self, s, grids):
        QtWidgets.QGraphicsScene.__init__(self)
        self.grids = grids
        self.s = s
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_next)
        self.timer.start(500)
        self.w = 800
        self.tile_w = (self.w - 100) // s
        self.t_off = self.tile_w // 2
        self.f = QtGui.QFont("Times", 25, QtGui.QFont.Bold)
        self.display(self.grids.pop(0))
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
                    t = self.addText("{}".format(grid[x][y]))
                    t.setPos(y * self.tile_w + self.t_off, x * self.tile_w + self.t_off)
                    t.setFont(self.f)
                    r = QRectF(y * self.tile_w, x * self.tile_w, self.tile_w, self.tile_w)
                    self.addRect(r)

def display_all(s, grids):
    if s > 10:
        print ("this grid is too wide to be displayed")
        sys.exit(0)
    grids = [np.asarray(g).reshape(s,s) for g in grids]
    app = QtWidgets.QApplication([])
    scene = MyScene(s, grids)
    view = QtWidgets.QGraphicsView(scene)
    view.resize(scene.w, scene.w)
    view.show()
    sys.exit(app.exec_())
        