import sys  
import os
import subprocess
import datetime
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *  
from MainUI import Ui_MainWindow
from SuperParaSettingDialog import Ui_SuperParaSettingDialog
from AutoSparseDialog import Ui_AutoSparseDialog
from AutoDenseDialog import Ui_AutoDenseDialog
from AutoMeshDialog import Ui_AutoMeshDialog
from AutoAllReDialog import Ui_AutoAllReDialog
from MeshReconstruction import MeshReconstruction
from SparseReconstruction import SparseReconstruction
from DenseReconstruction import DenseReconstruction
from DenseCommandInterface import Ui_DenseCmdDialog
from PartitionDialog import Ui_PartitionDialog
from PatchMatchDialog import Ui_PatchMatchDialog
from FusedDialog import Ui_FusedDialog
from MergeDialog import Ui_MergeDialog
#############################################Model###############################################

class SuperParaSetting:
	def __init__(self):
		self.machine_num = 0	

############################################# Dense Controller###########################################

class SuperParaSettingDialog(QDialog, Ui_SuperParaSettingDialog): 
	def __init__(self, mainWindow):
		super(SuperParaSettingDialog, self).__init__()
		self.setupUi(self)
		self.mainWindow = mainWindow
		self.ConfirmBtn.clicked.connect(self.returnPara)

	def returnPara(self):
			self.mainWindow.superParaSetting.machine_num = int(self.machine_num_input.text())
			
			self.close()
#			for i in range(0,100):
#				self.mainWindow.logTextBrowser.append(str(i) + "\n")
#			self.mainWindow.logTextBrowser.clear()
#			self.mainWindow.logTextBrowser.moveCursor(self.logTextBrowser.textCursor().End)
			self.mainWindow.statusbar.showMessage("指定机器数为" + str(self.mainWindow.superParaSetting.machine_num) + "台")
			for i in range(0, self.mainWindow.superParaSetting.machine_num - 1):
				self.mainWindow.comboBox.addItem('slave' + str(i + 1))

