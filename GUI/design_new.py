# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Desktop/itmo/TAY_helper/GUI/design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(436, 475)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		self.A_field = QtWidgets.QPlainTextEdit(self.centralwidget)
		self.A_field.setGeometry(QtCore.QRect(50, 20, 150, 150))
		self.A_field.setTabChangesFocus(True)
		self.A_field.setObjectName("A_field")
		self.A_field.setPlaceholderText("1 2 3\n4 5 6\n7 8 9")

		self.B_field = QtWidgets.QPlainTextEdit(self.centralwidget)
		self.B_field.setGeometry(QtCore.QRect(260, 20, 150, 150))
		self.B_field.setObjectName("B_field")
		self.B_field.setPlaceholderText("0\n1\n2")
		self.B_field.setTabChangesFocus(True)

		self.C_field = QtWidgets.QPlainTextEdit(self.centralwidget)
		self.C_field.setGeometry(QtCore.QRect(50, 180, 150, 150))
		self.C_field.setObjectName("C_field")
		self.C_field.setPlaceholderText("0 1 2")
		self.C_field.setTabChangesFocus(True)

		self.TF_field = QtWidgets.QPlainTextEdit(self.centralwidget)
		self.TF_field.setGeometry(QtCore.QRect(260, 180, 150, 150))
		self.TF_field.setObjectName("TF_field")
		self.TF_field.setPlaceholderText("1, 2, 3\n1, 2, 3, 4")
		self.TF_field.setTabChangesFocus(True)

		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(10, 80, 41, 31))
		self.label.setTextFormat(QtCore.Qt.RichText)
		self.label.setObjectName("label")

		self.label_2 = QtWidgets.QLabel(self.centralwidget)
		self.label_2.setGeometry(QtCore.QRect(220, 80, 41, 31))
		self.label_2.setTextFormat(QtCore.Qt.RichText)
		self.label_2.setObjectName("label_2")

		self.label_3 = QtWidgets.QLabel(self.centralwidget)
		self.label_3.setGeometry(QtCore.QRect(210, 230, 41, 31))
		self.label_3.setTextFormat(QtCore.Qt.RichText)
		self.label_3.setObjectName("label_3")

		self.label_4 = QtWidgets.QLabel(self.centralwidget)
		self.label_4.setGeometry(QtCore.QRect(10, 230, 41, 31))
		self.label_4.setTextFormat(QtCore.Qt.RichText)
		self.label_4.setObjectName("label_4")

		self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
		self.layoutWidget.setGeometry(QtCore.QRect(10, 410, 411, 61))
		self.layoutWidget.setObjectName("layoutWidget")

		self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout.setObjectName("horizontalLayout")

		self.startButton = QtWidgets.QPushButton(self.layoutWidget)
		self.startButton.setObjectName("startButton")
		self.horizontalLayout.addWidget(self.startButton)

		self.clearButton = QtWidgets.QPushButton(self.layoutWidget)
		self.clearButton.setObjectName("clearButton")
		self.horizontalLayout.addWidget(self.clearButton)

		self.ControllRadioButton = QtWidgets.QRadioButton(self.centralwidget)
		self.ControllRadioButton.setGeometry(QtCore.QRect(270, 358, 131, 23))
		self.ControllRadioButton.setChecked(True)
		self.ControllRadioButton.setObjectName("ControllRadioButton")

		self.ObserveRadioButton = QtWidgets.QRadioButton(self.centralwidget)
		self.ObserveRadioButton.setGeometry(QtCore.QRect(270, 380, 131, 21))
		self.ObserveRadioButton.setChecked(False)
		self.ObserveRadioButton.setObjectName("ObserveRadioButton")

		self.SystemQualitiesField = QtWidgets.QTextEdit(self.centralwidget)
		self.SystemQualitiesField.setGeometry(QtCore.QRect(120, 340, 81, 61))
		self.SystemQualitiesField.setObjectName("SystemQualitiesField")
		self.SystemQualitiesField.setReadOnly(True)

		self.label_5 = QtWidgets.QLabel(self.centralwidget)
		self.label_5.setGeometry(QtCore.QRect(16, 340, 101, 20))
		self.label_5.setObjectName("label_5")

		self.label_6 = QtWidgets.QLabel(self.centralwidget)
		self.label_6.setGeometry(QtCore.QRect(10, 360, 101, 20))
		self.label_6.setObjectName("label_6")

		self.label_7 = QtWidgets.QLabel(self.centralwidget)
		self.label_7.setGeometry(QtCore.QRect(30, 380, 101, 20))
		self.label_7.setObjectName("label_7")

		self.label_8 = QtWidgets.QLabel(self.centralwidget)
		self.label_8.setGeometry(QtCore.QRect(290, 340, 101, 20))
		self.label_8.setObjectName("label_8")

		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "TAYHelper"))
		self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">A =</span></p></body></html>"))
		self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">B =</span></p></body></html>"))
		self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-style:italic;\">W(s) =</span></p></body></html>"))
		self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">C =</span></p></body></html>"))
		self.startButton.setText(_translate("MainWindow", "Начать"))
		self.clearButton.setText(_translate("MainWindow", "Очистить"))
		self.ControllRadioButton.setText(_translate("MainWindow", "Управляемый"))
		self.ObserveRadioButton.setText(_translate("MainWindow", "Наблюдаемый"))
		self.label_5.setText(_translate("MainWindow", "Управляемая"))
		self.label_6.setText(_translate("MainWindow", "Наблюдаемая"))
		self.label_7.setText(_translate("MainWindow", "Устойчивая"))
		self.label_8.setText(_translate("MainWindow", "Базис:"))

