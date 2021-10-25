from PyQt5.QtWidgets import QMessageBox

msg = QMessageBox()
msg.setWindowTitle("Название окна")
msg.setText("Описание")
msg.setIcon(QMessageBox.Warning)