class AutoAllReDialog(QDialog, Ui_AutoAllReDialog):
	def __init__(self, mainWindow):
		super(AutoAllReDialog, self).__init__()
		self.setupUi(self)
		self.mainWindow = mainWindow
		self.autoDenseStartBtn.clicked.connect(self.startAllReconstruction)
		self.input_path_btn.clicked.connect(self.setInputpath)
		self.output_path_btn.clicked.connect(self.setOutputpath)
		#self.base_path_btn.clicked.connect(self.setBasepath)
		#self.autoTask.stateChanged.connect(self.checkboxHandle)
	def startAllReconstruction(self):
		self.mainWindow.statusbar.showMessage("开始自动重建")
		self.mainWindow.denseReconstruction.nParts = int(self.nparts_input.text())
		self.mainWindow.sparseReconstruction.execNum = self.mainWindow.superParaSetting.machine_num

		# if self.autoTask.isChecked():
		# 	self.mainWindow.denseReconstruction.autoGenerateTask()
		# else:
		# 	raw_task_str = self.task_input.text()
		# 	self.mainWindow.denseReconstruction.task_num_list = raw_task_str.split(',')
		# self.mainWindow.sparseReconstruction.
		
		# self.max_image_size = 2000
		# self.max_num_neighbors = 50
		# self.max_distance = 100
		# self.final_ba = 0
		# self.completeness_ratio = 0.5
		# self.max_local_ba_iterations = 6
		# self.max_global_ba_iterations = 2
		# self.ba_global_images_ratio = 1.3200000000000001
		# self.ba_global_points_ratio = 1.3200000000000001
		# self.ba_global_max_refinements = 2
		# self.num_workers = 8
		# self.num_images_ub = 100

		self.mainWindow.sparseReconstruction.quality = self.quality_input.currentText()
		image_num_obj = os.popen("ls -l " + self.mainWindow.sparseReconstruction.input_path + "|wc -l")
		image_num = image_num_obj.read().strip()
		#print("ls -l " + self.mainWindow.sparseReconstruction.input_path + "|wc -l")
		# print(image_num)
		# print(int(int(image_num) / (int(self.nparts_input.text())-1)))
		# temp = 1/0
		#print(self.quality_input.currentText())
		if self.quality_input.currentText() == "low" :
			self.mainWindow.sparseReconstruction.max_image_size = 1000
			self.mainWindow.sparseReconstruction.max_num_neighbors =50
			self.mainWindow.sparseReconstruction.max_distance = 100
			self.mainWindow.sparseReconstruction.final_ba =0
			self.mainWindow.sparseReconstruction.completeness_ratio = 0.5
			self.mainWindow.sparseReconstruction.max_local_ba_iterations = 6
			self.mainWindow.sparseReconstruction.max_global_ba_iterations = 2
			self.mainWindow.sparseReconstruction.ba_global_images_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_points_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_max_refinements =2
			self.mainWindow.sparseReconstruction.num_workers =8
			self.mainWindow.sparseReconstruction.num_images_ub =int(int(image_num) / (int(self.nparts_input.text())-1))
		elif self.quality_input.currentText() == "Medium" :
			self.mainWindow.sparseReconstruction.max_image_size = 3200
			self.mainWindow.sparseReconstruction.max_num_neighbors =100
			self.mainWindow.sparseReconstruction.max_distance = 100
			self.mainWindow.sparseReconstruction.final_ba =1
			self.mainWindow.sparseReconstruction.completeness_ratio = 0.6
			self.mainWindow.sparseReconstruction.max_local_ba_iterations = 15
			self.mainWindow.sparseReconstruction.max_global_ba_iterations = 30
			self.mainWindow.sparseReconstruction.ba_global_images_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_points_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_max_refinements =3
			self.mainWindow.sparseReconstruction.num_workers =8
			self.mainWindow.sparseReconstruction.num_images_ub =int(int(image_num) / (int(self.nparts_input.text())-1))
		elif self.quality_input.currentText() == "High" :
			self.mainWindow.sparseReconstruction.max_image_size = 3200
			self.mainWindow.sparseReconstruction.max_num_neighbors =200
			self.mainWindow.sparseReconstruction.max_distance = 100
			self.mainWindow.sparseReconstruction.final_ba =1
			self.mainWindow.sparseReconstruction.completeness_ratio = 0.7
			self.mainWindow.sparseReconstruction.max_local_ba_iterations = 30
			self.mainWindow.sparseReconstruction.max_global_ba_iterations = 75
			self.mainWindow.sparseReconstruction.ba_global_images_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_points_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_max_refinements =3
			self.mainWindow.sparseReconstruction.num_workers =8
			self.mainWindow.sparseReconstruction.num_images_ub =int(int(image_num) / (int(self.nparts_input.text())-1))
		else :
			print("yq else")
		# self.mainWindow.denseReconstruction.window_radius = 4
		# self.mainWindow.denseReconstruction.window_step = 2
		# self.mainWindow.denseReconstruction.num_samples = 7
		# self.mainWindow.denseReconstruction.num_iterations = 3
		# self.mainWindow.denseReconstruction.geom_consistency = "false"
		
		# self.mainWindow.denseReconstruction.check_num_images = 25
		# self.mainWindow.denseReconstruction.max_reproj_error = 2
		# self.mainWindow.denseReconstruction.max_depth_error = 0.01
		# self.mainWindow.denseReconstruction.max_normal_error = 10

		# self.mainWindow.denseReconstruction.merge_archive_type = 1
		self.mainWindow.sparseReconstruction.basepath = self.mainWindow.sparseReconstruction.output_path

		#######################################################SCX###################################################
		self.mainWindow.statusbar.showMessage("开始自动稠密重建")
		self.mainWindow.denseReconstruction.nParts = int(self.nparts_input.text())
		self.mainWindow.denseReconstruction.execNum = self.mainWindow.superParaSetting.machine_num

		self.mainWindow.denseReconstruction.autoGenerateTask()

		self.mainWindow.denseReconstruction.resolution = 1000
		self.mainWindow.denseReconstruction.min_resolution = 320
		self.mainWindow.denseReconstruction.res_level = 4
		self.mainWindow.denseReconstruction.part_archive_type = 1


		self.mainWindow.denseReconstruction.basepath = self.mainWindow.sparseReconstruction.output_path
		self.mainWindow.denseReconstruction.input_path = self.mainWindow.sparseReconstruction.output_path + "/0/"
		self.mainWindow.denseReconstruction.output_path = "/home/hadoop/scx/Distribute/Scene/Re/"

		self.mainWindow.denseReconstruction.outputdir = self.mainWindow.denseReconstruction.output_path + "/"
		self.mainWindow.denseReconstruction.pairpath = "/home/hadoop/GUI_master/"
		self.mainWindow.denseReconstruction.logdirpath = self.mainWindow.denseReconstruction.basepath + "/scx_log/"
		self.mainWindow.denseReconstruction.allmvsrepath = self.mainWindow.denseReconstruction.basepath + "/scx_Re/"
		self.mainWindow.denseReconstruction.config = "--min-resolution 320 --resolution-level " + str(self.mainWindow.denseReconstruction.res_level) + " -w " + self.mainWindow.denseReconstruction.basepath + "workPath/"
		self.mainWindow.denseReconstruction.scenepath = self.mainWindow.denseReconstruction.input_path + "/"
		self.mainWindow.denseReconstruction.imgpath = self.mainWindow.denseReconstruction.input_path + "/undistorted_images/"

		#self.mainWindow.denseReconstruction.quality = self.quality_input.currentText()
		if self.quality_input.currentText() == "low" :
			self.mainWindow.denseReconstruction.quality = "Low"
		elif self.quality_input.currentText() == "Medium" :
			self.mainWindow.denseReconstruction.quality = "Medium"
		elif self.quality_input.currentText() == "High" :
			self.mainWindow.denseReconstruction.quality = "High"

		self.mainWindow.denseReconstruction.window_radius = 4
		self.mainWindow.denseReconstruction.window_step = 2
		self.mainWindow.denseReconstruction.num_samples = 7
		self.mainWindow.denseReconstruction.num_iterations = 3
		self.mainWindow.denseReconstruction.geom_consistency = "false"
		
		self.mainWindow.denseReconstruction.check_num_images = 25
		self.mainWindow.denseReconstruction.max_reproj_error = 2
		self.mainWindow.denseReconstruction.max_depth_error = 0.01
		self.mainWindow.denseReconstruction.max_normal_error = 10

		self.mainWindow.denseReconstruction.merge_archive_type = 1

		slave_id = 0		

		for i in range(0, int(self.mainWindow.denseReconstruction.execNum)):
			exe_num_each_nodes = self.mainWindow.denseReconstruction.task_num_list[i]
			for j in range(0, int(exe_num_each_nodes)):
				self.mainWindow.denseReconstruction.task_exeSlave.append(slave_id)
			slave_id = slave_id + 1
	

		for i in range(0, int(self.mainWindow.denseReconstruction.nParts)):
			self.mainWindow.denseReconstruction.inputpaths.append(self.mainWindow.denseReconstruction.basepath + "/Densify_temp_" + str(i)+ "/")
			self.mainWindow.denseReconstruction.colmap_data_paths.append(self.mainWindow.denseReconstruction.basepath + "/Colmap_In_" + str(i) + "/")
			self.mainWindow.denseReconstruction.workpaths.append(self.mainWindow.denseReconstruction.basepath + "/workPath_" + str(i) + "/")
			self.mainWindow.denseReconstruction.outputpaths.append(self.mainWindow.denseReconstruction.outputdir + "/Re_"+str(i)+"/")
			self.mainWindow.denseReconstruction.configs.append("--min-resolution 320 --resolution-level " + str(self.mainWindow.denseReconstruction.res_level) + " -w " + self.mainWindow.denseReconstruction.workpaths[i])
		self.mainWindow.denseReconstruction.all_process = True
		#######################################################SCX###################################################


		#######################################################ZZY###################################################
		self.mainWindow.statusbar.showMessage("开始自动网格重建")
		self.mainWindow.meshReconstruction.nParts = int(self.nparts_input.text())
		self.mainWindow.meshReconstruction.execNum = self.mainWindow.superParaSetting.machine_num

		#if self.autoTask.isChecked():
			#self.mainWindow.denseReconstruction.autoGenerateTask()
		#else:
		raw_task_str = "1,1,1,1,1,1,1,1,1"
		self.mainWindow.meshReconstruction.task_num_list = raw_task_str.split(',')

		self.mainWindow.meshReconstruction.input_path = self.mainWindow.denseReconstruction.basepath
		self.mainWindow.meshReconstruction.output_path = self.mainWindow.denseReconstruction.basepath + "/Mesh/"
		self.mainWindow.meshReconstruction.scenestructpath = self.mainWindow.denseReconstruction.basepath
		self.mainWindow.meshReconstruction.logdirpath = self.mainWindow.meshReconstruction.output_path + "/zzy_log/"
		self.mainWindow.meshReconstruction.quality = self.quality_input.currentText()

		self.close()
		slave_id = 0		

		for i in range(0, int(self.mainWindow.meshReconstruction.execNum)):
			exe_num_each_nodes = self.mainWindow.meshReconstruction.task_num_list[i]
			for j in range(0, int(exe_num_each_nodes)):
				self.mainWindow.meshReconstruction.task_exeSlave.append(slave_id)
			slave_id = slave_id + 1
	

		for i in range(0, int(self.mainWindow.meshReconstruction.nParts)):
			self.mainWindow.meshReconstruction.inputpaths.append(self.mainWindow.meshReconstruction.input_path + "/Colmap_In_" + str(i)+ "/dense")
			self.mainWindow.meshReconstruction.outputpaths.append(self.mainWindow.meshReconstruction.output_path + "/scene_mesh_"+str(i))


		self.close()
		# slave_id = 0		

		# for i in range(0, int(self.mainWindow.denseReconstruction.execNum)):
		# 	exe_num_each_nodes = self.mainWindow.denseReconstruction.task_num_list[i]
		# 	for j in range(0, int(exe_num_each_nodes)):
		# 		self.mainWindow.denseReconstruction.task_exeSlave.append(slave_id)
		# 	slave_id = slave_id + 1
	

		# for i in range(0, int(self.mainWindow.denseReconstruction.nParts)):
		# 	self.mainWindow.denseReconstruction.inputpaths.append(self.mainWindow.denseReconstruction.basepath + "/Densify_temp_" + str(i)+ "/")
		# 	self.mainWindow.denseReconstruction.colmap_data_paths.append(self.mainWindow.denseReconstruction.basepath + "/Colmap_In_" + str(i) + "/")
		# 	self.mainWindow.denseReconstruction.workpaths.append(self.mainWindow.denseReconstruction.basepath + "/workPath_" + str(i) + "/")
		# 	self.mainWindow.denseReconstruction.outputpaths.append(self.mainWindow.denseReconstruction.outputdir + "/Re_"+str(i)+"/")
		# 	self.mainWindow.denseReconstruction.configs.append("--min-resolution 320 --resolution-level " + str(self.mainWindow.denseReconstruction.res_level) + " -w " + self.mainWindow.denseReconstruction.workpaths[i])
		self.mainWindow.label_2.setText("Image List(" + str(image_num) + ")")
		image_list = os.popen("ls " + self.mainWindow.sparseReconstruction.input_path)
		image_list_str = image_list.read()
		self.mainWindow.textBrowser.clear()
		self.mainWindow.textBrowser.append(image_list_str)
		self.mainWindow.timer.start(100, self.mainWindow)
		self.mainWindow.log_timer.start(500)
		self.mainWindow.sparseReconstruction.autoSparsify(1)

		#######################################################ZZY###################################################
	# def checkboxHandle(self):	
	# 	if self.autoTask.isChecked():
	# 		self.task_input.setReadOnly(True)
	# 	else:
	# 		self.task_input.setReadOnly(False)


	def setInputpath(self):
		self.mainWindow.sparseReconstruction.input_path = QFileDialog.getExistingDirectory(self, "选择输入文件夹", "/")
		self.input_path_label.setText(self.mainWindow.sparseReconstruction.input_path)
	def setOutputpath(self):
		self.mainWindow.sparseReconstruction.output_path = QFileDialog.getExistingDirectory(self, "选择输出文件夹", "/")
		self.ouput_path_label.setText(self.mainWindow.sparseReconstruction.output_path)
