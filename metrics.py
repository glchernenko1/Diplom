from SSIM_PIL import compare_ssim
from PIL import Image
import cv2
import os



def psnr(im1, im2):
    return cv2.PSNR(cv2.cvtColor(cv2.imread(im1), cv2.COLOR_RGB2BGR), cv2.cvtColor(cv2.imread(im2), cv2.COLOR_RGB2BGR))


def ssim(im1, im2):
    return compare_ssim(Image.open(im1), Image.open(im2))


def compare(generate_path, origin_path):
    average_psnr = 0
    average_ssim = 0
    count = 0
    dir_generator = os.path.abspath(generate_path)
    dir_origin = os.path.abspath(origin_path)
    for g, o in zip(os.listdir(dir_generator), os.listdir(dir_origin)):
        average_psnr += psnr(os.path.join(dir_generator, g), os.path.join(dir_origin, o))
        average_ssim += ssim(os.path.join(dir_generator, g), os.path.join(dir_origin, o))
        count += 1
    return average_ssim / count, average_psnr / count
#чем psnr больше тем лучше
print(psnr(r"C:\Users\google\PycharmProjects\Diplom\height_quality\img00001.png", r"C:\Users\google\PycharmProjects\Diplom\height_quality\img00008.png"))
#print(compare('low_quality', 'low_quality'))

