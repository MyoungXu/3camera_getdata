import datetime
import os
import shutil


def copy_files_with_same_names(A_folder, B_folder, C_folder):
    # 获取A文件夹中所有文件名
    filenames_A = os.listdir(A_folder)

    for filename in filenames_A:
        # 构建B文件夹中的完整路径
        src_file = os.path.join(B_folder, filename)

        # 检查文件是否存在于B文件夹中
        if os.path.exists(src_file):
            # 构建C文件夹中的完整路径
            dst_file = os.path.join(C_folder, filename)

            # 复制文件
            shutil.copy(src_file, dst_file)


current_date = datetime.datetime.now()
date = current_date.strftime('%Y%m%d')
base_folder = os.path.join('data', date)

A_folder = os.path.join(base_folder, 'get', 'sample')  # 替换为A文件夹的路径
B_folder = os.path.join(base_folder, 'cam1')  # 替换为B文件夹的路径
C_folder = os.path.join(base_folder, 'get', 'cam1')  # 替换为C文件夹的路径
copy_files_with_same_names(A_folder, B_folder, C_folder)
B_folder = os.path.join(base_folder, 'cam2')  # 替换为B文件夹的路径
C_folder = os.path.join(base_folder, 'get', 'cam2')  # 替换为C文件夹的路径
copy_files_with_same_names(A_folder, B_folder, C_folder)
B_folder = os.path.join(base_folder, 'event')  # 替换为B文件夹的路径
C_folder = os.path.join(base_folder, 'get', 'event')  # 替换为C文件夹的路径
copy_files_with_same_names(A_folder, B_folder, C_folder)
