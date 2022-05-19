import cv2
import glob
import shutil
import insightface
import math

# FIXME: There is no boundary check when using correction, and padding

# read pictures in folder, crop and store in new folder
FROM_PATH = './images/FRGC_original'
TO_PATH = './images/FRGC_cropped'
NO_FACE_PATH = './error/no_face_found'
ERROR_IMG_PATH = './error/error_image'
ERROR_TEXT_PATH = './error/error_log.txt'
IMAGE_EXT = 'jpg'
FILTER_LIST = False  # set to True in order to use filter finished files

# # prepare model
fr_model = insightface.app.FaceAnalysis('buffalo_sc')
fr_model.prepare(ctx_id=0, det_size=(320, 320))


def main():
    search = FROM_PATH + '/*.' + IMAGE_EXT
    file_paths = glob.glob(search)

    i = file_paths[0].rindex('\\')+1  # offset due to special character '\\'
    file_names = [f[i:] for f in file_paths]

    if FILTER_LIST:
        dirs = [TO_PATH, NO_FACE_PATH, ERROR_IMG_PATH]  # dirs to filter from
        for dir in dirs:
            search = dir + '/*.jpg'
            filter_paths = glob.glob(search)
            # offset due to special character '\\'
            if len(filter_paths) > 0:
                i = filter_paths[0].rindex('\\')+1
                filter_names = [f[i:] for f in filter_paths]
                file_names = [
                    name for name in file_names if name not in filter_names]

    print(f'Total files: {len(file_names)}')
    lim = len(file_names)
    no_face_found = 0

    for i in range(lim):
        name = file_names[i]
        path = FROM_PATH + '/' + name

        # perform action on image
        status, img = crop_image(path)
        if status:
            try:
                save_to = TO_PATH + '/' + name
                cv2.imwrite(save_to, img)

            except Exception as e:
                print('Error saved')
                save_to = ERROR_IMG_PATH + '/' + name
                shutil.copyfile(path, save_to)
                errorMsg = path + ' - ERROR: \n' + str(e) + '\n\n'
                with open(ERROR_TEXT_PATH, 'a') as f:
                    f.write(errorMsg)

        else:
            save_to = NO_FACE_PATH + '/' + name
            shutil.copyfile(path, save_to)
            no_face_found += 1

        if i % 50 == 0:
            print(f'Image: {i} of {lim}')
            print(f'Done with files to: {name}')

    print(f'Images with no faces: {no_face_found}')


def diff_distribution(diff):
    # return equal distibution +-1 for image scaling
    m = diff % 2
    diff += m
    ldiff = int(diff/2)
    return [ldiff, diff-m]


def crop_image(image_path):
    img = cv2.imread(image_path)
    # FIXME: Use protperies below to implement boundery control
    # max_height, max_width, channels = img.shape
    faces = fr_model.get(img)

    if faces != []:
        bbox = faces[0]['bbox']
        bbox = [math.floor(b) for b in bbox]
        bbox[0] = 0 if bbox[0] < 0 else bbox[0]
        bbox[1] = 0 if bbox[1] < 0 else bbox[1]

        topX = bbox[0]
        topY = bbox[1]
        bottomX = bbox[2]
        bottomY = bbox[3]

        # scale to 1:1 by expanding to the largest axis
        height = bottomY - topY
        width = bottomX - topX
        diff = abs(height-width)
        correction = diff_distribution(diff)

        if height > width:
            topX -= correction[0]
            width += correction[1]
        else:
            topY -= correction[0]
            height += correction[1]

        img = img[topY:topY+height, topX:topX + width]
        return (True, img)
    else:
        return (False, None)


if __name__ == '__main__':
    main()
