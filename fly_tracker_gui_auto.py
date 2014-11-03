# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fly_tracker_gui.ui'
#
# Created: Sun Nov  2 16:58:59 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FlyTracker(object):
    def setupUi(self, FlyTracker):
        FlyTracker.setObjectName("FlyTracker")
        FlyTracker.resize(1372, 886)
        FlyTracker.setMaximumSize(QtCore.QSize(140000, 140000))
        self.centralwidget = QtWidgets.QWidget(FlyTracker)
        self.centralwidget.setObjectName("centralwidget")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(16, 14, 111, 41))
        self.start_button.setObjectName("start_button")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(16, 64, 111, 41))
        self.stop_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.stop_button.setObjectName("stop_button")
        self.infuse_button = QtWidgets.QPushButton(self.centralwidget)
        self.infuse_button.setGeometry(QtCore.QRect(10, 208, 99, 27))
        self.infuse_button.setObjectName("infuse_button")
        self.withdraw_button = QtWidgets.QPushButton(self.centralwidget)
        self.withdraw_button.setGeometry(QtCore.QRect(10, 246, 99, 27))
        self.withdraw_button.setObjectName("withdraw_button")
        self.camera2 = QtWidgets.QFrame(self.centralwidget)
        self.camera2.setGeometry(QtCore.QRect(484, 24, 300, 300))
        self.camera2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camera2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camera2.setObjectName("camera2")
        self.camera1 = QtWidgets.QFrame(self.centralwidget)
        self.camera1.setGeometry(QtCore.QRect(174, 24, 300, 300))
        self.camera1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camera1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camera1.setObjectName("camera1")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(64, 126, 93, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.syringe_size_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.syringe_size_box.setGeometry(QtCore.QRect(6, 156, 51, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.syringe_size_box.setFont(font)
        self.syringe_size_box.setDecimals(1)
        self.syringe_size_box.setProperty("value", 30.0)
        self.syringe_size_box.setObjectName("syringe_size_box")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(62, 162, 97, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(156, 12, 16, 329))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.trial_run2 = QtWidgets.QFrame(self.centralwidget)
        self.trial_run2.setGeometry(QtCore.QRect(502, 380, 400, 467))
        self.trial_run2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trial_run2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trial_run2.setObjectName("trial_run2")
        self.cummulative_run = QtWidgets.QFrame(self.centralwidget)
        self.cummulative_run.setGeometry(QtCore.QRect(810, 4, 317, 319))
        self.cummulative_run.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cummulative_run.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cummulative_run.setObjectName("cummulative_run")
        self.run_button = QtWidgets.QPushButton(self.centralwidget)
        self.run_button.setGeometry(QtCore.QRect(136, 712, 157, 59))
        self.run_button.setObjectName("run_button")
        self.num_trials_box = QtWidgets.QSpinBox(self.centralwidget)
        self.num_trials_box.setGeometry(QtCore.QRect(16, 590, 91, 27))
        self.num_trials_box.setMaximum(1000)
        self.num_trials_box.setProperty("value", 1)
        self.num_trials_box.setObjectName("num_trials_box")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(116, 596, 51, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.flush_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.flush_box.setGeometry(QtCore.QRect(16, 552, 69, 27))
        self.flush_box.setDecimals(1)
        self.flush_box.setProperty("value", 5.0)
        self.flush_box.setObjectName("flush_box")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(94, 558, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.stim_box_label = QtWidgets.QLabel(self.centralwidget)
        self.stim_box_label.setGeometry(QtCore.QRect(94, 526, 67, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.stim_box_label.setFont(font)
        self.stim_box_label.setObjectName("stim_box_label")
        self.stim_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.stim_box.setGeometry(QtCore.QRect(16, 520, 69, 27))
        self.stim_box.setDecimals(1)
        self.stim_box.setProperty("value", 10.0)
        self.stim_box.setObjectName("stim_box")
        self.pre_stim_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.pre_stim_box.setGeometry(QtCore.QRect(16, 488, 69, 27))
        self.pre_stim_box.setDecimals(1)
        self.pre_stim_box.setProperty("value", 5.0)
        self.pre_stim_box.setObjectName("pre_stim_box")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(94, 492, 85, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.experimental_dir_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.experimental_dir_text.setGeometry(QtCore.QRect(18, 436, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.experimental_dir_text.setFont(font)
        self.experimental_dir_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.experimental_dir_text.setObjectName("experimental_dir_text")
        self.choose_dir_button = QtWidgets.QToolButton(self.centralwidget)
        self.choose_dir_button.setGeometry(QtCore.QRect(314, 434, 24, 25))
        self.choose_dir_button.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.choose_dir_button.setArrowType(QtCore.Qt.NoArrow)
        self.choose_dir_button.setObjectName("choose_dir_button")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(18, 418, 159, 17))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(264, 596, 109, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.trial_period_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.trial_period_box.setGeometry(QtCore.QRect(190, 592, 69, 27))
        self.trial_period_box.setDecimals(1)
        self.trial_period_box.setProperty("value", 10.0)
        self.trial_period_box.setObjectName("trial_period_box")
        self.stim_type = QtWidgets.QComboBox(self.centralwidget)
        self.stim_type.setGeometry(QtCore.QRect(12, 638, 108, 27))
        self.stim_type.setObjectName("stim_type")
        self.stim_type.addItem("")
        self.stim_type.addItem("")
        self.stim_type.addItem("")
        self.stim_type.addItem("")
        self.stim_type.addItem("")
        self.stim_type.addItem("")
        self.stim_type.addItem("")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(130, 644, 66, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.trial_run1 = QtWidgets.QFrame(self.centralwidget)
        self.trial_run1.setGeometry(QtCore.QRect(932, 380, 401, 467))
        self.trial_run1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trial_run1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trial_run1.setObjectName("trial_run1")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(454, 384, 16, 473))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(792, 10, 16, 329))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.polar_plot_1 = QtWidgets.QFrame(self.centralwidget)
        self.polar_plot_1.setGeometry(QtCore.QRect(1132, 6, 219, 317))
        self.polar_plot_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.polar_plot_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.polar_plot_1.setObjectName("polar_plot_1")
        self.max_velocity = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.max_velocity.setGeometry(QtCore.QRect(1134, 328, 127, 27))
        self.max_velocity.setMaximum(1000000000.0)
        self.max_velocity.setProperty("value", 2000.0)
        self.max_velocity.setObjectName("max_velocity")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(1280, 334, 73, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.rate_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.rate_box.setGeometry(QtCore.QRect(6, 122, 53, 27))
        self.rate_box.setDecimals(1)
        self.rate_box.setProperty("value", 10.0)
        self.rate_box.setObjectName("rate_box")
        self.stim_prate_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.stim_prate_box.setGeometry(QtCore.QRect(188, 522, 67, 27))
        self.stim_prate_box.setProperty("value", 8.0)
        self.stim_prate_box.setObjectName("stim_prate_box")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(264, 526, 145, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.flush_prate_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.flush_prate_box.setGeometry(QtCore.QRect(188, 556, 67, 27))
        self.flush_prate_box.setProperty("value", 10.0)
        self.flush_prate_box.setObjectName("flush_prate_box")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(266, 560, 113, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        FlyTracker.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FlyTracker)
        self.statusbar.setObjectName("statusbar")
        FlyTracker.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(FlyTracker)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1372, 27))
        self.menubar.setObjectName("menubar")
        FlyTracker.setMenuBar(self.menubar)

        self.retranslateUi(FlyTracker)
        QtCore.QMetaObject.connectSlotsByName(FlyTracker)
        FlyTracker.setTabOrder(self.start_button, self.infuse_button)
        FlyTracker.setTabOrder(self.infuse_button, self.withdraw_button)
        FlyTracker.setTabOrder(self.withdraw_button, self.stop_button)

    def retranslateUi(self, FlyTracker):
        _translate = QtCore.QCoreApplication.translate
        FlyTracker.setWindowTitle(_translate("FlyTracker", "Fly Tracker"))
        self.start_button.setText(_translate("FlyTracker", "Start"))
        self.stop_button.setText(_translate("FlyTracker", "Stop"))
        self.infuse_button.setText(_translate("FlyTracker", "Infuse"))
        self.withdraw_button.setText(_translate("FlyTracker", "Withdraw"))
        self.label.setText(_translate("FlyTracker", "Rate (mL/min)"))
        self.label_2.setText(_translate("FlyTracker", "Syringe Size (mL)"))
        self.run_button.setText(_translate("FlyTracker", "Run"))
        self.label_3.setText(_translate("FlyTracker", "# Trials"))
        self.label_4.setText(_translate("FlyTracker", "Flush (s)"))
        self.stim_box_label.setText(_translate("FlyTracker", "Stim (s)"))
        self.label_6.setText(_translate("FlyTracker", "Pre stim (s)"))
        self.choose_dir_button.setText(_translate("FlyTracker", "..."))
        self.label_7.setText(_translate("FlyTracker", "Experiment directory:"))
        self.label_8.setText(_translate("FlyTracker", "Trial Period (s)"))
        self.stim_type.setItemText(0, _translate("FlyTracker", "Random"))
        self.stim_type.setItemText(1, _translate("FlyTracker", "Both_Air"))
        self.stim_type.setItemText(2, _translate("FlyTracker", "Both_Odor"))
        self.stim_type.setItemText(3, _translate("FlyTracker", "Left_Odor"))
        self.stim_type.setItemText(4, _translate("FlyTracker", "Right_Odor"))
        self.stim_type.setItemText(5, _translate("FlyTracker", "Left_Air"))
        self.stim_type.setItemText(6, _translate("FlyTracker", "Right_Air"))
        self.label_5.setText(_translate("FlyTracker", "Stim Type"))
        self.label_9.setText(_translate("FlyTracker", "Max velocity "))
        self.label_10.setText(_translate("FlyTracker", "Stim Rate (mL/min)"))
        self.label_11.setText(_translate("FlyTracker", "Flush rate (mL/min)"))

