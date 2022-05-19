from get_paths import get_file_names
import os

FILE_LIST = 'rnd_list_12.txt'
DIRS = []  # add folders to filter
# '256_64_swinir_real_sr_x4', '256_64_cropped_BSRGAN_x4', '256_64_cropped',
# '256_cropped', '512_128_swinir_real_sr_x4', '512_128_cropped', '512_cropped'


def main():
    # get list of imgs to keep
    rnd_list = []
    with open(FILE_LIST, 'r') as file:
        for line in file:
            line = line.strip()
            rnd_list.append(line)

    for dir in DIRS:
        print(dir)
        dir = dir + '/'
        names = get_file_names('jpg', dir)

        print('Files in DIR: ', len(names))
        for name in names:
            if name not in rnd_list:
                # remove files not in list
                path = dir + name
                os.remove(path)

        names = get_file_names('jpg', dir)
        print('Files in DIR: ', len(names))
        print('Files in rnd_list: ', len(rnd_list))


if __name__ == '__main__':
    q = 'This function deletes files, do you wish to continue? Y/N  --  '
    if input(q).capitalize() == 'Y':
        main()
