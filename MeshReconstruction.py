import datetime
import os
import subprocess
import time
import argparse
import signal
from PyQt5.QtCore import *

class MeshRunThread(QThread):
	finished = pyqtSignal(str)
	def __init__(self, slave_cmdtexts, mode, mainWindow, parent=None):
		super().__init__(parent)
		self.slave_cmdtexts = slave_cmdtexts	
		self.mainWindow = mainWindow
		self.mode = mode
		#self.mode = 0
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
					self.mainWindow.meshReconstruction.logContents[i] = self.mainWindow.meshReconstruction.logContents[i] + str(line)
					self.mainWindow.meshReconstruction.logfiles[i].write(str(line))
				else:
					p.stdout.flush()
					line = p.stdout.read()
					line = line.decode('utf-8')
					self.mainWindow.meshReconstruction.logContents[i] = self.mainWindow.meshReconstruction.logContents[i] + str(line)
					if running_task[i] + 1 < len(processlist[i]):
						running_task[i] = running_task[i] + 1
						processlist[i][running_task[i]].send_signal(signal.SIGCONT)
					else:
						densify_end[i] = True
						running_task[i] = -1
		if self.mode == 0:		
			self.finished.emit("MeshEnd")
		elif self.mode ==1:
			self.finished.emit("All_MeshEnd")

class MeshReconstruction:
	def __init__(self, mainWindow):
