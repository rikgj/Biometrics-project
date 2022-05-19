import insightface
import numpy as np
import cv2
import os
import get_project_folder as get_pf
import math

# FIXME: check if folder and file exists
# load information, replace folder and save to fit your structure
DIM = '256'
DET_S = int(math.floor(int(DIM)/2))  # must be int
IMG_FOLDER_REFERENCE, REF_NAME = get_pf.get_swinir_folder(DIM)
IMG_FOLDER_PROBE, PROBE_NAME = get_pf.get_swinir_folder(DIM)
REFERENCE_FILE = './lists/rnd_reference_3.txt'
PROBE_FILE = './lists/rnd_probe_9.txt'

# save information
file_prefix = DIM + '_ref_' + REF_NAME + '_probe_' + PROBE_NAME
subfolder = DIM + '_similarity'
SAVE_IMPOSTER = f'scores/{DIM}/{subfolder}/{file_prefix}_imposter_scores.txt'
SAVE_GENUINE = f'scores/{DIM}/{subfolder}/{file_prefix}_genuine_scores.txt'

ERROR_TRACKER = []


# scoring and distance metric provided by ArcFace, cosine
def distance(embeddings1, embeddings2):
    embeddings1 = embeddings1.astype(np.float64)
    embeddings2 = embeddings2.astype(np.float64)

    # Distance based on cosine similarity
    dot = np.sum(np.multiply(embeddings1, embeddings2), axis=0)
    norm = np.linalg.norm(embeddings1, axis=0) * \
        np.linalg.norm(embeddings2, axis=0)
    similarity = dot/norm
    # rstrict score to range 0..1
    similarity = min(1, similarity)
    similarity = max(0, similarity)
    dist = 1-similarity

    return dist


def get_file_as_list(filename):
    ret_list = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            ret_list.append(line)
    return ret_list


def is_same_id(fname1, fname2):
    # assumes name convention [id]d[num]
    i = fname1.index('d')
    return fname1[0:i] == fname2[0:i]


def save_list_to_file(list, path):
    with open(path, 'w') as file:
        for line in list:
            line = str(line)
            file.write(line + '\n')
    print('Data stored at: ', path)


def main():
    # prepare model
    fr_model = insightface.app.FaceAnalysis('buffalo_sc')
    fr_model.prepare(ctx_id=0, det_size=(DET_S, DET_S))

    def get_embeddings(dir, file_list):
        embeddings = []
        goal = len(file_list)
        prog = 0
        err = 0
        for file in file_list:
            prog += 1
            if prog % 100 == 0:
                print(prog, '/', goal)
            path = dir + '/' + file
            img = cv2.imread(path)
            face = fr_model.get(img)
            if len(face) == 0:
                err += 1
                print('ERROR get_embeddings: ', path)
            else:
                embedding = face[0].normed_embedding
                embeddings.append((file, embedding))
        print('ERRORS in get_embeddings: ', err)
        ERROR_TRACKER.append(err)
        return embeddings

    # get embeddings
    print('Getting embeddings\n')
    references = get_file_as_list(REFERENCE_FILE)
    reference_embeddings = get_embeddings(IMG_FOLDER_REFERENCE, references)

    probes = get_file_as_list(PROBE_FILE)
    probe_embeddings = get_embeddings(IMG_FOLDER_PROBE, probes)

    # get distance scores
    print('Calculating scores\n')
    genuine_scores = []
    imposter_scores = []
    num_probes = len(probe_embeddings)
    cur_num = 0
    for probe in probe_embeddings:
        cur_num += 1
        if cur_num % 50 == 0:
            print(cur_num, '/', num_probes)
        probe_id = probe[0]
        probe_emb = probe[1]
        for reference in reference_embeddings:
            ref_id = reference[0]
            ref_emb = reference[1]
            dist = distance(probe_emb, ref_emb)
            if is_same_id(probe_id, ref_id):
                genuine_scores.append(dist)
            else:
                imposter_scores.append(dist)

    save_list_to_file(genuine_scores, SAVE_GENUINE)
    save_list_to_file(imposter_scores, SAVE_IMPOSTER)

    print('Embedding_errors reference : ', ERROR_TRACKER[0])
    print('Embedding_errors probe     : ', ERROR_TRACKER[1])


if __name__ == '__main__':
    if os.path.exists(SAVE_GENUINE) or os.path.exists(SAVE_IMPOSTER):
        print('Score files exists, delete or rename, before running this')
        print(SAVE_GENUINE)
        print(SAVE_IMPOSTER)
    else:
        main()
