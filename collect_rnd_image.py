import get_project_folder as get_pf
import get_paths
import random
import shutil
import os

DIMS = ['64', '128', '256']
SAVE_AT = './img_report'
EXT = 'jpg'

# get a random image from lowest res (highest embedding loss)
sw_dir = get_pf.get_swinir_folder(64)
file_names = get_paths.get_file_names(EXT, sw_dir[0])
image_name = random.choice(file_names)

# create a folder for image
base_folder = f'{SAVE_AT}/{image_name[0:len(image_name)-len(EXT)-1]}'
os.mkdir(base_folder)

# gather image from all folder, and copy
for dim in DIMS:
    sw_dir = get_pf.get_swinir_folder(dim)
    bi_dir = get_pf.get_bicubic_folder(dim)
    gt_dir = get_pf.get_gt_folder(dim)
    br_dir = get_pf.get_bsrgan_folder(dim)
    dirs = [sw_dir, bi_dir, gt_dir, br_dir]

    for i in range(len(dirs)):
        source = f'{dirs[i][0]}/{image_name}'
        prefix = dirs[i][1]
        destination = f'{base_folder}/{dim}_{prefix}.{EXT}'

        shutil.copy(source, destination)