##################################zzy		
		self.mainWindow = mainWindow

		self.input_path = ""
		self.output_path = ""
		self.scenestructpath = ""
		self.nParts = 0
		self.execNum = 0
		self.quality = "Self_Defined"
		self.task_num_list = []
		

		self.begin_time = 0
		self.inputpaths = []
		self.outputpaths = []
		self.logfiles = []
		self.task_exeSlave = []
		self.logContents = []
		self.logContents.append("")
		#self.pairpath = "/home/hadoop/scx/Distribute/"
		self.logdirpath = ""
		self.colmapexepath="/home/hadoop/zzy/colmap/build/src/exe/colmap delaunay_mesher "
		self.col2mvsexepath="/home/hadoop/zzy/openMVS_col2mvs/openMVS_build/bin/ReconstructMesh"
		self.mvsmergeexepath="/home/hadoop/zzy/openMVS_merge/openMVS_build/bin/ReconstructMesh"



	def autoGenerateTask(self):
		for j in range(0, int(self.execNum)):
			self.task_num_list.append(0)
		num = int(self.nParts)/int(self.execNum)
		res = int(self.nParts)%int(self.execNum)
		for i in range(0, int(self.execNum)):
			self.task_num_list[i] = self.task_num_list[i] + num
			if i < res:
				self.task_num_list[i] = self.task_num_list[i] + 1
		


	def autoMeshReconstruct(self,mode):
		self.total_auto_time =  datetime.datetime.now()
		self.MeshReconstruct(True)		
	def MeshReconstruct(self,mode,auto=False):
		self.resmesh_start_time=datetime.datetime.now()
		scripts=[]
		for i in range(0,int(self.execNum)):
			scripts.append([])
		if not self.output_path == "":
			#scripts[0].append("rm -r "+self.output_path)
			scripts[0].append("mkdir "+self.output_path)
			scripts[0].append("cp " + self.input_path + "/0/scene_modified.mvs " + self.scenestructpath)
		if mode==1:
			os.system("mkdir " + self.output_path)
		os.system("rm -r  " + self.logdirpath)
		os.system("mkdir " + self.logdirpath)

		#each log for one nodes
		for i in range(0, int(self.execNum)):
			self.logfiles.append(open(self.logdirpath + "slave" + str(i) + ".log", "w"))
		for i in range(0, int(self.execNum) - 1):
			if not self.output_path == "" :
				os.system("ssh slave" + str(i + 1) + " rm -r " + self.output_path)
				scripts[i+1].append("ssh slave" + str(i + 1) + " mkdir " + self.output_path)
				scripts[i+1].append("scp " + self.input_path + "/0/scene_modified.mvs " + "hadoop@slave" + str(i+1) + ":" + self.scenestructpath)
		for i in range(0, int(self.nParts)):
			slave_index = self.task_exeSlave[i]
			if slave_index == 0:
				scripts[slave_index].append(self.colmapexepath+"--input_path "+self.inputpaths[i]+" --output_path "+self.outputpaths[i]+".ply")
				scripts[slave_index].append(self.col2mvsexepath +  " " + self.scenestructpath + "/scene_modified.mvs " + self.outputpaths[i])
			else:
				scripts[slave_index].append("ssh slave" + str(slave_index) + " " + self.colmapexepath+"--input_path "+self.inputpaths[i]+" --output_path "+self.outputpaths[i]+".ply")
				scripts[slave_index].append("ssh slave" + str(slave_index) + " " + self.col2mvsexepath +  " " + self.scenestructpath + "/scene_modified.mvs " + self.outputpaths[i])
		for i in range(0, int(self.execNum) - 1):
			scripts[i+1].append("scp hadoop@slave" + str(i+1) + ":" + self.output_path + "/scene_mesh* " + self.output_path)
		self.thread = MeshRunThread(scripts, mode, self.mainWindow)
		self.thread.finished.connect(self.onFinished)
		self.thread.start()




	def onFinished(self, flag):
		self.mainWindow.log_timer.stop()
		self.mainWindow.print_log()
		for i in range(0, int(self.execNum)):
			self.logfiles[i].close()
		

	def AutoFinished(self, flag):
		if flag == "PartEnd":
			print("Part finished")
			self.part_end_time = datetime.datetime.now()
			part_time = (self.part_end_time - self.part_start_time).seconds
			self.mainWindow.statusbar.showMessage("稠密分块结束, 运行时间：" + str(part_time) + "s")
			print("Partition finished, run time is %0.2f s\n"%part_time)
			print("=====================Partition end=====================")
			self.logfiles[0].write("Partition finished, run time is %0.2f s\n"%part_time)
			self.logfiles[0].write("=====================Partition end=====================")		
			self.logContents[0] = self.logContents[0] + "Partition finished, run time is " + str(part_time) + "\n"
			self.logContents[0] = self.logContents[0] + "=====================Partition end====================="
			self.DensifyReconstruction(2, True)
		elif flag == "PatchMatchEnd":
			print("PatchMatch finished")
			self.pm_end_time = datetime.datetime.now()
			pm_time = (self.pm_end_time - self.pm_start_time).seconds
			self.mainWindow.statusbar.showMessage("PatchMatch结束, 运行时间：" + str(pm_time)+ "s")
			for i in range(1, int(self.execNum)):
				self.logfiles[i].write("==================finished===============")
				self.logContents[i] = self.logContents[i] + "==================finished==============="
			self.logfiles[0].write("PatchMatch finished, run time is %0.2f s\n"%pm_time)
			self.logfiles[0].write("=====================PatchMatch Densify end=====================")
			self.logContents[0] = self.logContents[0] + "PatchMatch finished, run time is " + str(pm_time) + "\n"	
			self.logContents[0] = self.logContents[0] + "==============PatchMatch Densify end================="
			print("=====================PatchMatch Densify end=====================")
			self.DensifyReconstruction(3, True)
		elif flag == "FusedEnd":
			print("Fused finished")
			self.fused_end_time = datetime.datetime.now()
			fused_time = (self.fused_end_time - self.fused_start_time).seconds
			self.mainWindow.statusbar.showMessage("FusePly结束, 运行时间：" + str(fused_time)+ "s")
			for i in range(1, int(self.execNum)):
				self.logfiles[i].write("==================finished===============")
				self.logContents[i] = self.logContents[i] + "==================finished==============="
			self.logfiles[0].write("FusePly finished, run time is %0.2f s\n"%fused_time)
			self.logfiles[0].write("=====================FusePly Densify end=====================")
			self.logContents[0] = self.logContents[0] + "FusePly finished, run time is " + str(fused_time) + "\n"	
			self.logContents[0] = self.logContents[0] + "==============FusePly Densify end================="
			print("=====================FusePly Densify end=====================")
			self.SceneMerge(True)
		elif flag == "MergeEnd":
			self.mainWindow.log_timer.stop()
			self.mainWindow.print_log()
			print("Merge finished")
			self.total_auto_end_time = datetime.datetime.now()
			merge_time = (self.total_auto_end_time - self.total_auto_time).seconds
			self.mainWindow.statusbar.showMessage("总运行时间：" + str(merge_time)+ "s")
			self.logfiles[0].write("Merge finished, run time is %0.2f s\n"%merge_time)
			self.logfiles[0].write("=====================Merge Densify end=====================")
			self.logContents[0] = self.logContents[0] + "Merge finished, run time is " + str(merge_time) + "\n"	
			self.logContents[0] = self.logContents[0] + "==============Merge Densify end================="
			print("=====================Merge Densify end=====================")
			for i in range(0, int(self.execNum)):
				self.logfiles[i].close()
			


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

		self.thread = MeshRunThread(scripts, mode, self.mainWindow)
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
		

		for i in range(0, int(self.nParts)):
			slave_index = self.task_exeSlave[i]
			if slave_index == 0:
				if self.algo == 'gipuma':
					scripts[slave_index].append("cp " + self.inputpaths[i] + "/scene.mvs " + self.outputpaths[i] + "/scene_dense_" + str(i) + ".mvs")
					scripts[slave_index].append("cp " + self.outputpaths[i] + "/dense_points.txt " + self.outputpaths[i] + "/dense_points_"+str(i) + ".txt")
				else:
					scripts[slave_index].append("cp " + self.outputpaths[i] + "/scene* " + self.allmvsrepath + "/scene_dense_" + str(i) + ".mvs")
					scripts[slave_index].append("cp " + self.colmap_data_paths[i] + "/dense/fused.ply " + self.allmvsrepath + "/fused" + str(i) + ".ply")
			else:
				if self.algo == 'gipuma':
					scripts[slave_index].append("scp "+"hadoop@slave"+str(slave_index)+":"+self.outputpaths[i]+"/dense* "+ "/dense_points_"+str(i) + ".txt")
				else:
					scripts[slave_index].append("scp "+"hadoop@slave"+str(slave_index)+":"+self.outputpaths[i]+"/scene* " + self.allmvsrepath + "/scene_dense_" + str(i) + ".mvs")
					scripts[slave_index].append("scp "+"hadoop@slave"+str(slave_index)+":"+self.colmap_data_paths[i]+"/dense/fused.ply  " + self.allmvsrepath + "/fused" + str(i) + ".ply")
					#scripts[slave_index].append("scp "+"hadoop@slave"+str(slave_index)+":"+self.outputpaths[i]+"/dense* " + self.allmvsrepath + "/dense_points_" + str(i) + ".mvs")

		#Merge results into one
		if self.algo == 'COLMAP':
			scripts[0].append("python " + self.colmapmergeplypath+" --folder_path " + self.allmvsrepath + " --merged_path "+self.allmvsrepath + "/fused_All.ply ")
			scripts[0].append(self.colmapmergeexepath+" -i " + self.allmvsrepath + "/scene_dense_0.mvs"+" -o "+self.allmvsrepath + "/scene_dense.mvs "+self.config + " --archive-type " + str(self.merge_archive_type))
		elif self.algo == 'openMVS':
			scripts[0].append(self.mergeexepath+" -i "+self.allmvsrepath+"/scene_dense_0.mvs"+" -o "+self.allmvsrepath+"/scene_dense.mvs "+self.config + " --archive-type 1")
		elif algo == 'gipuma':
			scripts[0].append(self.mergeexepath+" -i "+self.allmvsrepath+"/scene_dense_0.mvs"+" -o "+self.allmvsrepath+"/scene_dense.mvs "+self.config + " --archive-type 1")

		scripts[0].append("cp "+self.allmvsrepath+"/scene_dense.* "+self.scenepath)

		self.thread = MeshRunThread(scripts, 4, self.mainWindow)
		if auto:
			self.thread.finished.connect(self.AutoFinished)
		else:
			self.thread.finished.connect(self.onFinished)
		self.thread.start()

	def print_settings(self):
		print("input_path: " + self.input_path + "\n")
		print("output_path: " + self.output_path + "\n")
		print("base_path: " + self.basepath + "\n")
		print("parts: " + str(self.nParts) + "\n")
		print("quality: " + self.quality + "\n")
		print(self.task_num_list)

	def CmdFileGen(self, cmdtext, slaveIndex):
		f1 = open('/home/hadoop/scx/Distribute/tmpData/test' + str(slaveIndex) + '.sh', 'w')
		headtext = "#!/bin/bash\n"
		sshhead = "ssh hadoop@slave" + str(slaveIndex) + " -tt << sshoff\n"
		exittext = "exit\n"
		endtext = "sshoff\n"
		f1.writelines([headtext, sshhead, cmdtext, exittext, endtext] )

