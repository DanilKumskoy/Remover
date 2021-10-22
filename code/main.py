import sys
import os
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget, QInputDialog, QMessageBox, QAction

from ui.MainForm import Ui_MainWindow as MainF
from ui.ListForm import Ui_Form as ListF
from ui.LogForm import Ui_Dialog as LogF
from ui.Help import Ui_Form as HelpF



class MainWindow(QtWidgets.QMainWindow, MainF):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        def setDirectory(event):
            dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
            self.dirLineEdit.setText(dirlist)
            # self.plainTextEdit.appendHtml("<br>Выбрали папку: <b>{}</b>".format(dirlist))
        self.dirLineEdit.mouseDoubleClickEvent = setDirectory
        self.SearchButton.clicked.connect(lambda: self.Search())
        self.pushButton.clicked.connect(lambda: self.help())
    def help(self):
        self.h = Help()
        self.h.show()

    def Search(self):
        global filelist, dir
        dir = self.dirLineEdit.text()
        word = self.wordLineEdit.text()
        txt = ""

        if dir == "":
            QMessageBox.critical(self, "Ошибка ", "Введите директроию", QMessageBox.Ok)
        else:
            try:
                filelist = []
                log = open("log.txt", 'a')
                log.write("Remover log " + str(datetime.now()) + ":\n")
                log.write("Dir: " + dir + "\nWord: " + word + "\n\n")
                # print(os.listdir(dir))

                for f in os.listdir(dir):
                    log.write(f)

                    if f.find(word) != -1:
                        # print(f)
                        filelist.append(f)

                        log.write(" " * (20 - len(f)) + "Содержит в названии " + word + "\n")

                    else:
                        if f.endswith(".txt"):
                            # print(f)
                            file = open(dir + "/" + f, 'r')
                            if file.read().find(word) != -1:
                                filelist.append(f)
                                log.write(" " * (20 - len(f)) + "В файле найдено " + word + "\n")
                            else:
                                log.write("\n")
                        else:
                            log.write("\n")

                log.close()
                self.listw = ListWindow(self)
                self.listw.show()
            except:
                QMessageBox.critical(self, "Ошибка ", "Такой дириктории нет", QMessageBox.Ok)


class ListWindow(QtWidgets.QDialog, ListF):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        txt = ''

        for f in filelist:
            txt += f + "\n"
        self.textBrowser.setText(txt)

        self.delallButton.clicked.connect(lambda: self.DelAll())
        self.cancelButton.clicked.connect(lambda: self.close())

    def DelAll(self):
        global filelist, txt

        txt = ''
        log = open("log.txt", 'a')
        log.write("\n")
        for f in filelist:
            # print(dir + '\\' + f)
            os.remove(dir + '\\' + f)
            log.write(f + " " * (20 - len(f)) + "Remowed" + "\n")
            txt += f + " " * (20 - len(f)) + "Remowed" + "\n"

        log.write("--" * 100 + "\n")
        log.write("--" * 100 + "\n")
        log.write("--" * 100 + "\n\n\n")
        log.close()
        self.logw = LogWindow()
        self.logw.show()
        self.hide()


class LogWindow(QtWidgets.QDialog, LogF):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.textBrowser.setText(txt)

class Help(QtWidgets.QDialog, HelpF):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mv = MainWindow()
    mv.show()
    sys.exit(app.exec_())
