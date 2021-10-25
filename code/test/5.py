import sys
from PyQt5.QtWidgets import QSystemTrayIcon, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


@pyqtSlot()
def action(signal):
    print('test1')

app = QApplication(sys.argv)
icon = QSystemTrayIcon(QIcon('any_icon.png'), app)
icon.show()

icon.activated.connect(action)
#icon.activated['QSystemTrayIcon::ActivationReason'].connect(action)
#icon.pyqtConfigure(activated=action)

print(icon.receivers(icon.activated))  # to check if is connected
sys.exit(app.exec_())