# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fused.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FusedDialog(object):
    def setupUi(self, FusedDialog):
        FusedDialog.setObjectName("FusedDialog")
        FusedDialog.resize(385, 413)
        self.verticalLayout = QtWidgets.QVBoxLayout(FusedDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_4 = QtWidgets.QWidget(FusedDialog)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_7 = QtWidgets.QLabel(self.widget_4)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.check_num_input = QtWidgets.QLineEdit(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.check_num_input.sizePolicy().hasHeightForWidth())
        self.check_num_input.setSizePolicy(sizePolicy)
        self.check_num_input.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.check_num_input.setClearButtonEnabled(False)
        self.check_num_input.setObjectName("check_num_input")
        self.horizontalLayout.addWidget(self.check_num_input)
        self.horizontalLayout.setStretch(0, 3)
        self.verticalLayout.addWidget(self.widget_4)
        self.widget_5 = QtWidgets.QWidget(FusedDialog)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_8 = QtWidgets.QLabel(self.widget_5)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.reproj_error_input = QtWidgets.QLineEdit(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reproj_error_input.sizePolicy().hasHeightForWidth())
        self.reproj_error_input.setSizePolicy(sizePolicy)
        self.reproj_error_input.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.reproj_error_input.setClearButtonEnabled(False)
        self.reproj_error_input.setObjectName("reproj_error_input")
        self.horizontalLayout_2.addWidget(self.reproj_error_input)
        self.horizontalLayout_2.setStretch(0, 3)
        self.verticalLayout.addWidget(self.widget_5)
        self.widget_6 = QtWidgets.QWidget(FusedDialog)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.widget_6)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.depth_error_input = QtWidgets.QLineEdit(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.depth_error_input.sizePolicy().hasHeightForWidth())
        self.depth_error_input.setSizePolicy(sizePolicy)
        self.depth_error_input.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.depth_error_input.setClearButtonEnabled(False)
        self.depth_error_input.setObjectName("depth_error_input")
        self.horizontalLayout_3.addWidget(self.depth_error_input)
        self.horizontalLayout_3.setStretch(0, 3)
        self.verticalLayout.addWidget(self.widget_6)
        self.widget_7 = QtWidgets.QWidget(FusedDialog)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_10 = QtWidgets.QLabel(self.widget_7)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)
        self.normal_error_input = QtWidgets.QLineEdit(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.normal_error_input.sizePolicy().hasHeightForWidth())
        self.normal_error_input.setSizePolicy(sizePolicy)
        self.normal_error_input.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.normal_error_input.setClearButtonEnabled(False)
        self.normal_error_input.setObjectName("normal_error_input")
        self.horizontalLayout_4.addWidget(self.normal_error_input)
        self.horizontalLayout_4.setStretch(0, 3)
        self.verticalLayout.addWidget(self.widget_7)
        self.widget_3 = QtWidgets.QWidget(FusedDialog)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.fuseStartBtn = QtWidgets.QPushButton(self.widget_3)
        self.fuseStartBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fuseStartBtn.setObjectName("fuseStartBtn")
        self.horizontalLayout_6.addWidget(self.fuseStartBtn)
        self.verticalLayout.addWidget(self.widget_3)

        self.retranslateUi(FusedDialog)
        QtCore.QMetaObject.connectSlotsByName(FusedDialog)

    def retranslateUi(self, FusedDialog):
        _translate = QtCore.QCoreApplication.translate
        FusedDialog.setWindowTitle(_translate("FusedDialog", "Dialog"))
        self.label_7.setText(_translate("FusedDialog", "一致性图像数："))
        self.label_8.setText(_translate("FusedDialog", "重投影误差阈值："))
        self.label_9.setText(_translate("FusedDialog", "深度误差阈值："))
        self.label_10.setText(_translate("FusedDialog", "法向量阈值："))
        self.fuseStartBtn.setText(_translate("FusedDialog", "Fused Start"))
