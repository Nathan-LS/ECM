# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_scope_sso.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_scopes_sso(object):
    def setupUi(self, scopes_sso):
        scopes_sso.setObjectName("scopes_sso")
        scopes_sso.setEnabled(True)
        scopes_sso.resize(320, 337)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(scopes_sso)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(scopes_sso)
        self.frame.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tabWidget = QtWidgets.QTabWidget(self.frame)
        self.tabWidget.setObjectName("tabWidget")
        self.read = QtWidgets.QWidget()
        self.read.setObjectName("read")
        self.gridLayout = QtWidgets.QGridLayout(self.read)
        self.gridLayout.setObjectName("gridLayout")
        self.read_scopes_list = QtWidgets.QListWidget(self.read)
        self.read_scopes_list.setObjectName("read_scopes_list")
        self.gridLayout.addWidget(self.read_scopes_list, 0, 0, 1, 1)
        self.tabWidget.addTab(self.read, "")
        self.write = QtWidgets.QWidget()
        self.write.setObjectName("write")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.write)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.write_scopes_list = QtWidgets.QListWidget(self.write)
        self.write_scopes_list.setObjectName("write_scopes_list")
        self.verticalLayout_3.addWidget(self.write_scopes_list)
        self.tabWidget.addTab(self.write, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.sso_redirect = QtWidgets.QPushButton(self.frame)
        self.sso_redirect.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/static/icons/eve-sso-login-black-large.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.sso_redirect.setIcon(icon)
        self.sso_redirect.setIconSize(QtCore.QSize(270, 40))
        self.sso_redirect.setFlat(True)
        self.sso_redirect.setObjectName("sso_redirect")
        self.verticalLayout.addWidget(self.sso_redirect)
        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(scopes_sso)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(scopes_sso)

    def retranslateUi(self, scopes_sso):
        _translate = QtCore.QCoreApplication.translate
        scopes_sso.setWindowTitle(_translate("scopes_sso", "Form"))
        self.label.setText(_translate("scopes_sso", "Scope Permissions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.read), _translate("scopes_sso", "Read"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.write), _translate("scopes_sso", "Write"))
