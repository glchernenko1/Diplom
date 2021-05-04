from SSIM_PIL import compare_ssim
from PIL import Image
import cv2
import os
import numpy as np


# чем psnr больше тем лучше
def psnr(im1, im2):
    return cv2.PSNR(cv2.cvtColor(cv2.imread(im1), cv2.COLOR_RGB2BGR), cv2.cvtColor(cv2.imread(im2), cv2.COLOR_RGB2BGR))


def ssim(im1, im2):
    return compare_ssim(Image.open(im1), Image.open(im2))


# чем меньше тем лучше
def rmse(im1, im2):
    err = np.sum((cv2.imread(im1).astype("float") - cv2.imread(im2).astype("float")) ** 2)
    err /= float(cv2.imread(im1).shape[0] * cv2.imread(im1).shape[1])
    return np.sqrt(err)


def compare(generate_path, origin_path):
    average_psnr = 0
    average_ssim = 0
    average_rmse = 0
    count = 0
    dir_generator = os.path.abspath(generate_path)
    dir_origin = os.path.abspath(origin_path)
    for g, o in zip(os.listdir(dir_generator), os.listdir(dir_origin)):
        average_psnr += psnr(os.path.join(dir_generator, g), os.path.join(dir_origin, o))
        average_ssim += ssim(os.path.join(dir_generator, g), os.path.join(dir_origin, o))
        average_rmse += rmse(os.path.join(dir_generator, g), os.path.join(dir_origin, o))
        count += 1
    return average_ssim / count, average_psnr / count, average_rmse / count


# print(rmse(r"C:\Users\google\PycharmProjects\Diplom\height_quality\img00001.png", r"C:\Users\google\PycharmProjects\Diplom\height_quality\img00007.png"))
