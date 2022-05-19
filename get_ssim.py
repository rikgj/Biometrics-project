import cv2
from skimage.metrics import structural_similarity
import get_project_folder as get_pf

# FIXME: check if folder exists, and if file exists
# load information, replace folder and save to fit your structure
DIM = '256'
IMG_NAME_LIST = './lists/rnd_list_12.txt'
IMG_FOLDER_REFERENCE, REF_NAME = get_pf.get_gt_folder(DIM)  # this should be GT
IMG_FOLDER_PROBE, PROBE_NAME = get_pf.get_swinir_folder(DIM)

# save information
file_prefix = DIM + '_' + PROBE_NAME
subfolder = DIM + '_SSIM'
SAVE_TO_FILE = f'scores/{DIM}/{subfolder}/{file_prefix}_SSIM.txt'


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
    probe = IMG_FOLDER_PROBE + '/' + img
    ref = IMG_FOLDER_REFERENCE + '/' + img
    img1 = cv2.imread(ref)
    img2 = cv2.imread(probe)

    # Convert images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    ssim = structural_similarity(img1, img2)
    scores.append(ssim)

with open(SAVE_TO_FILE, 'w') as file:
    for score in scores:
        file.write(str(score) + '\n')

final_score = sum(scores)/num_of_imgs
print('avg SSIM: ', final_score)
print('SSIM file stored: ', SAVE_TO_FILE)