#	def setBasepath(self):
#		self.mainWindow.sparseReconstruction.basepath = QFileDialog.getExistingDirectory(self, "选择工作文件夹", "/")
#		self.base_path_label.setText(self.mainWindow.sparseReconstruction.basepath)
				
class AutoSparseDialog(QDialog, Ui_AutoSparseDialog):
	def __init__(self, mainWindow):
		super(AutoSparseDialog, self).__init__()
		self.setupUi(self)
		self.mainWindow = mainWindow
		self.autoDenseStartBtn.clicked.connect(self.startSparseReconstruction)
		self.input_path_btn.clicked.connect(self.setInputpath)
		self.output_path_btn.clicked.connect(self.setOutputpath)
		self.base_path_btn.clicked.connect(self.setBasepath)
		#self.autoTask.stateChanged.connect(self.checkboxHandle)
	def startSparseReconstruction(self):
		self.mainWindow.statusbar.showMessage("开始自动sparse重建")
		#self.mainWindow.denseReconstruction.nParts = int(self.nparts_input.text())
		self.mainWindow.sparseReconstruction.execNum = self.mainWindow.superParaSetting.machine_num

		# if self.autoTask.isChecked():
		# 	self.mainWindow.denseReconstruction.autoGenerateTask()
		# else:
		# 	raw_task_str = self.task_input.text()
		# 	self.mainWindow.denseReconstruction.task_num_list = raw_task_str.split(',')
		# self.mainWindow.sparseReconstruction.
		
		# self.max_image_size = 2000
		# self.max_num_neighbors = 50
		# self.max_distance = 100
		# self.final_ba = 0
		# self.completeness_ratio = 0.5
		# self.max_local_ba_iterations = 6
		# self.max_global_ba_iterations = 2
		# self.ba_global_images_ratio = 1.3200000000000001
		# self.ba_global_points_ratio = 1.3200000000000001
		# self.ba_global_max_refinements = 2
		# self.num_workers = 8
		# self.num_images_ub = 100

		self.mainWindow.sparseReconstruction.quality = self.quality_input.currentText()
		print(self.quality_input.currentText())
		if self.quality_input.currentText() == "Lowest" :
			self.mainWindow.sparseReconstruction.max_image_size = 2000
			self.mainWindow.sparseReconstruction.max_num_neighbors =50
			self.mainWindow.sparseReconstruction.max_distance = 100
			self.mainWindow.sparseReconstruction.final_ba =0
			self.mainWindow.sparseReconstruction.completeness_ratio = 0.5
			self.mainWindow.sparseReconstruction.max_local_ba_iterations = 6
			self.mainWindow.sparseReconstruction.max_global_ba_iterations = 2
			self.mainWindow.sparseReconstruction.ba_global_images_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_points_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_max_refinements =2
			self.mainWindow.sparseReconstruction.num_workers =8
			self.mainWindow.sparseReconstruction.num_images_ub = int(self.nparts_input.text())
		elif self.quality_input.currentText() == "low" :
			self.mainWindow.sparseReconstruction.max_image_size = 2000
			self.mainWindow.sparseReconstruction.max_num_neighbors =50
			self.mainWindow.sparseReconstruction.max_distance = 100
			self.mainWindow.sparseReconstruction.final_ba =0
			self.mainWindow.sparseReconstruction.completeness_ratio = 0.5
			self.mainWindow.sparseReconstruction.max_local_ba_iterations = 12
			self.mainWindow.sparseReconstruction.max_global_ba_iterations = 4
			self.mainWindow.sparseReconstructyqion.ba_global_images_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_points_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_max_refinements =2
			self.mainWindow.sparseReconstruction.num_workers =8
			self.mainWindow.sparseReconstruction.num_images_ub =int(self.nparts_input.text())
		elif self.quality_input.currentText() == "Medium" :
			self.mainWindow.sparseReconstruction.max_image_size = 3200
			self.mainWindow.sparseReconstruction.max_num_neighbors =100
			self.mainWindow.sparseReconstruction.max_distance = 100
			self.mainWindow.sparseReconstruction.final_ba =1
			self.mainWindow.sparseReconstruction.completeness_ratio = 0.6
			self.mainWindow.sparseReconstruction.max_local_ba_iterations = 15
			self.mainWindow.sparseReconstruction.max_global_ba_iterations = 30
			self.mainWindow.sparseReconstruction.ba_global_images_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_points_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_max_refinements =3
			self.mainWindow.sparseReconstruction.num_workers =8
			self.mainWindow.sparseReconstruction.num_images_ub =int(self.nparts_input.text())
		elif self.quality_input.currentText() == "High" :
			self.mainWindow.sparseReconstruction.max_image_size = 3200
			self.mainWindow.sparseReconstruction.max_num_neighbors =200
			self.mainWindow.sparseReconstruction.max_distance = 100
			self.mainWindow.sparseReconstruction.final_ba =1
			self.mainWindow.sparseReconstruction.completeness_ratio = 0.7
			self.mainWindow.sparseReconstruction.max_local_ba_iterations = 30
			self.mainWindow.sparseReconstruction.max_global_ba_iterations = 75
			self.mainWindow.sparseReconstruction.ba_global_images_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_points_ratio = 1.3200000000000001
			self.mainWindow.sparseReconstruction.ba_global_max_refinements =3
			self.mainWindow.sparseReconstruction.num_workers =8
			self.mainWindow.sparseReconstruction.num_images_ub =int(self.nparts_input.text())
		else :
			print("yq else")
		# self.mainWindow.denseReconstruction.window_radius = 4
		# self.mainWindow.denseReconstruction.window_step = 2
		# self.mainWindow.denseReconstruction.num_samples = 7
		# self.mainWindow.denseReconstruction.num_iterations = 3
		# self.mainWindow.denseReconstruction.geom_consistency = "false"
		
		# self.mainWindow.denseReconstruction.check_num_images = 25
		# self.mainWindow.denseReconstruction.max_reproj_error = 2
		# self.mainWindow.denseReconstruction.max_depth_error = 0.01
		# self.mainWindow.denseReconstruction.max_normal_error = 10

		# self.mainWindow.denseReconstruction.merge_archive_type = 1

		self.close()
		# slave_id = 0		

		# for i in range(0, int(self.mainWindow.denseReconstruction.execNum)):
		# 	exe_num_each_nodes = self.mainWindow.denseReconstruction.task_num_list[i]
		# 	for j in range(0, int(exe_num_each_nodes)):
		# 		self.mainWindow.denseReconstruction.task_exeSlave.append(slave_id)
		# 	slave_id = slave_id + 1
	

		# for i in range(0, int(self.mainWindow.denseReconstruction.nParts)):
		# 	self.mainWindow.denseReconstruction.inputpaths.append(self.mainWindow.denseReconstruction.basepath + "/Densify_temp_" + str(i)+ "/")
		# 	self.mainWindow.denseReconstruction.colmap_data_paths.append(self.mainWindow.denseReconstruction.basepath + "/Colmap_In_" + str(i) + "/")
		# 	self.mainWindow.denseReconstruction.workpaths.append(self.mainWindow.denseReconstruction.basepath + "/workPath_" + str(i) + "/")
		# 	self.mainWindow.denseReconstruction.outputpaths.append(self.mainWindow.denseReconstruction.outputdir + "/Re_"+str(i)+"/")
		# 	self.mainWindow.denseReconstruction.configs.append("--min-resolution 320 --resolution-level " + str(self.mainWindow.denseReconstruction.res_level) + " -w " + self.mainWindow.denseReconstruction.workpaths[i])

		image_list = os.popen("ls " + self.mainWindow.sparseReconstruction.input_path)
		image_list_str = image_list.read()
		self.mainWindow.timer.start(100, self.mainWindow)
		self.mainWindow.textBrowser.clear()
		self.mainWindow.textBrowser.append(image_list_str)
		self.mainWindow.log_timer.start(500)
		self.mainWindow.sparseReconstruction.autoSparsify(0)

		
	# def checkboxHandle(self):	
	# 	if self.autoTask.isChecked():
	# 		self.task_input.setReadOnly(True)
	# 	else:
	# 		self.task_input.setReadOnly(False)


	def setInputpath(self):
		self.mainWindow.sparseReconstruction.input_path = QFileDialog.getExistingDirectory(self, "选择输入文件夹", "/")
		self.input_path_label.setText(self.mainWindow.sparseReconstruction.input_path)
	def setOutputpath(self):
		self.mainWindow.sparseReconstruction.output_path = QFileDialog.getExistingDirectory(self, "选择输出文件夹", "/")
		self.ouput_path_label.setText(self.mainWindow.sparseReconstruction.output_path)
	def setBasepath(self):
		self.mainWindow.sparseReconstruction.basepath = QFileDialog.getExistingDirectory(self, "选择工作文件夹", "/")
		self.base_path_label.setText(self.mainWindow.sparseReconstruction.basepath)

