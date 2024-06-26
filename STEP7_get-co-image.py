import datetime
import os
import xjh_stereo_config
from Utils import *
from tqdm import tqdm
from metavision_core.event_io.raw_reader import RawReader


def delete_files_without_matching_names(A_folder, B_folder):
    # 获取A文件夹中所有文件名
    filenames_A = os.listdir(A_folder)
    # 获取B文件夹中所有文件名
    filenames_B = os.listdir(B_folder)
    # 将B文件夹中的文件名放入一个集合中，以便快速查找
    existing_files_B = set(filenames_B)
    # 遍历A文件夹中的文件名
    for filename in filenames_A:
        # 检查文件是否存在于B文件夹中
        if filename not in existing_files_B:
            # 构建文件的完整路径
            file_path = os.path.join(A_folder, filename)

            # 删除文件
            os.remove(file_path)


if __name__ == '__main__':

    current_date = datetime.datetime.now()
    date = current_date.strftime('%Y%m%d')
    base_folder = os.path.join('data', date, 'get')
    # 设置图像文件夹路径
    cam1_folder = os.path.join(base_folder, 'cam1')
    cam2_folder = os.path.join(base_folder, 'cam2')
    out1_folder = os.path.join(base_folder, 'co_cam1')
    out2_folder = os.path.join(base_folder, 'co_cam2')
    if not os.path.exists(out1_folder):
        os.makedirs(out1_folder)
    if not os.path.exists(out2_folder):
        os.makedirs(out2_folder)

    height = 1080
    width = 1440

    # 读取文件夹中的所有文件
    cam1_files = os.listdir(cam1_folder)

    config1 = xjh_stereo_config.cam1cam2()
    map1x, map1y, map2x, map2y, _, _ = getRectifyTransform(height, width, config1, alpha=1.0)

    for image_file in tqdm(cam1_files):
        # 拼接图像文件的完整路径
        image_path = os.path.join(cam1_folder, image_file)
        # 读取图像
        img = cv2.imread(image_path)
        # 应用rectification映射
        new_img = cv2.remap(img, map1x, map1y, cv2.INTER_AREA)
        # 保存rectified图像
        cv2.imwrite(os.path.join(out1_folder, image_file), new_img)

        # 拼接图像文件的完整路径
        image_path = os.path.join(cam2_folder, image_file)
        # 读取图像
        img = cv2.imread(image_path)
        # 应用rectification映射
        new_img = cv2.remap(img, map2x, map2y, cv2.INTER_AREA)
        # 保存rectified图像
        cv2.imwrite(os.path.join(out2_folder, image_file), new_img)

    A_folder = os.path.join(base_folder, 'event')  # 替换为A文件夹的路径
    B_folder = os.path.join(base_folder, 'co_cam1')  # 替换为B文件夹的路径
    delete_files_without_matching_names(A_folder, B_folder)
