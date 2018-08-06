# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_pane_char_overview.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_tab_overview(object):
    def setupUi(self, tab_overview):
        tab_overview.setObjectName("tab_overview")
        tab_overview.resize(787, 670)
        self.gridLayout = QtWidgets.QGridLayout(tab_overview)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(tab_overview)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.pilot_contents = QtWidgets.QWidget()
        self.pilot_contents.setGeometry(QtCore.QRect(0, 0, 785, 668))
        self.pilot_contents.setObjectName("pilot_contents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.pilot_contents)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea.setWidget(self.pilot_contents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(tab_overview)
        QtCore.QMetaObject.connectSlotsByName(tab_overview)

    def retranslateUi(self, tab_overview):
        _translate = QtCore.QCoreApplication.translate
        tab_overview.setWindowTitle(_translate("tab_overview", "Form"))
