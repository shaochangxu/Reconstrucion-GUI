import subprocess
import argparse
import os
from time import *

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_path", type=str)
parser.add_argument("--scene_path", type=str)
parser.add_argument("--pair_file", type=str)
parser.add_argument("--mvs_img_prefix", type=str)
parser.add_argument("--adjust_path_for_mesh", type=str)
parser.add_argument("--resolution", type=str)
parser.add_argument("--task_id", type=str)
parser.add_argument("--quality", type=str)
args = parser.parse_args()

dataset_path = args.dataset_path
scene_path = args.scene_path
pair_file_path = args.pair_file
resolution = args.resolution

task_id = args.task_id
colmap_exe_path = "/home/hadoop/scx/colmap/build/src/exe/colmap "


#mvs_img_prefix = "/home/hadoop/scx/Distribute/Scene/Zone14/"
mvs_img_prefix = args.mvs_img_prefix
adjust_path_for_mesh = args.adjust_path_for_mesh
quality = args.quality
#print "feature_extractor:\n"
#subprocess.Popen(colmap_exe_path + "feature_extractor" + " --database_path " + dataset_path + "/database.db" + " --image_path " + dataset_path + "/images " + " --SiftExtraction.max_image_size 1000", shell = True)

#print "exhaustive_matcher:\n"
#subprocess.Popen(colmap_exe_path + "exhaustive_matcher" + " --database_path " + dataset_path +  "/database.db", shell = True)

#print "mapper:\n"
#os.popen("mkdir " + dataset_path + "/sparse")
#subprocess.Popen(colmap_exe_path + "mapper" + " --database_path " + dataset_path +  "/database.db" + " --image_path " + dataset_path + "/images " + " --output_path " + dataset_path + "/sparse" + " --Mapper.ba_local_max_num_iterations 12 --Mapper.ba_global_max_num_iterations 25 --Mapper.ba_global_images_ratio 1.32  --Mapper.ba_global_points_ratio 1.32 --Mapper.ba_global_max_refinements 2", shell = True)

######################################################## Dense Reconstruction Start ##################################################################################3
begin_time = time()
os.popen("rm -r " + dataset_path)
os.popen("mkdir " + dataset_path)
print("mvs2colmap:\n")
#print("/home/hadoop/openMVS/openMVS_test_build/bin/InterfaceCOLMAP" + " -i " + dataset_path +  "../Densify_temp/scene.mvs" + " -o " + dataset_path + " --archive-type 1")
os.system("/home/hadoop/scx/Distribute/openMVS_distribute_build/bin/InterfaceCOLMAP" + " -i " + dataset_path +  "../Densify_temp_" + str(task_id) + "/scene.mvs" + " -o " + dataset_path + " --archive-type 1")
#os.system("/home/hadoop/openMVS/openMVS_test_build/bin/InterfaceCOLMAP" + " -i " + dataset_path +  "../Densify_temp/scene.mvs" + " -o " + dataset_path + " --archive-type 1")

os.popen("mkdir " + dataset_path + "/dense")

print("image_undistorter:\n")
#print(colmap_exe_path + "image_undistorter" + " --image_path "+ dataset_path + "/images" + " --input_path " + dataset_path + "/sparse " + " --output_path " + dataset_path + "/dense" + " --output_type COLMAP " + " max_image_size 1000")

if quality == 'Low':
	os.system(colmap_exe_path + "image_undistorter" + " --image_path "+ "/" + " --input_path " + dataset_path + "/sparse " + " --output_path " + dataset_path + "/dense" + " --output_type COLMAP " + " max_image_size 1000")
elif quality == 'Medium':
	os.system(colmap_exe_path + "image_undistorter" + " --image_path "+ "/" + " --input_path " + dataset_path + "/sparse " + " --output_path " + dataset_path + "/dense" + " --output_type COLMAP " + " max_image_size 1600")
elif quality == 'High':
	os.system(colmap_exe_path + "image_undistorter" + " --image_path "+ "/" + " --input_path " + dataset_path + "/sparse " + " --output_path " + dataset_path + "/dense" + " --output_type COLMAP " + " max_image_size 2400")
elif quality == 'Extreme':
	os.system(colmap_exe_path + "image_undistorter" + " --image_path "+ "/" + " --input_path " + dataset_path + "/sparse " + " --output_path " + dataset_path + "/dense" + " --output_type COLMAP ")
else :
	os.system(colmap_exe_path + "image_undistorter" + " --image_path "+ "/" + " --input_path " + dataset_path + "/sparse " + " --output_path " + dataset_path + "/dense" + " --output_type COLMAP " + " max_image_size " + resolution)

os.popen("rm -r " + dataset_path + "/dense/images/" + mvs_img_prefix + "/undistorted_images/")
os.popen("ln -s -f " + mvs_img_prefix + "/undistorted_images " + dataset_path + "/dense/images/" + mvs_img_prefix)

