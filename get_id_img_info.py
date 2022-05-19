from get_paths import get_file_names
from collections import Counter
import matplotlib.pyplot as plt

FACE_FOLDER = './images/FRGC_cropped'
LIM_START = 5
LIM_END = 25

limits = [i for i in range(LIM_START, LIM_END+1)]


def get_id_img_info():
    full_names = get_file_names('jpg', FACE_FOLDER)
    i = full_names[0].index('d')
    ids = [id[0:i] for id in full_names]

    # number of images
    images_per_id = Counter(ids)

    # get number of ids with imgs
    images_per_id = images_per_id.items()

    plotX = []
    plotY = []

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
