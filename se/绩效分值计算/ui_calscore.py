# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calscore.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(560, 369)
        MainWindow.setMinimumSize(QSize(100, 100))
        MainWindow.setMaximumSize(QSize(3840, 2160))
        MainWindow.setWindowOpacity(1.000000000000000)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(190, 240, 181, 81))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 250, 212))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.calendarWidget_start = QCalendarWidget(self.layoutWidget)
        self.calendarWidget_start.setObjectName(u"calendarWidget_start")
        self.calendarWidget_start.setMouseTracking(False)
        self.calendarWidget_start.setSelectedDate(QDate(2022, 9, 1))

        self.verticalLayout.addWidget(self.calendarWidget_start)

        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(300, 10, 250, 212))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setFocusPolicy(Qt.NoFocus)

        self.verticalLayout_2.addWidget(self.label_2)

        self.calendarWidget_end = QCalendarWidget(self.layoutWidget1)
        self.calendarWidget_end.setObjectName(u"calendarWidget_end")
        self.calendarWidget_end.setSelectedDate(QDate(2022, 10, 1))

        self.verticalLayout_2.addWidget(self.calendarWidget_end)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 560, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.calendarWidget_end, self.pushButton)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.run)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u65e5\u671f", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f\u65e5\u671f", None))
    # retranslateUi

