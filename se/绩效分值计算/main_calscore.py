# -*- coding: utf-8 -*-
# date: 2022/6/28
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from ui_calscore import Ui_MainWindow
from code_calscore import main


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def run(self):
        main(self.ui.calendarWidget_start.selectedDate().toString('yyyy-MM-dd'),
             self.ui.calendarWidget_end.selectedDate().toString('yyyy-MM-dd')
             )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
