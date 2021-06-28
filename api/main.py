import os
import numpy as np
from datetime import datetime
from PIL import Image, ImageEnhance

def renderImage(i, res_list, r_list, g_list, b_list, imagePath, return_dict):

    # Get res in path
    imagePathRes = imagePath + 'R' + res_list[i] + 'm/'

    # Import bands
    print(f'Starting job {i+1} of {len(res_list)}...')
    bandR = Image.open(imagePathRes + 'T29TQH_20210605T110619_' + r_list[i] + '_' + res_list[i] + 'm.jp2')
    bandG = Image.open(imagePathRes + 'T29TQH_20210605T110619_' + g_list[i] + '_' + res_list[i] + 'm.jp2')
    bandB = Image.open(imagePathRes + 'T29TQH_20210605T110619_' + b_list[i] + '_' + res_list[i] + 'm.jp2')

    print(f'Bands read. Rendering image {i+1} of {len(res_list)}...')

    # We divide by 2^8 to transform from uint16 to uint8 range
    b_r = np.asarray(bandR)/256
    b_g = np.asarray(bandG)/256
    b_b = np.asarray(bandB)/256

    # We assemble the combined color rgb image
    RGB_gt = np.zeros([len(b_r), len(b_r[0]), 3], np.uint8)
    RGB_gt[:, :, 0] = b_r
    RGB_gt[:, :, 1] = b_g
    RGB_gt[:, :, 2] = b_b

    # Get pillow object again and increase brightness
    RGB_gt = Image.fromarray(RGB_gt)
    enhancer = ImageEnhance.Brightness(RGB_gt)
    factor = 10
    im_output = enhancer.enhance(factor)

    # Crop area of interest
    im_crop = im_output.crop((im_output.size[0]*1/4, im_output.size[1]*2/7, im_output.size[0]*3/4, im_output.size[1]*5/7))

    # Get datetime now
    now = datetime.now().strftime('%Y%m%d-%H%M%S')
    fileString = f'./Output/{now}_R{res_list[i]}m_{r_list[i]}_{g_list[i]}_{b_list[i]}.jpg'
    im_crop.save(fileString)

    print(f'Done job {i+1} of {len(res_list)}...')

    return_dict[i] = fileString
