

# Download the pre-trained models
!wget https://github.com/cszn/KAIR/releases/download/v1.0/BSRGAN.pth -P BSRGAN/model_zoo
!wget https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth -P experiments/pretrained_models


# Run SRs
## BSRGAN
Change testsets, and testset_Ls to decide input and output folder
Change name convention for outputed files in the loop "for testset_L in testset_Ls" (line 88)

cd BSRGAN
python main_test_bsrgan.py

## SwinIR
Navigate to "def setup(args):" in main_test_swinir.py in order to change where the images are stored
You control the input folder for the images in the command below --folder_lq [path_to_images]

The commands below assumes you are in SR folder

// 64_16
python SwinIR/main_test_swinir.py --task real_sr --model_path experiments/pretrained_models/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth --folder_lq ../images/64/LR_16 --scale 4

// 128_32
python SwinIR/main_test_swinir.py --task real_sr --model_path experiments/pretrained_models/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth --folder_lq ../images/128/LR_32 --scale 4

// 256_64
python SwinIR/main_test_swinir.py --task real_sr --model_path experiments/pretrained_models/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth --folder_lq ../images/256/LR_64 --scale 4