#print("modify cfg files:\n")
#print("python /home/hadoop/scx/colmap/modify_cfg.py --pair_file " + pair_file_path + " --cfg_dir " + dataset_path + "/dense/stereo")
os.system("python /home/hadoop/scx/colmap/modify_cfg.py --pair_file " + pair_file_path + " --cfg_dir " + dataset_path + "/dense/stereo")

print("patch_match_stereo:\n")
#print(colmap_exe_path + "patch_match_stereo" + " --workspace_path " + dataset_path +  "/dense" + " --workspace_format COLMAP " + " --PatchMatchStereo.max_image_size 1000 --PatchMatchStereo.window_radius 4 --PatchMatchStereo.window_step 2 --PatchMatchStereo.num_samples 7 --PatchMatchStereo.num_iterations 3 --PatchMatchStereo.geom_consistency false ")
if quality == 'Low':
	os.system(colmap_exe_path + "patch_match_stereo" + " --workspace_path " + dataset_path +  "/dense" + " --workspace_format COLMAP " + " --PatchMatchStereo.max_image_size 1000" + " --PatchMatchStereo.window_radius 4 --PatchMatchStereo.window_step 2 --PatchMatchStereo.num_samples 7 --PatchMatchStereo.num_iterations 3 --PatchMatchStereo.geom_consistency false ")
	print("fused:\n")
	os.system(colmap_exe_path + "stereo_fusion" + " --workspace_path " + dataset_path +  "/dense" + " --workspace_format COLMAP " + " --output_path " + dataset_path + "/dense/fused.ply" + " --input_type photometric --StereoFusion.check_num_images 25 --StereoFusion.max_image_size 1000")
elif quality == 'Medium':
	os.system(colmap_exe_path + "patch_match_stereo" + " --workspace_path " + dataset_path +  "/dense" + " --workspace_format COLMAP " + " --PatchMatchStereo.max_image_size 1600" + " --PatchMatchStereo.window_radius 4 --PatchMatchStereo.window_step 2 --PatchMatchStereo.num_samples 10 --PatchMatchStereo.num_iterations 5 --PatchMatchStereo.geom_consistency false ")
	print("fused:\n")
	os.system(colmap_exe_path + "stereo_fusion" + " --workspace_path " + dataset_path +  "/dense" + " --workspace_format COLMAP " + " --output_path " + dataset_path + "/dense/fused.ply" + "  --input_type photometric --StereoFusion.check_num_images 33 --StereoFusion.max_image_size 1600")
elif quality == 'High':
	os.system(colmap_exe_path + "patch_match_stereo" + " --workspace_path " + dataset_path +  "/dense" + " --workspace_format COLMAP " + " --PatchMatchStereo.max_image_size 2400")
	print("fused:\n")
	os.system(colmap_exe_path + "stereo_fusion" + " --workspace_path " + dataset_path +  "/dense" + " --workspace_format COLMAP " + " --output_path " + dataset_path + "/dense/fused.ply" + "--StereoFusion.max_image_size 2400")
elif quality == 'Extreme':
	os.system(colmap_exe_path + "patch_match_stereo" + " --workspace_path " + dataset_path +  "/dense" + " --workspace_format COLMAP ")
	print("fused:\n")
	os.system(colmap_exe_path + "stereo_fusion" + " --workspace_path " + dataset_path +  "/dense" + " --workspace_format COLMAP " + " --output_path " + dataset_path + "/dense/fused.ply")
else:
	os.system(colmap_exe_path + "patch_match_stereo" + " --workspace_path " + dataset_path +  "/dense" + " --workspace_format COLMAP " + " --PatchMatchStereo.max_image_size " + resolution + " --PatchMatchStereo.window_radius 4 --PatchMatchStereo.window_step 2 --PatchMatchStereo.num_samples 7 --PatchMatchStereo.num_iterations 3 --PatchMatchStereo.geom_consistency false ")
	print("fused:\n")
	os.system(colmap_exe_path + "stereo_fusion" + " --workspace_path " + dataset_path +  "/dense" + " --workspace_format COLMAP " + " --output_path " + dataset_path + "/dense/fused.ply" + " --input_type photometric --StereoFusion.check_num_images 25 --StereoFusion.max_image_size " + resolution)


print("colmap2mvs:\n")
os.system("/home/hadoop/scx/Distribute/openMVS_distribute_build/bin/InterfaceCOLMAP" + " -i " + dataset_path + "/dense" + " -o " + scene_path + " --image-folder " + adjust_path_for_mesh + " --archive-type 1")

end_time = time()
run_time = end_time - begin_time
print("dense reconstruction finished, run time is %0.2f s\n"%run_time)
