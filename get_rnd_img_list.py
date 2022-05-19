from get_paths import get_file_names
from collections import Counter
import glob
import random
import os

FACE_FOLDER = './images/FRGC_cropped'
LIMIT = 12
SAVE_TO_FILE = './lists/rnd_list_' + str(LIMIT) + '.txt'


def create_rnd_list():
    full_names = get_file_names('jpg', FACE_FOLDER)
    i = full_names[0].index('d')
    ids = [id[0:i] for id in full_names]

    # number of images
    images_per_id = Counter(ids)

    # get number of ids with imgs
    images_per_id = images_per_id.items()

    discard_ids = []
    lost_imgs = 0
    tot = 0
    needed = 0
    remaining_ids = []
    for id, imgs in images_per_id:
        tot += imgs
        if imgs < LIMIT:
            discard_ids.append(id)
            lost_imgs += imgs
        else:
            needed += LIMIT
            remaining_ids.append(id)

    # print info
    print('Discarded IDs:  ', len(discard_ids))
    print('Remaining IDs:  ', len(remaining_ids))
    print('Discarded imgs: ', lost_imgs, '/', tot)
    print('Requiered imgs: ', needed)

    # select LIMIT rnd imgs from remaining ids
    num_id = 1
    remaining_ids_rnd_imgs = []
    for id in remaining_ids:
        print(num_id, id)
        num_id += 1
        # get all images related to id
        search = FACE_FOLDER + '/' + id + '*'
        paths = glob.glob(search)
        i = paths[0].rindex('\\')+1  # offset due to special character '\\'
        imgs = [f[i:] for f in paths]
        rnd_list = random.sample(imgs, k=LIMIT)
        remaining_ids_rnd_imgs.append(rnd_list)

        if len(rnd_list) != LIMIT:
            print('ERROR - rnd_list not of size LIMIT')

    print('Done, writing to file')

    textfile = open(SAVE_TO_FILE, "w")
    for id in remaining_ids_rnd_imgs:
        for img in id:
            textfile.write(img + "\n")
    textfile.close()
    print('File closed')


if __name__ == '__main__':
    if os.path.exists(SAVE_TO_FILE) is False:
        create_rnd_list()
    else:
        print('In order to make new rnd_list, delete or rename ', SAVE_TO_FILE)
