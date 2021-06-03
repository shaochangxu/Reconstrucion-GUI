import datetime
import os
import subprocess
import time
import argparse
import signal
from PyQt5.QtCore import *

class DenseRunThread(QThread):
	finished = pyqtSignal(str)
	def __init__(self, slave_cmdtexts, mode, mainWindow, parent=None):
		super().__init__(parent)
		self.slave_cmdtexts = slave_cmdtexts	
		self.mainWindow = mainWindow
		self.mode = mode

	def run(self):
		processlist = []
		densify_end = []
		slave_num = len(self.slave_cmdtexts)
		for slaveIndex in range(0, slave_num):
			node_processlist = []
			for taskIndex in range(0, len(self.slave_cmdtexts[slaveIndex])):
				child = subprocess.Popen(self.slave_cmdtexts[slaveIndex][taskIndex], shell= True,stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
				child.send_signal(signal.SIGTSTP)
				node_processlist.append(child)				
			processlist.append(node_processlist)
			if len(node_processlist) == 0:
				densify_end.append(True)
			else:
				densify_end.append(False)

		#start first task each slave
		running_task = []
		for slaveIndex in range(0, slave_num):
			if(densify_end[slaveIndex] == True):
				running_task.append(-1)
			else:
				processlist[slaveIndex][0].send_signal(signal.SIGCONT)
				running_task.append(0)
		
		#wait all nodes task all done
		Partition_Densify_Flag = False
		while ((not Partition_Densify_Flag)):
			Partition_Densify_Flag = True
			for i in range(0, slave_num):
				if(densify_end[i] == False):
					Partition_Densify_Flag = False
					break
	
			for i in range(0, slave_num):
				#print(running_task)
				if running_task[i] == -1:
					continue;
				p = processlist[i][running_task[i]]
				if p.poll() is None:
					p.stdout.flush()
					line = p.stdout.readline()
					line = line.decode('utf-8')
					print(line)
					self.mainWindow.denseReconstruction.logContents[i] = self.mainWindow.denseReconstruction.logContents[i] + str(line)
					#self.mainWindow.denseReconstruction.logfiles[i].write(str(line))
				else:
					p.stdout.flush()
					line = p.stdout.read()
					line = line.decode('utf-8')
					self.mainWindow.denseReconstruction.logContents[i] = self.mainWindow.denseReconstruction.logContents[i] + str(line)
					if running_task[i] + 1 < len(processlist[i]):
						running_task[i] = running_task[i] + 1
						time.sleep(0.5)
						processlist[i][running_task[i]].send_signal(signal.SIGCONT)
					else:
						densify_end[i] = True
						running_task[i] = -1
	
		if self.mode == 0:		
			self.finished.emit("PartEnd")
		elif self.mode == 1:
			self.finished.emit("AutoEnd")
		elif self.mode == 2:
			self.finished.emit("PatchMatchEnd")
		elif self.mode == 3:
			self.finished.emit("FusedEnd")
		elif self.mode == 4:
			self.finished.emit("MergeEnd")
		else:
			self.finished.emit("All_DenseEnd")

class DenseReconstruction:
	def __init__(self, mainWindow):
		self.mainWindow = mainWindow
	
		self.basepath = ""
		self.nParts = 0
		self.execNum = 0
		self.quality = "Self_Defined"
		self.task_num_list = []
		self.task_exeSlave = []
		self.kernel_path = "/home/hadoop/scx/cmd_version/Kernel/"

		self.begin_time = 0
		self.basepath = ""
		self.scenepath = ""
		self.tmppath = ""
		self.imgpath = ""
		self.outputdir = ""
	
		self.inputpaths = [] # scene.mvs, pair.txt
		self.colmap_data_paths = [] #Colmap output
		self.outputpaths = []# scene.mvs ply
		self.resolution = 1000
	
		self.logContents = []
		self.logContents.append("")
		########################################EXE PATH##########################################
		#partition exe program path
		self.part_exepath = self.kernel_path + "/openMVS_partition_build/bin/DensifyPointCloud"

		# dense estimate exe path
		self.colmap_exepath2 = self.kernel_path + "/gui_colmap_script2.py"
		self.colmap_exepath3 = self.kernel_path + "/gui_colmap_script3.py"

		# merge exe program path
		self.merge_mvs_exepath = self.kernel_path + "/openMVS_merge_build/bin/DensifyPointCloud"
		self.merge_ply_exepath = self.kernel_path + "/merge_ply_files.py"
		
		##################################### Partition Para #####################################
		self.part_archive_type = 1
		self.res_level = 4
		self.min_resolution = 320
		##################################### PatchMatch Para ####################################
		self.window_radius = 4
		self.window_step = 2
		self.num_samples = 7
		self.num_iterations = 3
		self.geom_consistency = "false"
		#####################################   Fused Para #######################################
		self.check_num_images = 25
		self.max_reproj_error = 2
		self.max_depth_error = 0.01
		self.max_normal_error = 10
		##################################### Merge Para #########################################
		self.merge_archive_type = 1
		self.all_process = False

	def resetPara(self):
		self.resolution = 1000
		self.quality = "Self_Defined"
		##################################### Partition Para #####################################
		self.part_archive_type = 1
		self.res_level = 4
		self.min_resolution = 320
		##################################### PatchMatch Para ####################################
		self.window_radius = 4
		self.window_step = 2
		self.num_samples = 7
		self.num_iterations = 3
		self.geom_consistency = False
		#####################################   Fused Para #######################################
		self.check_num_images = 25
		self.max_reproj_error = 2
		self.max_depth_error = 0.01
		self.max_normal_error = 10
		##################################### Merge Para #########################################
		self.merge_archive_type = 1
		self.sleep_time = 0.1
		self.all_process = False

	def autoGenerateTask(self):
		for j in range(0, int(self.execNum)):
			self.task_num_list.append(0)
		num = int(self.nParts)/int(self.execNum)
		res = int(self.nParts)%int(self.execNum)
		for i in range(0, int(self.execNum)):
			self.task_num_list[i] = self.task_num_list[i] + num
			if i < res:
				self.task_num_list[i] = self.task_num_list[i] + 1
		
	def autoDensify(self):
		#print("densify")
		self.total_auto_time =  datetime.datetime.now()
		self.ClearAndPartition(True)
		#print("Auto Densify finished")	

	def ClearAndPartition(self, auto = False):
		self.part_start_time = datetime.datetime.now()
	
		#delete extra outputs
		scripts = []
		for i in range(0, int(self.execNum)):
			scripts.append([])
		
		os.popen("mkdir " + self.tmppath)
		os.popen("mkdir " + self.outputdir)
		os.popen("mkdir " + self.outputdir + "/mvs")
		os.popen("rm " + self.tmppath + "/pair*")
		os.popen("rm " + self.tmppath + "/doupair*")
		
		for i in range(0, self.execNum - 1):
			scripts[i + 1].append("ssh slave" + str(i + 1) + " mkdir -p " + self.basepath)
			scripts[i + 1].append("ssh slave" + str(i + 1) + " rm -r " + self.outputdir)
			scripts[i + 1].append("ssh slave" + str(i + 1) + " mkdir " + self.outputdir)

		for i in range(0, self.nParts):
			slave_index = self.task_exeSlave[i]
			if slave_index == 0:
				scripts[0].append("rm -r " + self.inputpaths[i])
				scripts[0].append("rm -r " + self.outputpaths[i])
				scripts[0].append("rm -r " + self.colmap_data_paths[i])
				scripts[0].append("mkdir " + self.inputpaths[i])
				scripts[0].append("mkdir " + self.outputpaths[i])
				scripts[0].append("mkdir " + self.colmap_data_paths[i])
			else:
				scripts[slave_index].append("ssh slave" + str(slave_index) + " rm -r " + self.inputpaths[i])
				scripts[slave_index].append("ssh slave" + str(slave_index) + " rm -r " + self.outputpaths[i])
				scripts[slave_index].append("ssh slave" + str(slave_index) + " rm -r " + self.colmap_data_paths[i])
				scripts[slave_index].append("ssh slave" + str(slave_index) + " mkdir " + self.inputpaths[i])
				scripts[slave_index].append("ssh slave" + str(slave_index) + " mkdir " + self.outputpaths[i])
				scripts[slave_index].append("ssh slave" + str(slave_index) + " mkdir " + self.colmap_data_paths[i])

		scripts[0].append(self.part_exepath + " -i " + self.scenepath + " -o " + self.outputdir + "/scene_modified.mvs  --archive-type 1 --parts " + str(self.nParts) + " -w " + self.imgpath + " --pairpath " + self.tmppath)
		
		self.thread = DenseRunThread(scripts, 0, self.mainWindow)

		if auto:
			self.thread.finished.connect(self.AutoFinished)
		else:
			self.thread.finished.connect(self.onFinished)
		
		self.thread.start()


	def onFinished(self, flag):
		self.mainWindow.log_timer.stop()
		self.mainWindow.print_log()
		if flag == "PartEnd":
			for i in range(0, self.nParts):
				slave_index = self.task_exeSlave[i]
				if slave_index == 0:
					os.popen("cp -r " + self.scenepath + " " + self.inputpaths[i])
					# os.popen("cp -r " + pairpath + "/pair"+str(i)+".txt " + inputpaths[i])
					os.popen("cp -r " + self.tmppath + "/pairName"+str(i)+".txt " + self.inputpaths[i] + "/pairName.txt")
				else:
					os.popen("scp " + self.scenepath + " hadoop@slave"+str(slave_index)+":"+self.inputpaths[i])
					# os.popen("scp " + pairpath + "/pair"+str(i)+".txt "+" hadoop@slave"+str(slave_index)+":"+inputpaths[i])
					os.popen("scp " + self.tmppath + "/pairName"+str(i)+".txt "+" hadoop@slave"+str(slave_index)+":"+self.inputpaths[i] + "/pairName.txt")

			self.part_end_time = datetime.datetime.now()
			part_time = (self.part_end_time - self.part_start_time).seconds
			self.mainWindow.statusbar.showMessage("稠密分块结束, 运行时间：" + str(part_time))
			self.logContents[0] = self.logContents[0] + "Partition finished, run time is " + str(part_time) + "\n"
			self.logContents[0] = self.logContents[0] + "=====================Partition end====================="
		elif flag == "PatchMatchEnd":
			self.pm_end_time = datetime.datetime.now()
			pm_time = (self.pm_end_time - self.pm_start_time).seconds
			self.mainWindow.statusbar.showMessage("PatchMatch结束, 运行时间：" + str(pm_time))
			for i in range(1, int(self.execNum)):
				self.logContents[i] = self.logContents[i] + "==================finished==============="
			self.logContents[0] = self.logContents[0] + "PatchMatch finished, run time is " + str(pm_time) + "\n"	
			self.logContents[0] = self.logContents[0] + "==============PatchMatch Densify end================="
		elif flag == "FusedEnd":
			self.fused_end_time = datetime.datetime.now()
			fused_time = (self.fused_end_time - self.fused_start_time).seconds
			self.mainWindow.statusbar.showMessage("FusePly结束, 运行时间：" + str(fused_time))
			for i in range(1, int(self.execNum)):
				self.logContents[i] = self.logContents[i] + "==================finished==============="
			self.logContents[0] = self.logContents[0] + "FusePly finished, run time is " + str(fused_time) + "\n"	
			self.logContents[0] = self.logContents[0] + "==============FusePly Densify end================="
		elif flag == "MergeEnd":
			self.merge_end_time = datetime.datetime.now()
			merge_time = (self.merge_end_time - self.merge_start_time).seconds
			self.mainWindow.statusbar.showMessage("Merge结束, 运行时间：" + str(merge_time))
			self.logContents[0] = self.logContents[0] + "Merge finished, run time is " + str(merge_time) + "\n"	
			self.logContents[0] = self.logContents[0] + "==============Merge Densify end================="

	def AutoFinished(self, flag):
		if flag == "PartEnd":
			for i in range(0, self.nParts):
				slave_index = self.task_exeSlave[i]
				if slave_index == 0:
					os.popen("cp -r " + self.scenepath + " " + self.inputpaths[i])
					# os.popen("cp -r " + pairpath + "/pair"+str(i)+".txt " + inputpaths[i])
					os.popen("cp -r " + self.tmppath + "/pairName"+str(i)+".txt " + self.inputpaths[i] + "/pairName.txt")
				else:
					os.popen("scp " + self.scenepath + " hadoop@slave"+str(slave_index)+":"+self.inputpaths[i])
					# os.popen("scp " + pairpath + "/pair"+str(i)+".txt "+" hadoop@slave"+str(slave_index)+":"+inputpaths[i])
					os.popen("scp " + self.tmppath + "/pairName"+str(i)+".txt "+" hadoop@slave"+str(slave_index)+":"+self.inputpaths[i] + "/pairName.txt")

			print("Part finished")
			self.part_end_time = datetime.datetime.now()
			part_time = (self.part_end_time - self.part_start_time).seconds
			self.mainWindow.statusbar.showMessage("稠密分块结束, 运行时间：" + str(part_time) + "s")
			self.logContents[0] = self.logContents[0] + "Partition finished, run time is " + str(part_time) + "\n"
			self.logContents[0] = self.logContents[0] + "=====================Partition end====================="
			self.DensifyReconstruction(2, True)
		elif flag == "PatchMatchEnd":
			print("PatchMatch finished")
			self.pm_end_time = datetime.datetime.now()
			pm_time = (self.pm_end_time - self.pm_start_time).seconds
			self.mainWindow.statusbar.showMessage("PatchMatch结束, 运行时间：" + str(pm_time)+ "s")
			for i in range(1, int(self.execNum)):
				self.logContents[i] = self.logContents[i] + "==================finished==============="
			self.logContents[0] = self.logContents[0] + "PatchMatch finished, run time is " + str(pm_time) + "\n"	
			self.logContents[0] = self.logContents[0] + "==============PatchMatch Densify end================="
			self.DensifyReconstruction(3, True)
		elif flag == "FusedEnd":
			print("Fused finished")
			self.fused_end_time = datetime.datetime.now()
			fused_time = (self.fused_end_time - self.fused_start_time).seconds
			self.mainWindow.statusbar.showMessage("FusePly结束, 运行时间：" + str(fused_time)+ "s")
			for i in range(1, int(self.execNum)):
				self.logContents[i] = self.logContents[i] + "==================finished==============="
			self.logContents[0] = self.logContents[0] + "FusePly finished, run time is " + str(fused_time) + "\n"	
			self.logContents[0] = self.logContents[0] + "==============FusePly Densify end================="
			self.SceneMerge(True)
		elif flag == "MergeEnd":
			self.mainWindow.log_timer.stop()
			self.mainWindow.print_log()
			print("Merge finished")
			self.total_auto_end_time = datetime.datetime.now()
			merge_time = (self.total_auto_end_time - self.total_auto_time).seconds
			self.mainWindow.statusbar.showMessage("总运行时间：" + str(merge_time)+ "s")
			self.logContents[0] = self.logContents[0] + "Merge finished, run time is " + str(merge_time) + "\n"	
			self.logContents[0] = self.logContents[0] + "==============Merge Densify end================="
			if self.all_process == True:
				self.resetPara()
				print("zzy code")
				self.mainWindow.comboBox.currentIndexChanged.connect(self.mainWindow.print_log_mesh)
				self.mainWindow.log_timer.timeout.connect(self.mainWindow.print_log_mesh)
				self.mainWindow.log_timer.start(500)
				self.mainWindow.meshReconstruction.autoMeshReconstruct(1)

	def DensifyReconstruction(self, mode, auto=False):
		#mode[1: full process 2: patch-match and before 3: start from fused
		
		scripts = []
		for i in range(0, int(self.execNum)):
			scripts.append([])

		script = ""
		if mode == 2:
			self.pm_start_time = datetime.datetime.now()
		elif mode == 3:	
			self.fused_start_time = datetime.datetime.now()

		for i in range(0, int(self.nParts)):
			slave_index = self.task_exeSlave[i]
			if mode == 2:
				script = "python " + self.colmap_exepath2 + " --dataset_path " + self.colmap_data_paths[i] + " --scene_path " + self.outputpaths[i] + "/scene_dense_" +str(i)+ ".mvs" + " --pair_file " + self.inputpaths[i] + "/pairName.txt" + " --img_path " + self.imgpath + " --kernel_path " + self.kernel_path + " --resolution " + str(self.resolution) + " --task_id " + str(i) + " --quality " + self.quality + " --pm_window_radius " + str(self.window_radius) + " --pm_window_step " + str(self.window_step) + " --pm_num_samples " + str(self.num_samples) + " --pm_num_iterations " + str(self.num_iterations) + " --pm_geom_consistency " + str(self.geom_consistency) + "\n"
			elif mode == 3:
				script = "python " + self.colmap_exepath3 + " --dataset_path " + self.colmap_data_paths[i] + " --scene_path " + self.outputpaths[i] + "/scene_dense_" +str(i)+ ".mvs" + " --pair_file " + self.inputpaths[i] + "/pairName.txt" + " --img_path " + self.imgpath + " --kernel_path " + self.kernel_path + " --resolution " + str(self.resolution) + " --task_id " + str(i) + " --quality " + self.quality + " --fused_check_num_images " + str(self.check_num_images) + " --fused_max_reproj_error " + str(self.max_reproj_error) + " --fused_max_depth_error " + str(self.max_depth_error) + " --fused_max_normal_error " + str(self.max_normal_error) + "\n"

			if not slave_index == 0:
				script = "ssh slave" + str(slave_index) + " " + script	
			#print(script)
			scripts[slave_index].append(script)

		self.thread = DenseRunThread(scripts, mode, self.mainWindow)
		if auto:
			self.thread.finished.connect(self.AutoFinished)
		else:
			self.thread.finished.connect(self.onFinished)
		self.thread.start()

	def SceneMerge(self,auto=False):
		#Maybe aborted in the final version
		#send results to master
		self.merge_start_time = datetime.datetime.now()
		
		scripts = []
		for i in range(0, int(self.execNum)):
			scripts.append([])
		
		for i in range(0, self.nParts):
			slave_index = self.task_exeSlave[i]
			if slave_index == 0:
				scripts[0].append("cp " + self.outputpaths[i] + "/scene* " + self.outputdir + "/mvs/scene_dense_" + str(i) + ".mvs")
				scripts[0].append("cp " + self.colmap_data_paths[i] + "/dense/fused.ply  " + self.outputdir + "/fused" + str(i) + ".ply")
			else:
				scripts[slave_index].append("scp "+"hadoop@slave"+str(slave_index)+":"+self.outputpaths[i]+"/scene* " + self.outputdir + "/mvs/scene_dense_" + str(i) + ".mvs")
				scripts[slave_index].append("scp "+"hadoop@slave"+str(slave_index)+":"+self.colmap_data_paths[i]+"/dense/fused.ply  " + self.outputdir + "/fused" + str(i) + ".ply")

		scripts[0].append("python " + self.merge_ply_exepath + " --folder_path " + self.outputdir + " --merged_path "+ self.outputdir + "/fused_All.ply ")

		scripts[0].append(self.merge_mvs_exepath + " -i " + self.outputdir + "/mvs " + " -o " + self.outputdir + "/scene_dense_all.mvs " + " --archive-type 1 " + " -w " + self.imgpath)

		self.thread = DenseRunThread(scripts, 4, self.mainWindow)
		if auto:
			self.thread.finished.connect(self.AutoFinished)
		else:
			self.thread.finished.connect(self.onFinished)
		self.thread.start()

	def print_settings(self):
		print("input_path: " + self.scenepath + "\n")
		print("output_path: " + self.outputdir + "\n")
		print("base_path: " + self.basepath + "\n")
		print("parts: " + str(self.nParts) + "\n")
		print("quality: " + self.quality + "\n")
		print(self.task_num_list)
