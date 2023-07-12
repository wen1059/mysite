# -*- coding: utf-8 -*-
# date: 2022/6/28
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QFile
from ui_untitled import Ui_Form


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def slot1(self):
        file = QFileDialog.getOpenFileName(self)[0]
        self.ui.lineEdit.setText(file)
        print(self.ui.lineEdit.text())

    def slot2(self):
        dir = QFileDialog.getExistingDirectory(self)
        self.ui.lineEdit.setText(dir)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
