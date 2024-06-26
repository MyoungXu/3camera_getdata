import os
import datetime
from PIL import Image
from tqdm import tqdm

# 设置文件夹路径
folderA = r'D:\PycharmWork\e2calib-main\output\final'
current_date = datetime.datetime.now()
date = current_date.strftime('%Y%m%d')

folderB = os.path.join('data', date, 'event')

base_folder = os.path.join('data', date)
if not os.path.exists(base_folder):
    os.makedirs(base_folder)
if not os.path.exists(folderB):
    os.makedirs(folderB)

# 获取A文件夹中所有PNG图像文件名
filesA = [f for f in os.listdir(folderA) if f.endswith('.png')]

# 初始化计数器
fileCount = 1

# 遍历A文件夹中的PNG图像文件
for filenameA in tqdm(filesA):
    # 读取PNG图像
    img = Image.open(os.path.join(folderA, filenameA))
    # 构造保存文件名（以BMP格式）
    fileCount += 1
    filenameB = f'image_{fileCount:08d}.bmp'
    # 保存翻转后的图像到B文件夹
    img.save(os.path.join(folderB, filenameB))
