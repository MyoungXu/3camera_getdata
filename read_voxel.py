import os
import numpy as np
import matplotlib.pyplot as plt


# 设置源文件夹和目标文件夹
source_folder = r"D:\PycharmWork\3camera_getdata\output\xjh\voxel"
target_folder = r"D:\PycharmWork\3camera_getdata\output\xjh\visible_voxel"

# 检查目标文件夹是否存在，如果不存在则创建
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 遍历源文件夹中的所有文件
for file in os.listdir(source_folder):
    if file.endswith('.npy'):
        # 构建完整的文件路径
        file_path = os.path.join(source_folder, file)

        # 读取.npy文件
        data = np.load(file_path)
        data = np.moveaxis(data, 0, -1)

        # 设置显示范围
        vmin = -3
        vmax = 3

        # 创建五个子图
        fig, axes = plt.subplots(1, 5, figsize=(20, 4))

        # 循环遍历每个通道并可视化
        for i, ax in enumerate(axes):
            ax.imshow(data[:, :, i], cmap='gray', vmin=vmin, vmax=vmax)  # 设置显示范围
            ax.set_title(f'Channel {i+1}')
            ax.set_axis_off()  # 关闭坐标轴
            fig.colorbar(ax.imshow(data[:, :, i], cmap='gray', vmin=vmin, vmax=vmax), ax=ax)
            if i == 2:  # 索引从0开始，因此i == 2 表示第三个通道
                img_path = os.path.join(target_folder, file.replace('.npy', '.bmp'))
                plt.imsave(img_path, data[:, :, i], cmap='gray', vmin=vmin, vmax=vmax)

        plt.close(fig)