#		if self.algo == 'COLMAP':
#			cmdtext = "python " + self.colmapexepath + " --dataset_path " + self.colmap_data_paths[index] + \
#			" --scene_path " + self.outputpaths[index] + "/scene_dense_"+ str(index) +".mvs" + " --pair_file " + 			self.inputpaths[index] + "/pairName.txt" + \
#			" --mvs_img_prefix " + self.scenepath + " --adjust_path_for_mesh " + self.adjust_path_for_mesh + " --resolution " + str(self.resolution) + " --task_id " + str(index) + " --quality " + self.quality + "\n"
#		elif self.algo == 'openMVS':
#			cmdtext = self.openMVSexepath + " -i " + scenename + \
#			" -o " + self.outputpaths[index] + "/scene_dense_" + str(self.index) + ".mvs " + self.configs[index] + " --archive-type 1 \n"
#		elif self.algo == 'gipuma':
#			cmdtext = gipumaexepath + " -mvs_folder " + scenename + \
#			" -output_folder " + self.outputpaths[index] + " --depth_min=-1 --depth_max=-1 --down_scale=4  -remove_black_background\n"  



#				elif self.algo == 'openMVS':
#					child = subprocess.Popen(self.openMVSexepath + " -i "+ self.inputpaths[i] + "scene.mvs" + \
#				       		" -o " + self.outputpaths[i] + "/scene_dense_" + str(i) + ".mvs " + configs[i] + " --archive-type 1 \n" , shell= True)
#					#child.wait()
#				elif self.algo == 'gipuma':    
#					child = subprocess.Popen(self.gipumaexepath + " -mvs_folder "+self.inputpaths[i] + \
#				       	" -output_folder " + self.outputpaths[i] + " --depth_min=-1 --depth_max=-1 --down_scale="+str(self.res_level)+" -remove_black_background \n" , 			shell= True) 
