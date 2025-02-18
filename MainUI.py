# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 653)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.graphicsView = QtWidgets.QGraphicsView(self.frame_2)
        self.graphicsView.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.graphicsView.setAcceptDrops(False)
        self.graphicsView.setObjectName("graphicsView")
        self.browser = QWebEngineView()
        self.browser.load(QUrl('http://219.147.11.106:18011/Project/DataManagement.html'))
        #self.browser.load(QUrl('http://www.baidu.com'))
        self.browser.setZoomFactor(0.5)
        self.horizontalLayout_4.addWidget(self.browser)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.LogFrame = QtWidgets.QFrame(self.frame_4)
        self.LogFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.LogFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LogFrame.setObjectName("LogFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.LogFrame)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.LogFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet("background-color: rgb(222, 221, 221);\n"
"color: rgb(0, 0, 0);")
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.LogScrollArea = QtWidgets.QScrollArea(self.LogFrame)
        self.LogScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.LogScrollArea.setWidgetResizable(True)
        self.LogScrollArea.setObjectName("LogScrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 230, 298))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.logTextBrowser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents_2)
        self.logTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.logTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.logTextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.logTextBrowser.setObjectName("logTextBrowser")
        self.logTextBrowser.setReadOnly(False)
        self.verticalLayout_5.addWidget(self.logTextBrowser)
        self.LogScrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.addWidget(self.LogScrollArea)
        self.verticalLayout_4.setStretch(1, 9)
        self.verticalLayout_2.addWidget(self.LogFrame)
        self.frame_7 = QtWidgets.QFrame(self.frame_4)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.pbar = QtWidgets.QProgressBar(self.LogFrame)
        self.pbar.setObjectName("progressBar")
        self.verticalLayout_4.addWidget(self.pbar)
        self.verticalLayout_4.setStretch(1,9)
        self.comboBox = QtWidgets.QComboBox(self.frame_7)
        self.comboBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setEditable(True)
        self.comboBox.setMaxVisibleItems(4)
        self.comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox.setMinimumContentsLength(4)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.horizontalLayout_7.addWidget(self.comboBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.horizontalLayout_7.setStretch(0, 3)
        self.horizontalLayout_7.setStretch(1, 5)
        self.horizontalLayout_7.setStretch(2, 3)
        self.verticalLayout_2.addWidget(self.frame_7)
        self.verticalLayout_2.setStretch(0, 9)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout.addWidget(self.frame_4)
        self.ImageListFrame = QtWidgets.QFrame(self.frame_3)
        self.ImageListFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ImageListFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ImageListFrame.setObjectName("ImageListFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.ImageListFrame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.ImageListFrame)
        self.label_2.setStyleSheet("background-color: rgb(222, 221, 221);\n"
"color: rgb(0, 0, 0);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.ImageLIstScrollArea = QtWidgets.QScrollArea(self.ImageListFrame)
        self.ImageLIstScrollArea.setWidgetResizable(True)
        self.ImageLIstScrollArea.setObjectName("ImageLIstScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 232, 217))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.textBrowser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setReadOnly(False)
        self.horizontalLayout_5.addWidget(self.textBrowser)
        self.ImageLIstScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.ImageLIstScrollArea)
        self.verticalLayout.addWidget(self.ImageListFrame)
        self.verticalLayout.setStretch(0, 6)
        self.verticalLayout.setStretch(1, 4)
        self.horizontalLayout_2.addWidget(self.frame_3)
        self.horizontalLayout_2.setStretch(0, 7)
        self.horizontalLayout_2.setStretch(1, 3)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        openAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/open.png'), 'Exit', self)
        self.toolBar = self.addToolBar('open')
        self.toolBar.addAction(openAction)
        SaveAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/Save.png'), 'Save', self)
        self.toolBar = self.addToolBar('Save')
        self.toolBar.addAction(SaveAction)
        StartAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/Start.png'), 'Start', self)
        self.toolBar = self.addToolBar('Start')
        self.toolBar.addAction(StartAction)
        PauseAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/Pause.png'), 'Pause', self)
        self.toolBar = self.addToolBar('Pause')
        self.toolBar.addAction(PauseAction)
        exitAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/Stop.png'), 'Exit', self)
        self.toolBar = self.addToolBar('Exit')
        self.toolBar.addAction(exitAction)
        ShowAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/Show.png'), 'Show', self)
        self.toolBar = self.addToolBar('Show')
        self.toolBar.addAction(ShowAction)
        LargeAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/Large.png'), 'Large', self)
        self.toolBar = self.addToolBar('Large')
        self.toolBar.addAction(LargeAction)
        SmallAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/Small.png'), 'Small', self)
        self.toolBar = self.addToolBar('Small')
        self.toolBar.addAction(SmallAction)
        MoveAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/Move.png'), 'Move', self)
        self.toolBar = self.addToolBar('Move')
        self.toolBar.addAction(MoveAction)
        SelectAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/Select.png'), 'Select', self)
        self.toolBar = self.addToolBar('Select')
        self.toolBar.addAction(SelectAction)
        settingAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/setting.png'), 'setting', self)
        self.toolBar = self.addToolBar('setting')
        self.toolBar.addAction(settingAction)
#        exitAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/open.png'), 'Exit', self)
#        self.toolBar.addAction('Exit')
#        exitAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/open.png'), 'Exit', self)
#        self.toolBar.addAction('Exit')
#        exitAction = QAction(QIcon('/home/hadoop/scx/GUI/Icon/open.png'), 'Exit', self)
#        self.toolBar.addAction('Exit')
	
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage("当前运行时间： 127 min")
        self.version_label = QtWidgets.QLabel('verison: 京航智科三维重建工具 1.0.0')
        self.statusbar.addPermanentWidget(self.version_label, stretch = 0)
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        self.menubar.setDefaultUp(True)
        self.menubar.setObjectName("menubar")
        self.StartMenu = QtWidgets.QMenu(self.menubar)
        self.StartMenu.setObjectName("StartMenu")
        self.SpareReconstructionMenu = QtWidgets.QMenu(self.menubar)
        self.SpareReconstructionMenu.setObjectName("SpareReconstructionMenu")
        self.DenseReconstructionMenu = QtWidgets.QMenu(self.menubar)
        self.DenseReconstructionMenu.setObjectName("DenseReconstructionMenu")
        self.MeshMenu = QtWidgets.QMenu(self.menubar)
        self.MeshMenu.setObjectName("MeshMenu")
        self.AutoReconstructionMenu = QtWidgets.QMenu(self.menubar)
        self.AutoReconstructionMenu.setObjectName("AutoReconstructionMenu")
        MainWindow.setMenuBar(self.menubar)
        self.FeatureExtractorAction = QtWidgets.QAction(MainWindow)
        self.FeatureExtractorAction.setObjectName("FeatureExtractorAction")
        self.MatchingAction = QtWidgets.QAction(MainWindow)
        self.MatchingAction.setObjectName("MatchingAction")
        self.BAAction = QtWidgets.QAction(MainWindow)
        self.BAAction.setObjectName("BAAction")
        self.MergeAction = QtWidgets.QAction(MainWindow)
        self.MergeAction.setObjectName("MergeAction")
        self.AutoSparseAction = QtWidgets.QAction(MainWindow)
        self.AutoSparseAction.setObjectName("AutoSparseAction")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.PartAction = QtWidgets.QAction(MainWindow)
        self.PartAction.setCheckable(False)
        self.PartAction.setObjectName("PartAction")
        self.PatchMatchAction = QtWidgets.QAction(MainWindow)
        self.PatchMatchAction.setCheckable(False)
        self.PatchMatchAction.setObjectName("PatchMatchAction")
        self.ReconstructionAction = QtWidgets.QAction(MainWindow)
        self.ReconstructionAction.setObjectName("ReconstructionAction")
        self.RefineAction = QtWidgets.QAction(MainWindow)
        self.RefineAction.setObjectName("RefineAction")
        self.SimplifyAction = QtWidgets.QAction(MainWindow)
        self.SimplifyAction.setObjectName("SimplifyAction")
        self.AutoReconstructionAction = QtWidgets.QAction(MainWindow)
        self.AutoReconstructionAction.setObjectName("AutoReconstructionAction")
        self.SuperParaSettingAction = QtWidgets.QAction(MainWindow)
        self.SuperParaSettingAction.setObjectName("SuperParaSettingAction")
        self.action_12 = QtWidgets.QAction(MainWindow)
        self.action_12.setObjectName("action_12")
        self.FusedAction = QtWidgets.QAction(MainWindow)
        self.FusedAction.setObjectName("FusedAction")
        self.MergeAction_2 = QtWidgets.QAction(MainWindow)
        self.MergeAction_2.setObjectName("MergeAction_2")
        self.AutoDenseAction = QtWidgets.QAction(MainWindow)
        self.AutoDenseAction.setObjectName("AutoDenseAction")
        self.DenseParaSettingAction = QtWidgets.QAction(MainWindow)
        self.DenseParaSettingAction.setObjectName("DenseParaSettingAction")
        self.StartMenu.addAction(self.SuperParaSettingAction)
        self.SpareReconstructionMenu.addAction(self.FeatureExtractorAction)
        self.SpareReconstructionMenu.addAction(self.MatchingAction)
        self.SpareReconstructionMenu.addAction(self.BAAction)
        self.SpareReconstructionMenu.addAction(self.MergeAction)
        self.SpareReconstructionMenu.addAction(self.AutoSparseAction)
        self.DenseReconstructionMenu.addAction(self.PartAction)
        self.DenseReconstructionMenu.addAction(self.PatchMatchAction)
        self.DenseReconstructionMenu.addAction(self.FusedAction)
        self.DenseReconstructionMenu.addAction(self.MergeAction_2)
        self.DenseReconstructionMenu.addAction(self.AutoDenseAction)
        self.DenseReconstructionMenu.addAction(self.DenseParaSettingAction)
        self.MeshMenu.addAction(self.ReconstructionAction)
        self.MeshMenu.addAction(self.RefineAction)
        self.MeshMenu.addAction(self.SimplifyAction)
        self.AutoReconstructionMenu.addAction(self.AutoReconstructionAction)
        self.menubar.addAction(self.StartMenu.menuAction())
        self.menubar.addAction(self.SpareReconstructionMenu.menuAction())
        self.menubar.addAction(self.DenseReconstructionMenu.menuAction())
        self.menubar.addAction(self.MeshMenu.menuAction())
        self.menubar.addAction(self.AutoReconstructionMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.comboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Reconstruction"))
        self.label.setText(_translate("MainWindow", "Log"))
        self.comboBox.setCurrentText(_translate("MainWindow", "master"))
        self.comboBox.setItemText(0, _translate("MainWindow", "master"))
        self.label_2.setText(_translate("MainWindow", "Image List"))
        self.StartMenu.setTitle(_translate("MainWindow", "开始"))
        self.SpareReconstructionMenu.setTitle(_translate("MainWindow", "稀疏重建"))
        self.DenseReconstructionMenu.setTitle(_translate("MainWindow", "稠密重建"))
        self.MeshMenu.setTitle(_translate("MainWindow", "网格重建"))
        self.AutoReconstructionMenu.setTitle(_translate("MainWindow", "自动重建"))
        self.FeatureExtractorAction.setText(_translate("MainWindow", "特征匹配"))
        self.MatchingAction.setText(_translate("MainWindow", "Matching"))
        self.BAAction.setText(_translate("MainWindow", "BA"))
        self.MergeAction.setText(_translate("MainWindow", "Merge"))
        self.AutoSparseAction.setText(_translate("MainWindow", "自动稀疏重建"))
        self.action_3.setText(_translate("MainWindow", "输入图像"))
        self.action_4.setText(_translate("MainWindow", "输出模型"))
        self.PartAction.setText(_translate("MainWindow", "场景分块"))
        self.PatchMatchAction.setText(_translate("MainWindow", "深度图生成"))
        self.ReconstructionAction.setText(_translate("MainWindow", "网格重建"))
        self.RefineAction.setText(_translate("MainWindow", "网格优化"))
        self.SimplifyAction.setText(_translate("MainWindow", "网格简化"))
        self.AutoReconstructionAction.setText(_translate("MainWindow", "自动重建"))
        self.SuperParaSettingAction.setText(_translate("MainWindow", "超参数设置"))
        self.action_12.setText(_translate("MainWindow", "场景分块"))
        self.FusedAction.setText(_translate("MainWindow", "点云融合"))
        self.MergeAction_2.setText(_translate("MainWindow", "场景融合"))
        self.AutoDenseAction.setText(_translate("MainWindow", "自动稠密重建"))
        self.DenseParaSettingAction.setText(_translate("MainWindow", "Command Interface"))
