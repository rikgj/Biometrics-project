'''Support function to get access to project folders '''


def base(dim):
    return f'./images/{dim}/'


def dim_ndim(dim):
    return f'{dim}_{int(int(dim)/4)}'


def get_bicubic_folder(dim):
    return [base(dim) + dim_ndim(dim) + '_Bicubic_x4_' + dim, 'bicubic']


def get_gt_folder(dim):
    return [base(dim) + 'GT_' + dim, 'GT']


def get_bsrgan_folder(dim):
    return [base(dim) + f'LR_{int(int(dim)/4)}_BSRGAN_x4', 'BSRGAN']


def get_swinir_folder(dim):
    return [base(dim) + dim_ndim(dim) + 'swinir_x4', 'SwinIR']