class AutoDenseDialog(QDialog, Ui_AutoDenseDialog):
	def __init__(self, mainWindow):
		super(AutoDenseDialog, self).__init__()
		self.setupUi(self)
		self.mainWindow = mainWindow
		self.autoDenseStartBtn.clicked.connect(self.startDenseReconstruction)
		self.input_path_btn.clicked.connect(self.setInputpath)
		self.img_path_btn.clicked.connect(self.setImgpath)
		self.output_path_btn.clicked.connect(self.setOutputpath)
		self.base_path_btn.clicked.connect(self.setBasepath)
		self.autoTask.stateChanged.connect(self.checkboxHandle)

	def startDenseReconstruction(self):
		self.mainWindow.statusbar.showMessage("开始自动稠密重建")
		self.mainWindow.denseReconstruction.nParts = int(self.nparts_input.text())
		self.mainWindow.denseReconstruction.execNum = self.mainWindow.superParaSetting.machine_num

		if self.autoTask.isChecked():
			self.mainWindow.denseReconstruction.autoGenerateTask()
		else:
			raw_task_str = self.task_input.text()
			self.mainWindow.denseReconstruction.task_num_list = raw_task_str.split(',')

		self.mainWindow.denseReconstruction.resolution = self.resolution_input.text()
		self.mainWindow.denseReconstruction.min_resolution = 320
		self.mainWindow.denseReconstruction.res_level = 4
		self.mainWindow.denseReconstruction.part_archive_type = 1

		self.mainWindow.denseReconstruction.quality = self.quality_input.currentText()
		self.mainWindow.denseReconstruction.window_radius = 4
		self.mainWindow.denseReconstruction.window_step = 2
		self.mainWindow.denseReconstruction.num_samples = 7
		self.mainWindow.denseReconstruction.num_iterations = 3
		self.mainWindow.denseReconstruction.geom_consistency = "false"
		
		self.mainWindow.denseReconstruction.check_num_images = 25
		self.mainWindow.denseReconstruction.max_reproj_error = 2
		self.mainWindow.denseReconstruction.max_depth_error = 0.01
		self.mainWindow.denseReconstruction.max_normal_error = 10

		self.mainWindow.denseReconstruction.merge_archive_type = 1

		self.close()
		slave_id = 0		

		for i in range(0, int(self.mainWindow.denseReconstruction.execNum)):
			exe_num_each_nodes = self.mainWindow.denseReconstruction.task_num_list[i]
			for j in range(0, int(exe_num_each_nodes)):
				self.mainWindow.denseReconstruction.task_exeSlave.append(slave_id)
			slave_id = slave_id + 1
	
		for i in range(0, int(self.mainWindow.denseReconstruction.nParts)):
			self.mainWindow.denseReconstruction.inputpaths.append(self.mainWindow.denseReconstruction.basepath + "/Densify_temp_"+str(i)+"/")
			self.mainWindow.denseReconstruction.colmap_data_paths.append(self.mainWindow.denseReconstruction.basepath + "/Colmap_In_"+str(i)+"/")
			self.mainWindow.denseReconstruction.outputpaths.append(self.mainWindow.denseReconstruction.outputdir + "/Re_"+str(i)+"/")

		self.mainWindow.log_timer.start(500)
		self.mainWindow.denseReconstruction.autoDensify()

	def checkboxHandle(self):	
		if self.autoTask.isChecked():
			self.task_input.setReadOnly(True)
		else:
			self.task_input.setReadOnly(False)

	def setInputpath(self):
		self.mainWindow.denseReconstruction.scenepath = QFileDialog.getOpenFileName(self, "选择scene文件", "/home/hadoop/data/data/0529/", "mvs file (*.mvs)")[0]
		self.input_path_label.setText(self.mainWindow.denseReconstruction.scenepath)
	def setImgpath(self):
		self.mainWindow.denseReconstruction.imgpath = QFileDialog.getExistingDirectory(self, "选择输出文件夹", "/home/hadoop/data/data/TEST/")
		self.img_path_label.setText(self.mainWindow.denseReconstruction.imgpath)
	def setOutputpath(self):
		self.mainWindow.denseReconstruction.outputdir = QFileDialog.getExistingDirectory(self, "选择输出文件夹", "/home/hadoop/data/data/0529/dense_output/")
		self.ouput_path_label.setText(self.mainWindow.denseReconstruction.outputdir)
	def setBasepath(self):
		self.mainWindow.denseReconstruction.basepath = QFileDialog.getExistingDirectory(self, "选择工作文件夹", "/home/hadoop/data/data/0529/")
		self.mainWindow.denseReconstruction.tmppath = self.mainWindow.denseReconstruction.basepath
		self.base_path_label.setText(self.mainWindow.denseReconstruction.basepath)


