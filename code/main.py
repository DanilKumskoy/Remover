import sys
import os
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QWidget, QInputDialog, QMessageBox, QAction, QSystemTrayIcon, QStyle, QMenu

from ui.MainForm import Ui_MainWindow as MainF
from ui.ListForm import Ui_Form as ListF
from ui.LogForm import Ui_Dialog as LogF
from ui.Help import Ui_Form as HelpF
from ui.Screensaver import Ui_Form as SC
from ui.Settings import Ui_Form as SE


class MainWindow(QtWidgets.QMainWindow, MainF):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        global f1, f2, f3, f4
        f1 = False
        f2 = True
        f3 = False
        f4 = True

        def setDirectory(event):
            dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
            self.dirLineEdit.setText(dirlist)
            # self.plainTextEdit.appendHtml("<br>Выбрали папку: <b>{}</b>".format(dirlist))

        self.dirLineEdit.mouseDoubleClickEvent = setDirectory

        self.SearchButton.clicked.connect(lambda: self.Search())
        # self.pushButton.clicked.connect(lambda: self.pr())

        self.action_help.triggered.connect(lambda: self.help())
        self.action_settings.triggered.connect(lambda: self.settings())

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        @pyqtSlot()
        def action(signal):
            if signal == 2:
                self.showNormal()

        self.tray_icon.activated.connect(action)
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(app.quit)
        tray_menu = QMenu()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event):
        if f1:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Tray Program",
                "Application was minimized to Tray",
                QSystemTrayIcon.Information,
                2000
            )


    def help(self):
        self.h = Help()

        self.h.show()

    def settings(self):
        self.s = Settings()
        self.s.show()

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
                log = open("log.txt", 'w')
                log.write("Remover log:\n")
                log.write("Dir: " + dir + "\nWord: " + word + "\n\n")
                print(os.listdir(dir))

                for f in os.listdir(dir):
                    log.write(f)

                    if f.find(word) != -1:
                        print(f)
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
                                # pass
                        else:
                            log.write("\n")
                            # pass

                # log.close()
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
        self.cancelButton.clicked.connect(lambda: self.Cancel())

    def DelAll(self):
        if f3:
            msg = QMessageBox.critical(self, "Удалить ", "Вы уверены что хотите удалиь эти файлы?",
                                       QMessageBox.Ok | QMessageBox.No)
        if msg == 1024 or f3 == False:

            global filelist, txt

            txt = ''
            log = open("log.txt", 'a')
            log.write("\n")
            for f in filelist:
                # os.remove(dir + '\\' + f)
                log.write(f + " " * (20 - len(f)) + "Remowed" + "\n")
                txt += f + " " * (20 - len(f)) + "Remowed" + "\n"

            log.write("--" * 100 + "\n")
            log.write("--" * 100 + "\n")
            log.write("--" * 100 + "\n\n\n")
            log.close()
            if f2:
                self.logw = LogWindow()
                self.logw.show()
            self.hide()

    def Cancel(self):
        log = open("log.txt", 'a')
        log.write("--" * 100 + "\n")
        log.write("--" * 100 + "\n")
        log.write("--" * 100 + "\n\n\n")
        log.close()
        self.close()


class LogWindow(QtWidgets.QDialog, LogF):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.textBrowser.setText(txt)


class Help(QtWidgets.QDialog, HelpF):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class Screensaver(QtWidgets.QWidget, SC):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Settings(QtWidgets.QWidget, SE):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.buttonBox.accepted.connect(lambda: self.Change())

    def Change(self):
        global f1, f2, f3, f4
        f1 = self.checkBox_1.isChecked()
        f2 = self.checkBox_2.isChecked()
        f3 = self.checkBox_3.isChecked()
        f4 = self.checkBox_4.isChecked()
        # print(f1, f2, f3, f4)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mv = MainWindow()
    mv.showMinimized()
    # mv.show()

    sc = Screensaver()
    sc.show()
    QtCore.QTimer.singleShot(1500, sc.close)

    sys.exit(app.exec_())
