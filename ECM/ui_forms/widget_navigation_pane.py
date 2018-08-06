# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_navigation_pane.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_pane_navigation(object):
    def setupUi(self, pane_navigation):
        pane_navigation.setObjectName("pane_navigation")
        pane_navigation.resize(451, 591)
        self.gridLayout = QtWidgets.QGridLayout(pane_navigation)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(pane_navigation)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(pane_navigation)
        QtCore.QMetaObject.connectSlotsByName(pane_navigation)

    def retranslateUi(self, pane_navigation):
        _translate = QtCore.QCoreApplication.translate
        pane_navigation.setWindowTitle(_translate("pane_navigation", "Form"))
        self.label.setText(_translate("pane_navigation", "navigation coming soon"))