class AutoMeshDialog(QDialog, Ui_AutoMeshDialog):
	def __init__(self, mainWindow):
		super(AutoMeshDialog, self).__init__()
		self.setupUi(self)
		self.mainWindow = mainWindow
		self.autoDenseStartBtn.clicked.connect(self.startMeshReconstruction)
		self.input_path_btn.clicked.connect(self.setInputpath)
		self.output_path_btn.clicked.connect(self.setOutputpath)
		self.base_path_btn.clicked.connect(self.setBasepath)
		#self.autoTask.stateChanged.connect(self.checkboxHandle)

	def startMeshReconstruction(self):
		self.mainWindow.statusbar.showMessage("开始自动网格重建")
		self.mainWindow.meshReconstruction.nParts = int(self.nparts_input.text())
		self.mainWindow.meshReconstruction.execNum = self.mainWindow.superParaSetting.machine_num

		#if self.autoTask.isChecked():
			#self.mainWindow.denseReconstruction.autoGenerateTask()
		#else:
		raw_task_str = self.task_input.text()
		self.mainWindow.meshReconstruction.task_num_list = raw_task_str.split(',')

		self.mainWindow.meshReconstruction.logdirpath = self.mainWindow.meshReconstruction.output_path + "/zzy_log/"
		self.mainWindow.meshReconstruction.quality = self.quality_input.currentText()

		self.close()
		slave_id = 0		

		for i in range(0, int(self.mainWindow.meshReconstruction.execNum)):
			exe_num_each_nodes = self.mainWindow.meshReconstruction.task_num_list[i]
			for j in range(0, int(exe_num_each_nodes)):
				self.mainWindow.meshReconstruction.task_exeSlave.append(slave_id)
			slave_id = slave_id + 1
	

		for i in range(0, int(self.mainWindow.meshReconstruction.nParts)):
			self.mainWindow.meshReconstruction.inputpaths.append(self.mainWindow.meshReconstruction.input_path + "/Colmap_In_" + str(i)+ "/dense")
			self.mainWindow.meshReconstruction.outputpaths.append(self.mainWindow.meshReconstruction.output_path + "/scene_mesh_"+str(i))

		#image_list = os.popen("ls " + self.mainWindow.denseReconstruction.imgpath)
		#image_list_str = image_list.read()
		#self.mainWindow.textBrowser.clear()
		#self.mainWindow.textBrowser.append(image_list_str)
		self.mainWindow.log_timer.start(500)
		self.mainWindow.meshReconstruction.autoMeshReconstruct(0)

		
	def checkboxHandle(self):	
		if self.autoTask.isChecked():
			self.task_input.setReadOnly(True)
		else:
			self.task_input.setReadOnly(False)


	def setInputpath(self):
		self.mainWindow.meshReconstruction.input_path = QFileDialog.getExistingDirectory(self, "选择输入文件夹", "/")
		self.input_path_label.setText(self.mainWindow.meshReconstruction.input_path)
	def setOutputpath(self):
		self.mainWindow.meshReconstruction.output_path = QFileDialog.getExistingDirectory(self, "选择输出文件夹", "/")
		self.ouput_path_label.setText(self.mainWindow.meshReconstruction.output_path)
	def setBasepath(self):
		self.mainWindow.meshReconstruction.scenestructpath = QFileDialog.getExistingDirectory(self, "选择scene结构文件夹", "/")
		self.base_path_label.setText(self.mainWindow.meshReconstruction.scenestructpath)


