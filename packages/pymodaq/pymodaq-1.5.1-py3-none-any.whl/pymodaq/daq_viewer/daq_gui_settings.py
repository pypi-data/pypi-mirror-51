# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'daq_gui_settings.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(636, 590)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout.setObjectName("settings_layout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.title_label = QtWidgets.QLabel(Form)
        self.title_label.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout_4.addWidget(self.title_label)
        self.command_widget = QtWidgets.QWidget(Form)
        self.command_widget.setMaximumSize(QtCore.QSize(16777215, 30))
        self.command_widget.setObjectName("command_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.command_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.grab_pb = QtWidgets.QPushButton(self.command_widget)
        self.grab_pb.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/run2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.grab_pb.setIcon(icon)
        self.grab_pb.setCheckable(True)
        self.grab_pb.setObjectName("grab_pb")
        self.horizontalLayout_2.addWidget(self.grab_pb)
        self.single_pb = QtWidgets.QPushButton(self.command_widget)
        self.single_pb.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/snap.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.single_pb.setIcon(icon1)
        self.single_pb.setCheckable(False)
        self.single_pb.setObjectName("single_pb")
        self.horizontalLayout_2.addWidget(self.single_pb)
        self.stop_pb = QtWidgets.QPushButton(self.command_widget)
        self.stop_pb.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_pb.setIcon(icon2)
        self.stop_pb.setCheckable(False)
        self.stop_pb.setObjectName("stop_pb")
        self.horizontalLayout_2.addWidget(self.stop_pb)
        self.save_current_pb = QtWidgets.QPushButton(self.command_widget)
        self.save_current_pb.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/SaveAs.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_current_pb.setIcon(icon3)
        self.save_current_pb.setObjectName("save_current_pb")
        self.horizontalLayout_2.addWidget(self.save_current_pb)
        self.save_new_pb = QtWidgets.QPushButton(self.command_widget)
        self.save_new_pb.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Snap&Save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_new_pb.setIcon(icon4)
        self.save_new_pb.setObjectName("save_new_pb")
        self.horizontalLayout_2.addWidget(self.save_new_pb)
        self.load_data_pb = QtWidgets.QPushButton(self.command_widget)
        self.load_data_pb.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.load_data_pb.setIcon(icon5)
        self.load_data_pb.setObjectName("load_data_pb")
        self.horizontalLayout_2.addWidget(self.load_data_pb)
        self.settings_pb = QtWidgets.QPushButton(self.command_widget)
        self.settings_pb.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/HLM.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_pb.setIcon(icon6)
        self.settings_pb.setCheckable(True)
        self.settings_pb.setObjectName("settings_pb")
        self.horizontalLayout_2.addWidget(self.settings_pb)
        self.update_com_pb = QtWidgets.QPushButton(self.command_widget)
        self.update_com_pb.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Refresh2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.update_com_pb.setIcon(icon7)
        self.update_com_pb.setCheckable(False)
        self.update_com_pb.setObjectName("update_com_pb")
        self.horizontalLayout_2.addWidget(self.update_com_pb)
        self.navigator_pb = QtWidgets.QPushButton(self.command_widget)
        self.navigator_pb.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Select_24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.navigator_pb.setIcon(icon8)
        self.navigator_pb.setObjectName("navigator_pb")
        self.horizontalLayout_2.addWidget(self.navigator_pb)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addWidget(self.command_widget)
        self.settings_widget = QtWidgets.QWidget(Form)
        self.settings_widget.setObjectName("settings_widget")
        self.settings_layout_2 = QtWidgets.QVBoxLayout(self.settings_widget)
        self.settings_layout_2.setContentsMargins(0, 0, 0, 0)
        self.settings_layout_2.setSpacing(0)
        self.settings_layout_2.setObjectName("settings_layout_2")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.settings_widget)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 3)
        self.DAQ_type_combo = QtWidgets.QComboBox(self.settings_widget)
        self.DAQ_type_combo.setObjectName("DAQ_type_combo")
        self.DAQ_type_combo.addItem("")
        self.DAQ_type_combo.addItem("")
        self.DAQ_type_combo.addItem("")
        self.gridLayout_3.addWidget(self.DAQ_type_combo, 0, 3, 1, 3)
        self.label_4 = QtWidgets.QLabel(self.settings_widget)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 3)
        self.Quit_pb = QtWidgets.QPushButton(self.settings_widget)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/close2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Quit_pb.setIcon(icon9)
        self.Quit_pb.setObjectName("Quit_pb")
        self.gridLayout_3.addWidget(self.Quit_pb, 4, 0, 1, 2)
        self.Detector_type_combo = QtWidgets.QComboBox(self.settings_widget)
        self.Detector_type_combo.setObjectName("Detector_type_combo")
        self.gridLayout_3.addWidget(self.Detector_type_combo, 1, 3, 1, 3)
        self.load_settings_pb = QtWidgets.QPushButton(self.settings_widget)
        self.load_settings_pb.setIcon(icon5)
        self.load_settings_pb.setObjectName("load_settings_pb")
        self.gridLayout_3.addWidget(self.load_settings_pb, 7, 0, 3, 3)
        self.save_settings_pb = QtWidgets.QPushButton(self.settings_widget)
        self.save_settings_pb.setIcon(icon3)
        self.save_settings_pb.setObjectName("save_settings_pb")
        self.gridLayout_3.addWidget(self.save_settings_pb, 7, 3, 3, 3)
        self.take_bkg_cb = QtWidgets.QCheckBox(self.settings_widget)
        self.take_bkg_cb.setObjectName("take_bkg_cb")
        self.gridLayout_3.addWidget(self.take_bkg_cb, 5, 3, 2, 3)
        self.do_bkg_cb = QtWidgets.QCheckBox(self.settings_widget)
        self.do_bkg_cb.setObjectName("do_bkg_cb")
        self.gridLayout_3.addWidget(self.do_bkg_cb, 5, 0, 2, 3)
        self.Ini_state_LED = QLED(self.settings_widget)
        self.Ini_state_LED.setObjectName("Ini_state_LED")
        self.gridLayout_3.addWidget(self.Ini_state_LED, 4, 4, 1, 1)
        self.data_ready_led = QLED(self.settings_widget)
        self.data_ready_led.setObjectName("data_ready_led")
        self.gridLayout_3.addWidget(self.data_ready_led, 4, 5, 1, 1)
        self.IniDet_pb = QtWidgets.QPushButton(self.settings_widget)
        self.IniDet_pb.setCheckable(True)
        self.IniDet_pb.setChecked(False)
        self.IniDet_pb.setObjectName("IniDet_pb")
        self.gridLayout_3.addWidget(self.IniDet_pb, 4, 2, 1, 2)
        self.settings_layout_2.addLayout(self.gridLayout_3)
        self.verticalLayout_4.addWidget(self.settings_widget)
        self.settings_layout.addLayout(self.verticalLayout_4)
        self.gridLayout.addLayout(self.settings_layout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.title_label.setText(_translate("Form", "DAQ Title"))
        self.grab_pb.setToolTip(_translate("Form", "Grab"))
        self.single_pb.setToolTip(_translate("Form", "Single Grab"))
        self.stop_pb.setToolTip(_translate("Form", "Single Grab"))
        self.save_current_pb.setToolTip(_translate("Form", "Save Current Data"))
        self.save_new_pb.setToolTip(_translate("Form", "Save New Data"))
        self.settings_pb.setToolTip(_translate("Form", "Open Settings"))
        self.update_com_pb.setToolTip(_translate("Form", "Refresh Hardware"))
        self.navigator_pb.setToolTip(_translate("Form", "Send current data to navigator"))
        self.label_3.setText(_translate("Form", "Detector:"))
        self.DAQ_type_combo.setToolTip(_translate("Form", "Detector Type"))
        self.DAQ_type_combo.setItemText(0, _translate("Form", "DAQ0D"))
        self.DAQ_type_combo.setItemText(1, _translate("Form", "DAQ1D"))
        self.DAQ_type_combo.setItemText(2, _translate("Form", "DAQ2D"))
        self.label_4.setText(_translate("Form", "DAQ type:"))
        self.Quit_pb.setToolTip(_translate("Form", "quit and close the viewer"))
        self.Quit_pb.setText(_translate("Form", "Quit"))
        self.Detector_type_combo.setToolTip(_translate("Form", "Stage Type"))
        self.load_settings_pb.setToolTip(_translate("Form", "Load settings"))
        self.load_settings_pb.setText(_translate("Form", "Sett."))
        self.save_settings_pb.setToolTip(_translate("Form", "save settings"))
        self.save_settings_pb.setText(_translate("Form", "Sett."))
        self.take_bkg_cb.setText(_translate("Form", "Take Bkg"))
        self.do_bkg_cb.setText(_translate("Form", "Do Bkg sub."))
        self.Ini_state_LED.setToolTip(_translate("Form", "Green when controller is initialized"))
        self.Ini_state_LED.setText(_translate("Form", "TextLabel"))
        self.data_ready_led.setToolTip(_translate("Form", "Green when data ready"))
        self.data_ready_led.setText(_translate("Form", "TextLabel"))
        self.IniDet_pb.setToolTip(_translate("Form", "To initialize the detector"))
        self.IniDet_pb.setText(_translate("Form", "Ini. Det."))

from pymodaq.daq_utils.plotting.QLED.qled import QLED
from pymodaq.QtDesigner_Ressources import QtDesigner_ressources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

