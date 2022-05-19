import os.path
import logging
import torch
import glob

from utils import utils_logger
from utils import utils_image as util
from models.network_rrdbnet import RRDBNet as net


"""
Spyder (Python 3.6-3.7)
PyTorch 1.4.0-1.8.1
Windows 10 or Linux
Kai Zhang (cskaizhang@gmail.com)
github: https://github.com/cszn/BSRGAN
        https://github.com/cszn/KAIR
If you have any question, please feel free to contact with me.
Kai Zhang (e-mail: cskaizhang@gmail.com)
by Kai Zhang ( March/2020 --> March/2021 --> )
This work was previously submitted to CVPR2021.

# --------------------------------------------
@inproceedings{zhang2021designing,
  title={Designing a Practical Degradation Model for Deep Blind Image Super-Resolution},
  author={Zhang, Kai and Liang, Jingyun and Van Gool, Luc and Timofte, Radu},
  booktitle={arxiv},
  year={2021}
}
# --------------------------------------------
ALTERATIONS OF THE CODE BY OTHER THAN AUTHOR
- No alterations to the method itself
- Added filtering, checking if file exists in E_path
- Removed commentet code, and some print statements
"""


def main():
    FOLDER_DIM = 256
    EXTENSION = 'jpg'  # file format of images, eg 'jpg'

    utils_logger.logger_info('blind_sr_log', log_path='blind_sr_log.log')
    logger = logging.getLogger('blind_sr_log')

    sf = 4
    testsets = f'../../images/{FOLDER_DIM}'  # fixed, set path of testsets
    testset_Ls = [f'LR_{int(FOLDER_DIM/sf)}']  # LR folder

    model_names = ['RRDB', 'ESRGAN', 'FSSR_DPED',
                   'FSSR_JPEG', 'RealSR_DPED', 'RealSR_JPEG']
    model_names = ['BSRGAN']    # 'BSRGANx2' for scale factor 2

    save_results = True
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    for model_name in model_names:
        if model_name in ['BSRGANx2']:
            sf = 2
        model_path = os.path.join(
            'model_zoo', model_name+'.pth')          # set model path
        logger.info('{:>16s} : {:s}'.format('Model Name', model_name))

        # define network and load model
        model = net(in_nc=3, out_nc=3, nf=64, nb=23,
                    gc=32, sf=sf)  # define network

        model.load_state_dict(torch.load(model_path), strict=True)
        model.eval()
        for k, v in model.named_parameters():
            v.requires_grad = False
        model = model.to(device)
        torch.cuda.empty_cache()

        for testset_L in testset_Ls:

            L_path = os.path.join(testsets, testset_L)
            E_path = os.path.join(testsets, testset_L+'_BSRGAN_x'+str(sf))
            util.mkdir(E_path)

            logger.info('{:>16s} : {:s}'.format('Input Path', L_path))
            logger.info('{:>16s} : {:s}'.format('Output Path', E_path))
            idx = 0

            # make a filter list
            filter_names = []
            dir = E_path + '/'  # dir to filter from
            search = f'{dir}*.{EXTENSION}'
            EXTENSION = len(EXTENSION)+1  # get len of '.jpg'
            filter_paths = glob.glob(search)

            if len(filter_paths) > 0:
                # offset due to special character '\\'
                i = filter_paths[0].rindex('\\')+1
                filter_names = [f[i:len(f)-EXTENSION] for f in filter_paths]

            for idx, img in enumerate(sorted(glob.glob(os.path.join(L_path, '*')))):
                # --------------------------------
                # (1) img_L
                # --------------------------------
                img_name, ext = os.path.splitext(os.path.basename(img))
                if img_name in filter_names:
                    print(img_name)
                    continue

                logger.info(
                    '{:->4d} --> {:<s} --> x{:<d}--> {:<s}'.format(idx, model_name, sf, img_name+ext))

                img_L = util.imread_uint(img, n_channels=3)
                img_L = util.uint2tensor4(img_L)
                img_L = img_L.to(device)

                # --------------------------------
                # (2) inference
                # --------------------------------
                img_E = model(img_L)

                # --------------------------------
                # (3) img_E
                # --------------------------------
                img_E = util.tensor2uint(img_E)
                if save_results:
                    util.imsave(img_E, os.path.join(E_path, img_name+'.jpg'))


if __name__ == '__main__':
    main()
