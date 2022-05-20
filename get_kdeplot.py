import pandas as pd
import seaborn as sb
import numpy as np
from matplotlib import pyplot as plt


# = f'scores/{dim}/{subfolder}/{file_prefix}_imposter_scores.txt'
# = f'scores/{dim}/{subfolder}/{file_prefix}_genuine_scores.txt'
# bicubic
# BSRGAN
# GT
# SwinIR
DIMS = ['64', '128', '256']
# DIMS = ['64']
REF_NAME = 'GT'
PROBE_NAME = 'bicubic'
BASE = 'true_sim_score'


def get_scores(path):
    scores = []
    with open(path) as file:
        for line in file:
            line = line.strip()
            scores.append(float(line))
    return scores


n = 0
line_sty = ['dotted', 'solid', 'dashed']
for dim in DIMS:
    file_prefix = f'{dim}_ref_{REF_NAME}_probe_{PROBE_NAME}'
    gen_path = f'{BASE}/{dim}/{file_prefix}_genuine_scores.txt'
    imp_path = f'{BASE}/{dim}/{file_prefix}_imposter_scores.txt'

    # get scores from file
    print(f'{dim} - Getting scores')
    gen_scores = get_scores(gen_path)
    print(f'{dim} - Gen scores loaded')
    imp_scores = get_scores(imp_path)
    print(f'{dim} - Imp scores loaded')

    # plot figure

    sb.kdeplot(gen_scores, color='red', linestyle=line_sty[n], label=f'{dim}')
    sb.kdeplot(imp_scores, color='black', linestyle=line_sty[n])

    plt.title(f'Ref: {REF_NAME} Probe: {PROBE_NAME}')
    n += 1
    plt.legend()
plt.show()
