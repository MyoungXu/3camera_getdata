import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm

# 设置源文件夹和目标文件夹
source_folder = r"D:\PycharmWork\3camera_getdata\output\xjh\voxel"
target_folder = r"D:\PycharmWork\3camera_getdata\output\xjh\event-frame"

# 检查目标文件夹是否存在，如果不存在则创建
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 遍历源文件夹中的所有文件
for file in tqdm(os.listdir(source_folder)):
    if file.endswith('.npy'):
        # 构建完整的文件路径
        file_path = os.path.join(source_folder, file)

        # 读取.npy文件
        data = np.load(file_path)

        # 选择第三个通道 (从0开始计数，即索引为2)
        channel_data = data[2, :, :]

        # 创建一个空的 (256, 256, 3) 图像，初始化为白色 (255, 255, 255)
        image = np.ones((700, 925, 3), dtype=np.uint8) * 255

        # 根据条件设置颜色：正数为蓝色，负数为红色，零为白色（白色已经初始化）
        image[channel_data > 0.1] = [0, 0, 255]  # 蓝色
        image[channel_data < -0.1] = [255, 0, 0]  # 红色

        # 将 NumPy 数组转换为图像对象
        img = Image.fromarray(image)

        # 保存为BMP格式，使用与原始文件相同的名称，但扩展名为 .bmp
        output_file_path = os.path.join(target_folder, file.replace('.npy', '.bmp'))
        img.save(output_file_path)




