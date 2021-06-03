import datetime
import os
import subprocess
import time
import argparse
import signal
from PyQt5.QtCore import *

class SparseRunThread(QThread):
	finished = pyqtSignal(str)
	def __init__(self, slave_cmdtexts, mode, mainWindow, parent=None):
		super().__init__(parent)
		self.slave_cmdtexts = slave_cmdtexts	
		self.mainWindow = mainWindow
		self.mode = mode
		#self.slaveIndex = slaveIndex

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
					self.mainWindow.sparseReconstruction.logContents[i] = self.mainWindow.sparseReconstruction.logContents[i] + str(line)
					#self.mainWindow.dseReconstruction.logfiles[i].write(str(line))
				else:
					p.stdout.flush()
					line = p.stdout.read()
					line = line.decode('utf-8')
					self.mainWindow.sparseReconstruction.logContents[i] = self.mainWindow.sparseReconstruction.logContents[i] + str(line)
					if running_task[i] + 1 < len(processlist[i]):
						running_task[i] = running_task[i] + 1
						processlist[i][running_task[i]].send_signal(signal.SIGCONT)
					else:
						densify_end[i] = True
						running_task[i] = -1
		if self.mode == 0:
			self.finished.emit("SfMEnd")
		elif self.mode == 1:
			self.finished.emit("All_SfMEnd")
		