class DensePartitionDialog(QDialog, Ui_PartitionDialog):
	def __init__(self, mainWindow):
		super(DensePartitionDialog, self).__init__()
		self.setupUi(self)
		self.mainWindow = mainWindow
		self.StartBtn.clicked.connect(self.startDensePartition)
		self.input_path_btn.clicked.connect(self.setInputpath)
		self.base_path_btn.clicked.connect(self.setBasepath)
		self.img_path_btn.clicked.connect(self.setImgpath)
		self.output_path_btn.clicked.connect(self.setOutputpath)

	def startDensePartition(self):
		self.mainWindow.statusbar.showMessage("开始清理工作空间并开始分块")
		self.mainWindow.denseReconstruction.nParts = int(self.nParts_input.text())
		self.mainWindow.denseReconstruction.execNum = self.mainWindow.superParaSetting.machine_num
		raw_task_str = self.task_input.text()
		self.mainWindow.denseReconstruction.task_num_list = raw_task_str.split(',')

		self.mainWindow.denseReconstruction.min_resolution = self.resolution_input.text()
		self.mainWindow.denseReconstruction.res_level = self.resolutionlevel_input.text()
		
		astr = self.archive_input.currentText()
		if astr == 'Text':
			self.mainWindow.denseReconstruction.part_archive_type = 0
		elif astr == 'Binary':
			self.mainWindow.denseReconstruction.part_archive_type = 1
		elif astr == 'CompressedBinary':
			self.mainWindow.denseReconstruction.part_archive_type = 2
		else:
			self.mainWindow.denseReconstruction.part_archive_type = 1
		
		slave_id = 0

		for i in range(0, int(self.mainWindow.denseReconstruction.execNum)):
			exe_num_each_nodes = self.mainWindow.denseReconstruction.task_num_list[i]
			for j in range(0, int(exe_num_each_nodes)):
				self.mainWindow.denseReconstruction.task_exeSlave.append(slave_id)
			slave_id = slave_id + 1

		for i in range(0, int(self.mainWindow.denseReconstruction.nParts)):
			self.mainWindow.denseReconstruction.inputpaths.append(self.mainWindow.denseReconstruction.basepath + "/Densify_temp_"+str(i)+"/")
			self.mainWindow.denseReconstruction.colmap_data_paths.append(self.mainWindow.denseReconstruction.basepath + "/Colmap_In_"+str(i)+"/")
			self.mainWindow.denseReconstruction.outputpaths.append(self.mainWindow.denseReconstruction.outputdir + "/Re_"+str(i)+"/")

		self.close()
		self.mainWindow.log_timer.start(500)
		self.mainWindow.denseReconstruction.ClearAndPartition()

	def setInputpath(self):
		self.mainWindow.denseReconstruction.scenepath = QFileDialog.getOpenFileName(self, "选择scene文件", "/home/hadoop/data/data/0529/", "mvs file (*.mvs)")[0]
		self.input_path_label.setText(self.mainWindow.denseReconstruction.scenepath)
	def setImgpath(self):
		self.mainWindow.denseReconstruction.imgpath = QFileDialog.getExistingDirectory(self, "选择输出文件夹", "/home/hadoop/data/data/TEST/")
		self.img_path_label.setText(self.mainWindow.denseReconstruction.imgpath)
	def setBasepath(self):
		self.mainWindow.denseReconstruction.basepath = QFileDialog.getExistingDirectory(self, "选择工作文件夹", "/home/hadoop/data/data/0529/")
		self.mainWindow.denseReconstruction.tmppath = self.mainWindow.denseReconstruction.basepath
		self.base_path_label.setText(self.mainWindow.denseReconstruction.basepath)
	def setOutputpath(self):
		self.mainWindow.denseReconstruction.outputdir = QFileDialog.getExistingDirectory(self, "选择输出文件夹", "/home/hadoop/data/data/0529/dense_output/")
		self.ouput_path_label.setText(self.mainWindow.denseReconstruction.outputdir)

