# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_pilot_tabs.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_pilot_tab_widget(object):
    def setupUi(self, pilot_tab_widget):
        pilot_tab_widget.setObjectName("pilot_tab_widget")
        pilot_tab_widget.resize(613, 733)
        self.gridLayout = QtWidgets.QGridLayout(pilot_tab_widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pilot_tabs = QtWidgets.QTabWidget(pilot_tab_widget)
        self.pilot_tabs.setTabBarAutoHide(False)
        self.pilot_tabs.setObjectName("pilot_tabs")
        self.gridLayout.addWidget(self.pilot_tabs, 0, 0, 1, 1)

        self.retranslateUi(pilot_tab_widget)
        QtCore.QMetaObject.connectSlotsByName(pilot_tab_widget)

    def retranslateUi(self, pilot_tab_widget):
        _translate = QtCore.QCoreApplication.translate
        pilot_tab_widget.setWindowTitle(_translate("pilot_tab_widget", "Form"))
