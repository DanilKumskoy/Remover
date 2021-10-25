#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt
from sys import argv, exit

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # self.setFocusPolicy(Qt.StrongFocus)

        # def focusInEvent(self, event):
        #     print('focusInEvent')
        #     self.setWindowTitle('focusInEvent')
        #     self.showMinimized()
        #
        # def focusOutEvent(self, event):
        #     print('focusOutEvent')
        #     self.setWindowTitle('focusOutEvent')
        #     # self.showMinimized()



if __name__ == '__main__':
    app = QApplication([])
    w = Window()
    w.showMinimized()
    exit(app.exec_())