class DensePatchMatchDialog(QDialog, Ui_PatchMatchDialog):
	def __init__(self, mainWindow):
		super(DensePatchMatchDialog, self).__init__()
		self.setupUi(self)
		self.mainWindow = mainWindow
		self.pmStartBtn.clicked.connect(self.startDensePatchMatch)
	
	def startDensePatchMatch(self):
		self.mainWindow.statusbar.showMessage("开始估算深度图")
        
		self.mainWindow.denseReconstruction.window_radius = self.window_radius_input.text()
		self.mainWindow.denseReconstruction.window_step = self.window_step_input.text()
		self.mainWindow.denseReconstruction.num_samples = self.sample_input.text()
		self.mainWindow.denseReconstruction.num_iterations = self.iter_input.text()
		if self.gemo_checkBox.isChecked():
			self.mainWindow.denseReconstruction.geom_consistency = "true"
		else :
			self.mainWindow.denseReconstruction.geom_consistency = "false"
		print(self.mainWindow.denseReconstruction.geom_consistency)
		self.close()
		
		#pm_end_time = datetime.datetime.now()

		#self.mainWindow.denseReconstruction.print_settings()
		self.mainWindow.log_timer.start(500)
		self.mainWindow.denseReconstruction.DensifyReconstruction(2)
		#self.mainWindow.statusbar.showMessage("深度图估算结束, 运行时间：" + str((pm_end_time - pm_start_time).seconds))			
		#self.mainWindow.log_timer.stop()
		#self.mainWindow.print_log()	

class DenseFusedDialog(QDialog, Ui_FusedDialog):
	def __init__(self, mainWindow):
		super(DenseFusedDialog, self).__init__()
		self.setupUi(self)
		self.mainWindow = mainWindow
		self.fuseStartBtn.clicked.connect(self.startFusedPly)
		#self.output_path_btn.clicked.connect(self.setOutputpath)
	def startFusedPly(self):
		self.mainWindow.statusbar.showMessage("开始点云融合")
		#fused_start_time = datetime.datetime.now()

		self.mainWindow.denseReconstruction.check_num_images = self.check_num_input.text()
		self.mainWindow.denseReconstruction.max_reproj_error = self.reproj_error_input.text()
		self.mainWindow.denseReconstruction.max_depth_error = self.depth_error_input.text()
		self.mainWindow.denseReconstruction.max_normal_error = self.normal_error_input.text()

		self.close()

		self.mainWindow.log_timer.start(500)
		self.mainWindow.denseReconstruction.DensifyReconstruction(3)


class DenseMergeDialog(QDialog, Ui_MergeDialog):
	def __init__(self, mainWindow):
		super(DenseMergeDialog, self).__init__()
		self.setupUi(self)
		self.mainWindow = mainWindow
		self.StartBtn.clicked.connect(self.startMerge)

	def startMerge(self):
		self.mainWindow.statusbar.showMessage("开始场景拼接")
		#fused_start_time = datetime.datetime.now()
		astr = self.archive_input.currentText()
		if astr == 'Text':
			self.mainWindow.denseReconstruction.merge_archive_type = 0
		elif astr == 'Binary':
			self.mainWindow.denseReconstruction.merge_archive_type = 1
		elif astr == 'CompressedBinary':
			self.mainWindow.denseReconstruction.merge_archive_type = 2
		else:
			self.mainWindow.denseReconstruction.merge_archive_type = 1
		self.close()
		
		self.mainWindow.log_timer.start(500)
		self.mainWindow.denseReconstruction.SceneMerge()


