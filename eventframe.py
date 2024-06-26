from tqdm import tqdm

import xjh_stereo_config
from Utils import *

event_path = r'D:\PycharmWork\e2calib-main\output\008n'
output_path = r'result\008'

height = 1080
width = 1440
load_scale = [0, 1]  # 读取多少比例的图片
after_crop = [320, 576, 700, 956]   # HW（小系统）

if not os.path.exists(output_path):
    os.makedirs(output_path)

config2 = xjh_stereo_config.cameve()
map2x_2, map2y_2, map1x_2, map1y_2, maps2_f_2, maps1_f_2 = getRectifyTransform(height, width, config2, alpha=1.0)

cam1_files = os.listdir(event_path)
imgs_name_len = len(cam1_files)
for image_file in tqdm(cam1_files[int(imgs_name_len * load_scale[0]):int(imgs_name_len * load_scale[1])]):
    # 拼接图像文件的完整路径
    image_path = os.path.join(event_path, image_file)

    # 读取图像
    img = cv2.imread(image_path)
    # 应用rectification映射
    new_img = cv2.remap(img, map2x_2, map2y_2, cv2.INTER_AREA)
    img_cut = new_img[after_crop[0]:after_crop[1], after_crop[2]:after_crop[3]]
    # 保存rectified图像
    cv2.imwrite(os.path.join(output_path, image_file[6:14]+'.bmp'), img_cut)
