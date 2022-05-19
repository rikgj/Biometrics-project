import cv2
from skimage.metrics import peak_signal_noise_ratio
import get_project_folder as get_pf


# load information, replace folder and save to fit your structure
DIM = '256'
IMG_NAME_LIST = './lists/rnd_list_12.txt'
img_folder_reference, ref_name = get_pf.get_gt_folder(DIM)  # Set to GT
img_folder_probe, probe_name = get_pf.get_swinir_folder(DIM)

# save information
file_prefix = DIM + '_' + probe_name
subfolder = DIM + '_PSNR'
SAVE_TO_FILE = f'scores/{DIM}/{subfolder}/{file_prefix}_PSNR.txt'


imgs = []
with open(IMG_NAME_LIST, 'r') as file:
    for line in file:
        line = line.strip()
        imgs.append(line)

scores = []
num_of_imgs = len(imgs)
progress = 0
for img in imgs:
    progress += 1
    if progress % 100 == 0:
        print(progress, '/', num_of_imgs)

    probe = img_folder_probe + '/' + img
    ref = img_folder_reference + '/' + img

    img1 = cv2.imread(ref)
    img2 = cv2.imread(probe)
    psnr = peak_signal_noise_ratio(img1, img2)
    scores.append(psnr)

with open(SAVE_TO_FILE, 'w') as file:
    for score in scores:
        score = str(score)
        file.write(score + '\n')

final_score = sum(scores)/num_of_imgs
print('avg PSNR: ', final_score)
print('PSNR file stored: ', SAVE_TO_FILE)
