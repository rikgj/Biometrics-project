import cv2
import glob
import os

# add dimensions if needed, each creates a folder with dxd images
DIMS = [256]
FROM_PATH = './images/256/LR_64'
IMG_EXTENSION = 'jpg'
# dim in DIMS will be added at the end
TO_PATH = './images/256/256_64_Bicubic_x4'
GET_IMGS_FROM_LIST = True  # if False use all imgs in FROM_PATH
IMG_LIST_PATH = './lists/rnd_list_12.txt'

file_names = []
if GET_IMGS_FROM_LIST:
    with open(IMG_LIST_PATH) as file:
        for line in file:
            line = line.strip()
            file_names.append(line)
else:
    search = FROM_PATH + '/*.' + IMG_EXTENSION
    file_paths = glob.glob(search)
    # \\ is a special character, therefore offset is 1
    i = file_paths[0].rindex('\\') + 1
    file_names = [f[i:] for f in file_paths]

for dim in DIMS:
    to_path = TO_PATH + '_' + str(dim)

    if os.path.isdir(to_path):
        a = input(to_path + ' already exists, do you want to continue? Y/N --')
        if a.capitalize() != 'Y':
            # skip this dim
            print('Skipped ', dim)
            continue
    else:
        os.mkdir(to_path)
        print('Creating ' + to_path)

    tot_files = len(file_names)
    prog = 0
    for name in file_names:
        prog += 1
        read_path = FROM_PATH + '/' + name
        n_img = cv2.imread(read_path, cv2.IMREAD_UNCHANGED)
        n_img = cv2.resize(n_img, (dim, dim), interpolation=cv2.INTER_CUBIC)

        write_path = to_path + '/' + name
        cv2.imwrite(write_path, n_img)

        if prog % 200 == 0:
            print(str(prog) + ' / ' + str(tot_files))