class SparseReconstruction:
	def __init__(self, mainWindow):
		self.mainWindow = mainWindow

		self.input_path = ""
		self.output_path = ""
		self.basepath = ""
		#self.nParts = 0
		self.execNum = 0
		self.quality = "lowest"
		self.task_num_list = []
		

		self.begin_time = 0
		# self.inputpaths = []
		# self.colmap_data_paths = []
		# self.outputpaths = []
		# self.workpaths = []
		# self.outputdir = ""
		# self.algo = "COLMAP"
		# self.configs = []
		# self.logfiles = []
		# self.task_exeSlave = []
		self.logContents = []
		self.logContents.append("")
		#self.pairpath = "/home/hadoop/scx/Distribute/"
		# self.pairpath = ""
		# self.logdirpath = ""
		# self.allmvsrepath = ""
		# self.config = ""
		
		# #adjust path for zzy 
		# self.adjust_path_for_mesh = "../../../../../../../"

		# ##original scene and images path
		# self.scenepath = ""
		# self.imgpath = ""

		########################################EXE PATH#########################################################
		#colmap
		self.COLMAP_EXE_DIR = "/home/hadoop/yq/DAGSfM/build/src/exe/colmap "
		#interface colmap
		self.INTERFACE_EXE_DIR = "/home/hadoop/openMVS/openMVS_dis_build/bin/InterfaceCOLMAP "
		################local sfm worker sfm para####################
		self.max_image_size = 2000
		self.max_num_neighbors = 50
		self.max_distance = 100
		self.final_ba = 0
		self.completeness_ratio = 0.5
		self.max_local_ba_iterations = 6
		self.max_global_ba_iterations = 2
		self.ba_global_images_ratio = 1.3200000000000001
		self.ba_global_points_ratio = 1.3200000000000001
		self.ba_global_max_refinements = 2
		self.num_workers = 8
		self.num_images_ub = 100
		#self.cluster_type = "SPECTRA"
		
		# #spark exe program path
		# self.openMVSexepath = "/home/hadoop/scx/Distribute/openMVS_distribute_build/bin/DensifyPointCloud"
		# self.colmapexepath = "/home/hadoop/scx/colmap_script.py"
		# #self.colmapexepath2 = "/home/hadoop/scx/Kernel/DenseKernel/colmap_script2.py"
		# self.colmapexepath2 = "/home/hadoop/scx/Kernel/DenseKernel/acmm_script2.py"
		# self.colmapexepath3 = "/home/hadoop/scx/Kernel/DenseKernel/colmap_script3.py"
		# self.gipumaexepath = "/home/hadoop/scx/Distribute/gipuma/gipuma"
		# #partition exe program path 
		# self.partexepath = "/home/hadoop/scx/Kernel/DenseKernel/openMVS_partition_build/bin/DensifyPointCloud"
		# #merge exe program path
		# self.mergeexepath = "/home/hadoop/scx/Distribute/openMVS_merge_build/bin/DensifyPointCloud"
		# self.colmapmergeexepath = "/home/hadoop/scx/Distribute/openMVS_merge_colmap_build/bin/DensifyPointCloud"
		# self.colmapmergeplypath = "/home/hadoop/scx/colmap/scripts/python/merge_ply_files.py"
		# self.resolution = 1000
		# ##################################### Partition Para #####################################
		# self.part_archive_type = 1
		# self.res_level = 4
		# self.min_resolution = 320
		# ##################################### PatchMatch Para ####################################
		# self.window_radius = 4
		# self.window_step = 2
		# self.num_samples = 7
		# self.num_iterations = 3
		# self.geom_consistency = "false"
		# #####################################   Fused Para #######################################
		# self.check_num_images = 25
		# self.max_reproj_error = 2
		# self.max_depth_error = 0.01
		# self.max_normal_error = 10
		# ##################################### Merge Para #########################################
		# self.merge_archive_type = 1

	def resetPara(self):
		self.max_image_size = 2000
		self.max_num_neighbors = 50
		self.max_distance = 100
		self.final_ba = 0
		self.completeness_ratio = 0.5
		self.max_local_ba_iterations = 6
		self.max_global_ba_iterations = 2
		self.ba_global_images_ratio = 1.3200000000000001
		self.ba_global_points_ratio = 1.3200000000000001
		self.ba_global_max_refinements = 2
		self.num_workers = 8
		self.num_images_ub = 100
		# self.resolution = 1000
		self.quality = "lowest"
		# ##################################### Partition Para #####################################
		# self.part_archive_type = 1
		# self.res_level = 4
		# self.min_resolution = 320
		# ##################################### PatchMatch Para ####################################
		# self.window_radius = 4
		# self.window_step = 2
		# self.num_samples = 7
		# self.num_iterations = 3
		# self.geom_consistency = False
		# #####################################   Fused Para #######################################
		# self.check_num_images = 25
		# self.max_reproj_error = 2
		# self.max_depth_error = 0.01
		# self.max_normal_error = 10
		# ##################################### Merge Para #########################################
		# self.merge_archive_type = 1

	# def autoGenerateTask(self):
	# 	for j in range(0, int(self.execNum)):
	# 		self.task_num_list.append(0)
	# 	num = int(self.nParts)/int(self.execNum)
	# 	res = int(self.nParts)%int(self.execNum)
	# 	for i in range(0, int(self.execNum)):
	# 		self.task_num_list[i] = self.task_num_list[i] + num
	# 		if i < res:
	# 			self.task_num_list[i] = self.task_num_list[i] + 1
		


	def autoSparsify(self, mode):
		#print("densify")
		self.total_auto_time =  datetime.datetime.now()
		self.distributedSfM(mode)
		#print("Auto Densify finished")	

	def distributedSfM(self,mode):
		scripts = []
		for i in range(0, int(self.execNum)):
			scripts.append([])

		script = ""

		
		# scripts[0].append(self.COLMAP_EXE_DIR + " database_creator " + " --database_path " + self.basepath +"/database.db")
		
		# scripts[0].append(self.COLMAP_EXE_DIR + " feature_extractor " + " --database_path " + self.basepath + "/database.db" +
		# 		" --image_path " + self.input_path +
		# 		" --ImageReader.camera_model PINHOLE " +
		# 		" --SiftExtraction.max_image_size " + str(self.max_image_size))
		# scripts[0].append(self.COLMAP_EXE_DIR + " spatial_matcher " + " --database_path " + self.basepath +"/database.db" +
		# 		" --SpatialMatching.max_num_neighbors " + str(self.max_num_neighbors) + 
		# 		" --SpatialMatching.max_distance " +str(self.max_distance))

		os.popen("cp /home/hadoop/yq/config.txt " + self.output_path)
		config_file_name = self.output_path + "/config.txt"

	# 	for i in range(1, 9):
	# subprocess.Popen("ssh slave" + str(i) + " "  + COLMAP_EXE_DIR + " local_sfm_worker " + " --output_path " + args.output_path +\
	# 	" --Mapper.ba_local_max_num_iterations " + str(max_local_ba_iterations) + \
	# 	" --Mapper.ba_global_max_num_iterations " + str(max_global_ba_iterations) +\
	# 	" --Mapper.ba_local_max_refinements " + str(ba_global_max_refinements), shell= True
	# 	)
	# 	time.sleep(10)
		for i in range(1, int(self.execNum)):
			scripts[i].append("ssh slave" + str(i) + " "  + self.COLMAP_EXE_DIR + " local_sfm_worker " + " --output_path " + self.output_path +\
		" --Mapper.ba_local_max_num_iterations " + str(self.max_local_ba_iterations) + \
		" --Mapper.ba_global_max_num_iterations " + str(self.max_global_ba_iterations) +\
		" --Mapper.ba_local_max_refinements " + str(self.ba_global_max_refinements))

		#scripts[0].append("python /home/hadoop/yq/sleep.py")

		distributedSfM_scripts = self.COLMAP_EXE_DIR + " distributed_mapper " + \
		" --database_path " + self.basepath + "/database.db" +\
		" --image_path " + self.input_path +\
		" --output_path " + self.output_path +\
		" --vocab_tree_path " + self.output_path + \
		" --config_file_name " + config_file_name +\
		" --num_workers " + str(8) +\
		" --distributed " + str(1) +\
		" --num_images " + str(100) +\
		" --assign_cluster_id " + str(1) +\
		" --write_binary " + str(1) +\
		" --retriangulate " + str(0) +\
		" --final_ba " + str(0) + \
		" --select_tracks_for_bundle_adjustment " + str(1) +\
		" --long_track_length_threshold " + str(10) + \
		" --graph_dir " + self.output_path+\
		" --num_images_ub " + str(self.num_images_ub) +\
		" --completeness_ratio " + str(self.completeness_ratio) +\
		" --relax_ratio " + str(1.3) +\
		" --cluster_type " + "SPECTRA"
		
		print(distributedSfM_scripts)
		#temp = 1/0
		##################
		scripts[0].append(distributedSfM_scripts)

		zero_dir = self.output_path + "/0/"
		ply_name = zero_dir + "all.ply"
		scene_mvs_name = zero_dir + "scene.mvs"
		sparse_dir = self.output_path + "/0/sparse/"

		scripts[0].append("mkdir " + sparse_dir)
		ply_scripts = self.COLMAP_EXE_DIR + " model_converter " + " --input_path " + zero_dir + " --output_path " + ply_name + " --output_type " + "PLY"
		scripts[0].append(ply_scripts)
		
		txt_scripts = self.COLMAP_EXE_DIR + " model_converter " + " --input_path " + zero_dir + " --output_path " + sparse_dir + " --output_type " + "TXT"
		scripts[0].append(txt_scripts)
		#os.popen(COLMAP_EXE_DIR + " model_converter " + " --input_path " + zero_dir + " --output_path " + sparse_dir + " --output_type " + "TXT")
		mvs_scripts = self.INTERFACE_EXE_DIR + " -i " + zero_dir + " -o " + scene_mvs_name + " --image-folder " + self.input_path
		scripts[0].append(mvs_scripts)
		#########################################
		#os.popen(INTERFACE_EXE_DIR + " -i " + zero_dir + " -o " + scene_mvs_name + " --image-folder " + args.image_path)
		# scripts = []
		# for i in range(0, int(self.execNum)):
		# 	scripts.append([])

		self.thread = SparseRunThread(scripts, mode, self.mainWindow)
		# if auto:
		# 	self.thread.finished.connect(self.AutoFinished)
		# else:
		self.thread.finished.connect(self.onFinished)
		self.thread.start()
	

	def onFinished(self, flag):
		self.mainWindow.log_timer.stop()
		self.mainWindow.print_log_sparse()
		if flag == "SfMEnd":
			print("SfM finished")
			self.part_end_time = datetime.datetime.now()
			part_time = (self.part_end_time - self.total_auto_time).seconds
			self.mainWindow.statusbar.showMessage("SfM结束, 运行时间：" + str(part_time))
			print("SfM finished, run time is %0.2f s\n"%part_time)
			print("=====================SfM end=====================")		
			self.logContents[0] = self.logContents[0] + "SfM finished, run time is " + str(part_time) + "\n"
			self.logContents[0] = self.logContents[0] + "=====================SfM end====================="
		elif flag == "All_SfMEnd":
			print("SfM finished")
			self.part_end_time = datetime.datetime.now()
			part_time = (self.part_end_time - self.total_auto_time).seconds
			self.mainWindow.statusbar.showMessage("SfM结束, 运行时间：" + str(part_time))
			print("SfM finished, run time is %0.2f s\n"%part_time)
			print("=====================SfM end=====================")		
			self.logContents[0] = self.logContents[0] + "SfM finished, run time is " + str(part_time) + "\n"
			self.logContents[0] = self.logContents[0] + "=====================SfM end====================="
			print("scx code")
			self.mainWindow.comboBox.currentIndexChanged.connect(self.mainWindow.print_log)
			self.mainWindow.log_timer.timeout.connect(self.mainWindow.print_log)
			self.mainWindow.log_timer.start(500)
			self.mainWindow.denseReconstruction.autoDensify()
		
			


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
			if self.algo == 'COLMAP':
				if mode == 2:
					script = "python " + self.colmapexepath2 + " --dataset_path " + self.colmap_data_paths[i] + " --pair_file " + self.inputpaths[i] + "/pairName.txt" + " --mvs_img_prefix " + self.scenepath + " --adjust_path_for_mesh " + self.adjust_path_for_mesh + " --resolution " + str(self.resolution) + " --task_id " + str(i) + " --quality " + self.quality + " --pm_window_radius " + str(self.window_radius) + " --pm_window_step " + str(self.window_step) + " --pm_num_samples " + str(self.num_samples) + " --pm_num_iterations " + str(self.num_iterations) + " --pm_geom_consistency " + str(self.geom_consistency) + "\n"
					#print(script)
				elif mode == 3:
					script = "python " + self.colmapexepath3 + " --dataset_path " + self.colmap_data_paths[i] + " --pair_file " + self.inputpaths[i] + "/pairName.txt" + " --mvs_img_prefix " + self.scenepath + " --adjust_path_for_mesh " + self.adjust_path_for_mesh + " --resolution " + str(self.resolution) + " --task_id " + str(i) + " --quality " + self.quality + " --fused_check_num_images " + str(self.check_num_images) + " --fused_max_reproj_error " + str(self.max_reproj_error) + " --fused_max_depth_error " + str(self.max_depth_error) + " --fused_max_normal_error " + str(self.max_normal_error) + " --scene_path " + self.outputpaths[i] + "/scene_dense_"+ str(i) +".mvs" + "\n"
				else:
					script = ""
			elif self.algo == 'openMVS':
				script = ""
			elif self.algo == 'gipuma':
				script = ""

			if not slave_index == 0:
				script = "ssh slave" + str(slave_index) + " " + script	
			print(script)
			scripts[slave_index].append(script)

		self.thread = DenseRunThread(scripts, mode, self.mainWindow)
		if auto:
			self.thread.finished.connect(self.AutoFinished)
		else:
			self.thread.finished.connect(self.onFinished)
		self.thread.start()

		
	
