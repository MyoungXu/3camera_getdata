import datetime
import os
from PIL import Image
from tqdm import tqdm


def flip_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中所有BMP图像文件名
    files = [f for f in os.listdir(input_folder) if f.endswith('.bmp')]

    for filename in tqdm(files):
        # 读取BMP图像
        img = Image.open(os.path.join(input_folder, filename))
        # 左右翻转图像
        flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        # 构造保存文件名
        output_path = os.path.join(output_folder, filename)
        # 保存翻转后的图像到输出文件夹
        flipped_img.save(output_path)


# 指定输入和输出文件夹路径
basefolder = r'F:\000002'
current_date = datetime.datetime.now()
date = current_date.strftime('%Y%m%d')

input_folder1 = os.path.join(basefolder, 'cam1')
input_folder2 = os.path.join(basefolder, 'cam2')
output_folder1 = os.path.join('data', date, 'cam1')
output_folder2 = os.path.join('data', date, 'cam2')

flip_images_in_folder(input_folder1, output_folder1)
flip_images_in_folder(input_folder2, output_folder2)
