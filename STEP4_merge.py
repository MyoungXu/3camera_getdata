import datetime

from PIL import Image
import os

from tqdm import tqdm


current_date = datetime.datetime.now()
date = current_date.strftime('%Y%m%d')

# 定义三个文件夹目录和保存合并图的目录
folder1 = os.path.join('data', date, 'cam1')
folder2 = os.path.join('data', date, 'cam1')
folder3 = os.path.join('data', date, 'event')
output_folder = os.path.join('data', date, 'merge')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    folder = os.path.join('data', date, 'get')
    os.makedirs(folder)
    os.makedirs(os.path.join(folder, 'cam1'))
    os.makedirs(os.path.join(folder, 'cam2'))
    os.makedirs(os.path.join(folder, 'event'))
    os.makedirs(os.path.join(folder, 'cam1'))


# 获取三个文件夹中的文件列表
files1 = os.listdir(folder1)
files2 = os.listdir(folder2)
files3 = os.listdir(folder3)

# 定义缩小后的图像大小
target_size = (1500, 600)  # 修改为你想要的大小

# 获取三个文件夹中的文件列表
files1 = os.listdir(folder1)
files2 = os.listdir(folder2)
files3 = os.listdir(folder3)

# 遍历文件列表，合并同名图片并缩小
for filename in tqdm(files1):
    if filename in files2 and filename in files3:
        # 打开三个文件夹中对应的图片
        img1 = Image.open(os.path.join(folder1, filename))
        img2 = Image.open(os.path.join(folder2, filename))
        img3 = Image.open(os.path.join(folder3, filename))

        # 创建新的合并图
        merged_img = Image.new('RGB', (img1.width + img2.width + img3.width, max(img1.height, img2.height, img3.height)))

        # 将三张图片合并到一张图上
        merged_img.paste(img1, (0, 0))
        merged_img.paste(img2, (img1.width, 0))
        merged_img.paste(img3, (img1.width + img2.width, int((img1.height - img3.height)/2)))

        # 缩小图像
        merged_img = merged_img.resize(target_size)

        # 保存合并后的图到输出目录
        merged_img.save(os.path.join(output_folder, filename))

print("合并并缩小完成，并保存至输出目录。")
