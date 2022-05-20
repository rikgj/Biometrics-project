from get_paths import get_file_names
from collections import Counter
import matplotlib.pyplot as plt
import math

FACE_FOLDER = './images/FRGC_cropped'
LIM_START = 5
LIM_END = 25


def get_id_img_info():
    full_names = get_file_names('jpg', FACE_FOLDER)
    ids = [id[0:id.index('d')] for id in full_names]

    # number of images per id
    images_per_id = Counter(ids)
    images_per_id = images_per_id.items()

    # get median score
    img_list = [imgs for id, imgs in images_per_id]
    img_list.sort()
    s = len(img_list)
    median = -1
    if s % 2 == 0:
        i = int(s/2)
        median = img_list[i]
    else:
        i = int(math.floor(s/2))
        median = (img_list[i]+img_list[i+1])/2
    print(f'Median: {median}')

    # plot limit/discard_ids
    plotX = []
    plotY = []
    limits = [i for i in range(LIM_START, LIM_END+1)]

    for limit in limits:
        discard_ids = []
        lost_imgs = 0
        tot = 0
        needed = 0
        remaining_ids = []
        for id, imgs in images_per_id:
            tot += imgs
            if imgs < limit:
                discard_ids.append(id)
                lost_imgs += imgs
            else:
                needed += limit
                remaining_ids.append(id)
        plotX.append(limit)
        plotY.append(len(discard_ids))

        # print info
        print(f'Limit: {limit}')
        print(f'Discarded IDs: {len(discard_ids)}')
        print(f'Remaining IDs: {len(remaining_ids)}')
        print(f'Discarded imgs: {lost_imgs} / {tot}')
        print(f'Requiered imgs: {needed}\n')

    plt.plot(plotX, plotY, marker='o')
    ticks = [x for x in plotX if x % 2 == 0]
    plt.xticks(ticks)
    plt.ylabel('Discarded subjects')
    plt.xlabel('Samples per subject')
    plt.show()


get_id_img_info()
