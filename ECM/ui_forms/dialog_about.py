# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_about.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog_about(object):
    def setupUi(self, dialog_about):
        dialog_about.setObjectName("dialog_about")
        dialog_about.resize(806, 445)
        self.label = QtWidgets.QLabel(dialog_about)
        self.label.setGeometry(QtCore.QRect(60, 30, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(dialog_about)
        self.label_2.setGeometry(QtCore.QRect(60, 60, 61, 21))
        self.label_2.setObjectName("label_2")
        self.text_version = QtWidgets.QLabel(dialog_about)
        self.text_version.setGeometry(QtCore.QRect(110, 60, 91, 16))
        self.text_version.setText("")
        self.text_version.setObjectName("text_version")
        self.label_3 = QtWidgets.QLabel(dialog_about)
        self.label_3.setGeometry(QtCore.QRect(60, 90, 81, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(dialog_about)
        self.label_4.setGeometry(QtCore.QRect(60, 120, 47, 13))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(dialog_about)
        self.label_5.setGeometry(QtCore.QRect(20, 150, 381, 191))
        self.label_5.setOpenExternalLinks(True)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(dialog_about)
        QtCore.QMetaObject.connectSlotsByName(dialog_about)

    def retranslateUi(self, dialog_about):
        _translate = QtCore.QCoreApplication.translate
        dialog_about.setWindowTitle(_translate("dialog_about", "Dialog"))
        self.label.setText(_translate("dialog_about", "EVE Character Manager (ECM)"))
        self.label_2.setText(_translate("dialog_about", "Version"))
        self.label_3.setText(_translate("dialog_about", "Copyright 2018"))
        self.label_4.setText(_translate("dialog_about", "TextLabel"))
        self.label_5.setText(
            _translate("dialog_about", "    This program is free software: you can redistribute it and/or modify\n"
                                       "    it under the terms of the GNU General Public License as published by\n"
                                       "    the Free Software Foundation, either version 3 of the License, or\n"
                                       "    (at your option) any later version.\n"
                                       "\n"
                                       "    This program is distributed in the hope that it will be useful,\n"
                                       "    but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
                                       "    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
                                       "    GNU General Public License for more details.\n"
                                       "\n"
                                       "    You should have received a copy of the GNU General Public License\n"
                                       "    along with this program.  If not, see <a  href=\"https://www.gnu.org/licenses/\">Testing</a>."))