class DenseCommandInterfaceThread(QThread):
	finished = pyqtSignal(bool)
	def __init__(self, cmdtext, slaveIndex, mainWindow, parent=None):
		super().__init__(parent)
		self.cmdtext = cmdtext	
		self.mainWindow = mainWindow
		self.slaveIndex = slaveIndex

	def run(self):
		p = subprocess.Popen(self.cmdtext, shell= True,stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
		while p.poll() is None:
			line = p.stdout.readline()
			line = line.decode('utf-8')
			print(line)
			self.mainWindow.denseReconstruction.logContents[self.slaveIndex] = self.mainWindow.denseReconstruction.logContents[self.slaveIndex] + line
		self.finished.emit(True)
		

class DenseCommandInterfaceDialog(QDialog, Ui_DenseCmdDialog):
	def __init__(self, mainWindow):
		super(DenseCommandInterfaceDialog, self).__init__()
		self.setupUi(self)
		self.mainWindow = mainWindow
		self.pushButton.clicked.connect(self.exeCmd)
		

	def exeCmd(self):
		cmdtext = self.textEdit.toPlainText()
		self.mainWindow.log_timer.start(500)
		self.thread = DenseCommandInterfaceThread(cmdtext, 0, self.mainWindow)
		self.thread.finished.connect(self.onFinished)
		self.thread.start()

	def onFinished(self, flag):
		if(flag):
			print("finished")
			self.mainWindow.log_timer.stop()
			self.mainWindow.print_log()
			self.close()


#####################################################################################################################

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)

		self.superParaSetting = SuperParaSetting()
		#self.denseReconstruction = DenseReconstruction(self)

		self.SuperParaSettingAction.triggered.connect(self.super_para_setting)
		self.PartAction.triggered.connect(self.DensePartition)
		self.PatchMatchAction.triggered.connect(self.DensePatchMatch)
		self.FusedAction.triggered.connect(self.DenseFusedPly)
		self.MergeAction_2.triggered.connect(self.DenseSceneMerge)
		self.AutoReconstructionAction.triggered.connect(self.auto_All_Reconstruction)
		self.AutoSparseAction.triggered.connect(self.auto_Sparse_Reconstruction)
		self.AutoDenseAction.triggered.connect(self.auto_Dense_Reconstruction)
		self.DenseParaSettingAction.triggered.connect(self.DenseCommandInterface)
		self.ReconstructionAction.triggered.connect(self.auto_Mesh_Reconstruction)
		self.timer = QBasicTimer()
		self.step = 0
		self.small_step = 0
		
		#self.comboBox.currentIndexChanged.connect(self.print_log)
		#self.print_log = True
		self.log_timer = QTimer(self)
		#self.log_timer.start(1000)
		#self.log_timer.timeout.connect(self.print_log)


	def timerEvent(self,event):
		if self.step >= 100:
			self.timer.stop()
			return
		self.small_step = self.small_step + 1
		self.step = self.small_step / 120
		self.pbar.setValue(self.step)

	def super_para_setting(self):
		dialog = SuperParaSettingDialog(self)		
		dialog.show()	
		dialog.exec_()
	
	def DensePartition(self):
		self.denseReconstruction = DenseReconstruction(self)
		for i in range(0, int(self.superParaSetting.machine_num) - 1):
			self.denseReconstruction.logContents.append("")
		dialog = DensePartitionDialog(self)
		dialog.show()	
		dialog.exec_()	

	def DensePatchMatch(self):
		dialog = DensePatchMatchDialog(self)
		dialog.show()	
		dialog.exec_()	
	
	def DenseFusedPly(self):
		dialog = DenseFusedDialog(self)
		dialog.show()	
		dialog.exec_()	

	def DenseSceneMerge(self):
		dialog = DenseMergeDialog(self)
		dialog.show()	
		dialog.exec_()	
	def auto_All_Reconstruction(self):
		#self.allReconstruction = AllReconstruction(self)
		self.sparseReconstruction = SparseReconstruction(self)
		self.denseReconstruction = DenseReconstruction(self)
		self.meshReconstruction = MeshReconstruction(self)
		self.comboBox.currentIndexChanged.connect(self.print_log_sparse)
		self.log_timer.timeout.connect(self.print_log_sparse)
		for i in range(0, int(self.superParaSetting.machine_num) - 1):
			self.sparseReconstruction.logContents.append("")
			self.denseReconstruction.logContents.append("")
			self.meshReconstruction.logContents.append("")
		dialog = AutoAllReDialog(self)
		dialog.show()	
		dialog.exec_()

	def auto_Sparse_Reconstruction(self):
		self.sparseReconstruction = SparseReconstruction(self)
		self.comboBox.currentIndexChanged.connect(self.print_log_sparse)
		self.log_timer.timeout.connect(self.print_log_sparse)
		for i in range(0, int(self.superParaSetting.machine_num) - 1):
			self.sparseReconstruction.logContents.append("")
		dialog = AutoSparseDialog(self)
		dialog.show()	
		dialog.exec_()

	def auto_Dense_Reconstruction(self):
		self.denseReconstruction = DenseReconstruction(self)
		self.comboBox.currentIndexChanged.connect(self.print_log)
		self.log_timer.timeout.connect(self.print_log)
		for i in range(0, int(self.superParaSetting.machine_num) - 1):
			self.denseReconstruction.logContents.append("")
		dialog = AutoDenseDialog(self)
		dialog.show()	
		dialog.exec_()

	def auto_Mesh_Reconstruction(self):
		self.comboBox.currentIndexChanged.connect(self.print_log_mesh)
		self.log_timer.timeout.connect(self.print_log_mesh)
		self.meshReconstruction = MeshReconstruction(self)
		for i in range(0, int(self.superParaSetting.machine_num) - 1):
			self.meshReconstruction.logContents.append("")
		dialog = AutoMeshDialog(self)
		dialog.show()	
		dialog.exec_()

	def DenseCommandInterface(self):
		dialog = DenseCommandInterfaceDialog(self)
		dialog.show()	
		dialog.exec_()
	
	def print_log(self):
		self.logTextBrowser.clear()
		self.logTextBrowser.append(self.denseReconstruction.logContents[self.comboBox.currentIndex()])
		self.logTextBrowser.moveCursor(self.logTextBrowser.textCursor().End)

	def print_log_mesh(self):
		self.logTextBrowser.clear()
		self.logTextBrowser.append(self.meshReconstruction.logContents[self.comboBox.currentIndex()])
		self.logTextBrowser.moveCursor(self.logTextBrowser.textCursor().End)

	def print_log_sparse(self):
		#print(1)
		self.logTextBrowser.clear()
		self.logTextBrowser.append(self.sparseReconstruction.logContents[self.comboBox.currentIndex()])
		self.logTextBrowser.moveCursor(self.logTextBrowser.textCursor().End)
	def logging(self):
		self.logTextBrowser.clear()
		self.logTextBrowser.append(self.denseReconstruction.logContents[self.comboBox.currentIndex()])
		self.logTextBrowser.moveCursor(self.logTextBrowser.textCursor().End)
		#time.sleep(1)

	def closeEvent(self, event):
		self.print_log = False
		event.accept()

########################################Main######################################################
if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWindow = MainWindow()
	mainWindow.show()
	sys.exit(app.exec_())
