import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QToolBar, QMenu, QAction, QGraphicsView, QApplication


class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()

        # a grid foreground
        self.scene.setBackgroundBrush(QBrush(Qt.lightGray, Qt.CrossPattern))
        self.grid = True

        # Create menu options
        menubar = self.menuBar()
        menu = QMenu('File', self)  # title and parent
        db_action = QAction("Open file", self)  # title and parent
        db_action.setStatusTip("Select a file to use as a database")
        db_action.triggered.connect(self.open_new_db)
        menu.addAction(db_action)
        menubar.addMenu(menu)

        # tb.addWidget(menu)
        # tb.setAllowedAreas(Qt.TopToolBarArea)
        # tb.setFloatable(False)
        # tb.setMovable(False)
        # self.addToolBar(tb)

        self.statusBar().showMessage("Ready")

        # Demonstrate the results from the input.

        graphics = QGraphicsView(self.scene)
        self.setCentralWidget(graphics)
        self.showFullScreen()

    def open_new_db(self):
        pass

    def keyPressEvent(self, e):
        # Currently, we respond to a press of the Escape key by closing the program.
        if e.key() == Qt.Key_Escape:
            self.close()

app = QApplication(sys.argv)
gr = GraphWindow()
sys.exit(app.exec_())