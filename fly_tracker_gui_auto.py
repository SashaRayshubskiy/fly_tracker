# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fly_tracker_gui.ui'
#
# Created: Tue Aug 19 08:26:51 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FlyTracker(object):
    def setupUi(self, FlyTracker):
        FlyTracker.setObjectName("FlyTracker")
        FlyTracker.resize(794, 578)
        FlyTracker.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(FlyTracker)
        self.centralwidget.setObjectName("centralwidget")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(6, 30, 111, 41))
        self.start_button.setObjectName("start_button")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(6, 88, 111, 41))
        self.stop_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.stop_button.setObjectName("stop_button")
        self.infuse_button = QtWidgets.QPushButton(self.centralwidget)
        self.infuse_button.setGeometry(QtCore.QRect(134, 100, 99, 27))
        self.infuse_button.setObjectName("infuse_button")
        self.withdraw_button = QtWidgets.QPushButton(self.centralwidget)
        self.withdraw_button.setGeometry(QtCore.QRect(134, 130, 99, 27))
        self.withdraw_button.setObjectName("withdraw_button")
        self.camera2 = QtWidgets.QFrame(self.centralwidget)
        self.camera2.setGeometry(QtCore.QRect(456, 12, 161, 151))
        self.camera2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camera2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camera2.setObjectName("camera2")
        self.camera1 = QtWidgets.QFrame(self.centralwidget)
        self.camera1.setGeometry(QtCore.QRect(280, 12, 161, 151))
        self.camera1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camera1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camera1.setObjectName("camera1")
        self.rate_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.rate_box.setGeometry(QtCore.QRect(126, 16, 51, 25))
        self.rate_box.setMaximumSize(QtCore.QSize(16777215, 16777214))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rate_box.setFont(font)
        self.rate_box.setDecimals(1)
        self.rate_box.setMaximum(10.0)
        self.rate_box.setSingleStep(0.1)
        self.rate_box.setProperty("value", 10.0)
        self.rate_box.setObjectName("rate_box")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(184, 20, 69, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.diameter_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.diameter_box.setGeometry(QtCore.QRect(126, 50, 51, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.diameter_box.setFont(font)
        self.diameter_box.setDecimals(1)
        self.diameter_box.setProperty("value", 14.0)
        self.diameter_box.setObjectName("diameter_box")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(182, 56, 91, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(8, 166, 781, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(262, 6, 16, 163))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.trial_run = QtWidgets.QFrame(self.centralwidget)
        self.trial_run.setGeometry(QtCore.QRect(422, 194, 357, 321))
        self.trial_run.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trial_run.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trial_run.setObjectName("trial_run")
        self.cummulative_run = QtWidgets.QFrame(self.centralwidget)
        self.cummulative_run.setGeometry(QtCore.QRect(632, 12, 153, 151))
        self.cummulative_run.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cummulative_run.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cummulative_run.setObjectName("cummulative_run")
        self.run_button = QtWidgets.QPushButton(self.centralwidget)
        self.run_button.setGeometry(QtCore.QRect(144, 462, 113, 47))
        self.run_button.setObjectName("run_button")
        self.num_trials_box = QtWidgets.QSpinBox(self.centralwidget)
        self.num_trials_box.setGeometry(QtCore.QRect(24, 404, 48, 27))
        self.num_trials_box.setProperty("value", 1)
        self.num_trials_box.setObjectName("num_trials_box")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(78, 410, 51, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.flush_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.flush_box.setGeometry(QtCore.QRect(24, 366, 69, 27))
        self.flush_box.setDecimals(1)
        self.flush_box.setProperty("value", 5.0)
        self.flush_box.setObjectName("flush_box")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(102, 372, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.stim_box_label = QtWidgets.QLabel(self.centralwidget)
        self.stim_box_label.setGeometry(QtCore.QRect(102, 340, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.stim_box_label.setFont(font)
        self.stim_box_label.setObjectName("stim_box_label")
        self.stim_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.stim_box.setGeometry(QtCore.QRect(24, 334, 69, 27))
        self.stim_box.setDecimals(1)
        self.stim_box.setProperty("value", 15.0)
        self.stim_box.setObjectName("stim_box")
        self.pre_stim_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.pre_stim_box.setGeometry(QtCore.QRect(24, 302, 69, 27))
        self.pre_stim_box.setDecimals(1)
        self.pre_stim_box.setProperty("value", 5.0)
        self.pre_stim_box.setObjectName("pre_stim_box")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(102, 306, 85, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.experimental_dir_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.experimental_dir_text.setGeometry(QtCore.QRect(22, 252, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.experimental_dir_text.setFont(font)
        self.experimental_dir_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.experimental_dir_text.setObjectName("experimental_dir_text")
        self.choose_dir_button = QtWidgets.QToolButton(self.centralwidget)
        self.choose_dir_button.setGeometry(QtCore.QRect(318, 250, 24, 25))
        self.choose_dir_button.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.choose_dir_button.setArrowType(QtCore.Qt.NoArrow)
        self.choose_dir_button.setObjectName("choose_dir_button")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(22, 234, 159, 17))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(208, 410, 89, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.trial_period_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.trial_period_box.setGeometry(QtCore.QRect(134, 406, 69, 27))
        self.trial_period_box.setDecimals(1)
        self.trial_period_box.setProperty("value", 10.0)
        self.trial_period_box.setObjectName("trial_period_box")
        self.stim_type = QtWidgets.QComboBox(self.centralwidget)
        self.stim_type.setGeometry(QtCore.QRect(196, 302, 109, 27))
        self.stim_type.setObjectName("stim_type")
        self.stim_type.addItem("")
        self.stim_type.addItem("")
        self.stim_type.addItem("")
        self.stim_type.addItem("")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(314, 306, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        FlyTracker.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FlyTracker)
        self.statusbar.setObjectName("statusbar")
        FlyTracker.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(FlyTracker)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 794, 25))
        self.menubar.setObjectName("menubar")
        FlyTracker.setMenuBar(self.menubar)

        self.retranslateUi(FlyTracker)
        QtCore.QMetaObject.connectSlotsByName(FlyTracker)
        FlyTracker.setTabOrder(self.start_button, self.infuse_button)
        FlyTracker.setTabOrder(self.infuse_button, self.withdraw_button)
        FlyTracker.setTabOrder(self.withdraw_button, self.stop_button)

    def retranslateUi(self, FlyTracker):
        _translate = QtCore.QCoreApplication.translate
        FlyTracker.setWindowTitle(_translate("FlyTracker", "MainWindow"))
        self.start_button.setText(_translate("FlyTracker", "Start"))
        self.stop_button.setText(_translate("FlyTracker", "Stop"))
        self.infuse_button.setText(_translate("FlyTracker", "Infuse"))
        self.withdraw_button.setText(_translate("FlyTracker", "Withdraw"))
        self.label.setText(_translate("FlyTracker", "Rate (mL/h)"))
        self.label_2.setText(_translate("FlyTracker", "Diameter (mm)"))
        self.run_button.setText(_translate("FlyTracker", "Run"))
        self.label_3.setText(_translate("FlyTracker", "# Trials"))
        self.label_4.setText(_translate("FlyTracker", "Flush (s)"))
        self.stim_box_label.setText(_translate("FlyTracker", "Stim (s)"))
        self.label_6.setText(_translate("FlyTracker", "Pre stim (s)"))
        self.choose_dir_button.setText(_translate("FlyTracker", "..."))
        self.label_7.setText(_translate("FlyTracker", "Experiment directory:"))
        self.label_8.setText(_translate("FlyTracker", "Trial Period (s)"))
        self.stim_type.setItemText(0, _translate("FlyTracker", "Both Air"))
        self.stim_type.setItemText(1, _translate("FlyTracker", "Both Odor"))
        self.stim_type.setItemText(2, _translate("FlyTracker", "Left Odor"))
        self.stim_type.setItemText(3, _translate("FlyTracker", "Right Odor"))
        self.label_5.setText(_translate("FlyTracker", "Stim Type"))

