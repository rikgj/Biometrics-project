import glob


def get_paths(extension, dir):
    search = dir + '/*.' + extension
    paths = glob.glob(search)
    return paths


def get_file_names(extension, dir):
    paths = get_paths(extension, dir)

    if len(paths) > 0:
        i = paths[0].rindex('\\')+1  # offset due to special character '\\'
        names = [f[i:] for f in paths]

    return names
