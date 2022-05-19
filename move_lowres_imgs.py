import cv2
import glob
import shutil

# read pictures in folder and remove images with dim < MIN_DIM
FROM_PATH = './images/FRGC_cropped'
TO_PATH = './error/discarded_images'
MIN_DIM = 256


def main():
    search = FROM_PATH + '/*.jpg'
    file_paths = glob.glob(search)

    # offset due to special character '\\'
    name_i = file_paths[0].rindex('\\')+1

    removed = 0
    prog = 0
    lim = len(file_paths)

    for path in file_paths:
        img = cv2.imread(path)
        height, width, channels = img.shape
        if height < MIN_DIM:
            file_name = path[name_i:]
            dest = TO_PATH + '/' + file_name
            shutil.move(path, dest)
            removed += 1

        prog += 1
        if prog % 100 == 0:
            print(f'Progress: {prog} / {lim}')

    print(f'Moved: {removed} files to {TO_PATH}')


if __name__ == '__main__':
    main()
