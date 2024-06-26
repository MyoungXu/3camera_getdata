import xjh_stereo_config
from Utils import *
from tqdm import tqdm
from metavision_core.event_io.raw_reader import RawReader


after_crop = [100, 800, 240, 1165]   # HW（小系统）
# after_crop = [0, 1080, 0, 1440]   # HW（小系统）
load_scale = [0.1, 0.5]  # 读取多少比例的图片

base_path = r'F:\000002'
events_deltat = 10000  # us
exp_time = 20000  # us

imgs_path = os.path.join(base_path, 'cam1')
imgs_path_ = os.path.join(base_path, 'cam2')
record_raw = RawReader(os.path.join(base_path, 'event.raw'))
timestamp_list = get_timestamp(os.path.join(imgs_path, 'timestamp.txt'))
global_imshow_scale = 1.0
height = 1080
width = 1440
# 事件大小为1280,720


height_result = after_crop[1] - after_crop[0]
width_result = after_crop[3] - after_crop[2]

config1 = xjh_stereo_config.cam1cam2()
config2 = xjh_stereo_config.cameve()
map1x, map1y, map2x, map2y, maps1_f, maps2_f = getRectifyTransform(height, width, config1, alpha=1.0)
map2x_2, map2y_2, map1x_2, map1y_2, maps2_f_2, maps1_f_2 = getRectifyTransform(height, width, config2, alpha=1.0)


def overlap(img, events, maps_f):
    img = img.copy()
    img_events = 255 * np.ones([img.shape[0], img.shape[1], 3], dtype=np.uint8)

    for event in events:
        x, y, p, t = event
        x_new = int(maps_f[x, y, 0])
        y_new = int(maps_f[x, y, 1])
        if 0 <= x_new < img.shape[1] and 0 <= y_new < img.shape[0]:
            if p:
                img[y_new, x_new] = (0, 0, 255)
                img_events[y_new, x_new] = (0, 0, 255)

            else:
                img[y_new, x_new] = (255, 0, 0)
                img_events[y_new, x_new] = (255, 0, 0)

    return img, img_events


def main():
    imgs_name = os.listdir(imgs_path)
    imgs_name_len = len(imgs_name)

    for img_name in tqdm(imgs_name[int(imgs_name_len * load_scale[0]):int(imgs_name_len * load_scale[1])]):
        idx = int(img_name[6:14]) - 2
        if idx < 0:
            continue

        # 从曝光中间时刻提取前后各一半事件
        target_timestamp = int(timestamp_list[idx].strip('\n')) - int(exp_time / 2) - int(events_deltat / 2)
        record_raw.seek_time(target_timestamp)
        events = record_raw.load_delta_t(events_deltat)

        # 读取图像
        img = cv2.imread(os.path.join(imgs_path, img_name))
        img_flipped = cv2.flip(img, 1)  # 左右翻转
        # 应用rectification映射
        new_img = cv2.remap(img_flipped, map1x, map1y, cv2.INTER_AREA)
        newnew_img = cv2.remap(new_img, map2x_2, map2y_2, cv2.INTER_AREA)

        img_mapF_verify, img_events = overlap(newnew_img, events, maps1_f_2)
        img_cut = img_mapF_verify[after_crop[0]:after_crop[1], after_crop[2]:after_crop[3]]

        img_show('cam1', img_cut, global_imshow_scale)


        # 读取图像
        img = cv2.imread(os.path.join(imgs_path_, img_name))
        img_flipped = cv2.flip(img, 1)  # 左右翻转
        # 应用rectification映射
        new_img = cv2.remap(img_flipped, map2x, map2y, cv2.INTER_AREA)
        newnew_img = cv2.remap(new_img, map2x_2, map2y_2, cv2.INTER_AREA)

        img_mapF_verify, img_events = overlap(newnew_img, events, maps1_f_2)
        img_cut = img_mapF_verify[after_crop[0]:after_crop[1], after_crop[2]:after_crop[3]]


        img_show('cam2', img_cut, global_imshow_scale)

        if cv2.waitKey(1) == 27:
            exit(0)

if __name__ == '__main__':
    main()