import xjh_stereo_config
from Utils import *
from tqdm import tqdm
from metavision_core.event_io.raw_reader import RawReader
from voxel import events_to_voxel

after_crop = [100, 800, 240, 1165]  # HW（小系统）

base_path = r'F:\000002'
output_folder_name = 'xjh'

events_deltat = 10000  # us
exp_time = 20000  # us
VOXEL_FLAG = False

imgs_path = os.path.join(base_path, 'cam1')
imgs_path_ = os.path.join(base_path, 'cam2')
record_raw = RawReader(os.path.join(base_path, 'event.raw'))
timestamp_list = get_timestamp(os.path.join(imgs_path, 'timestamp.txt'))
global_imshow_scale = 1.0
height = 1080
width = 1440

height_result = after_crop[1] - after_crop[0]
width_result = after_crop[3] - after_crop[2]

config1 = xjh_stereo_config.cam1cam2()
config2 = xjh_stereo_config.cameve()
map1x, map1y, map2x, map2y, maps1_f, maps2_f = getRectifyTransform(height, width, config1, alpha=1.0)
map2x_2, map2y_2, map1x_2, map1y_2, maps2_f_2, maps1_f_2 = getRectifyTransform(height, width, config2, alpha=1.0)


# 事件大小为1280,720


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
    base_folder = os.path.join('output', output_folder_name)
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        os.makedirs(os.path.join(base_folder, 'low_light'))
        os.makedirs(os.path.join(base_folder, 'gt'))
        os.makedirs(os.path.join(base_folder, 'event'))
        if VOXEL_FLAG:
            os.makedirs(os.path.join(base_folder, 'voxel'))

    imgs_name = os.listdir(imgs_path)

    for img_name in tqdm(imgs_name):
        if img_name.endswith(".txt"):
            continue

        idx = int(img_name[6:14]) - 2
        if idx < 0:
            continue

        # 读取低光图像
        img = cv2.imread(os.path.join(imgs_path, img_name))
        img_flipped = cv2.flip(img, 1)  # 左右翻转
        # 应用rectification映射
        new_img = cv2.remap(img_flipped, map1x, map1y, cv2.INTER_AREA)
        newnew_img = cv2.remap(new_img, map2x_2, map2y_2, cv2.INTER_AREA)
        img_cut = newnew_img[after_crop[0]:after_crop[1], after_crop[2]:after_crop[3]]
        cv2.imwrite(os.path.join(base_folder, 'low_light', img_name[6:14] + '.bmp'), img_cut)

        # 读取gt
        img = cv2.imread(os.path.join(imgs_path_, img_name))
        img_flipped = cv2.flip(img, 1)  # 左右翻转
        # 应用rectification映射
        new_img = cv2.remap(img_flipped, map2x, map2y, cv2.INTER_AREA)
        newnew_img = cv2.remap(new_img, map2x_2, map2y_2, cv2.INTER_AREA)
        img_cut = newnew_img[after_crop[0]:after_crop[1], after_crop[2]:after_crop[3]]
        cv2.imwrite(os.path.join(base_folder, 'gt', img_name[6:14] + '.bmp'), img_cut)

        # 读取事件
        # 从曝光中间时刻提取前后各一半事件
        target_timestamp = int(timestamp_list[idx].strip('\n')) - int(exp_time / 2) - int(events_deltat / 2)
        record_raw.seek_time(target_timestamp)
        events = record_raw.load_delta_t(events_deltat)

        event_x = []
        event_y = []
        event_p = []
        event_t = []

        for event in events:
            x, y, p, t = event
            x_new = int(maps1_f_2[x, y, 0])
            y_new = int(maps1_f_2[x, y, 1])
            if after_crop[2] <= x_new < after_crop[3] and after_crop[0] <= y_new < after_crop[1]:
                x_new = x_new - after_crop[2]
                y_new = y_new - after_crop[0]
                event_x.append(x_new)
                event_y.append(y_new)
                event_p.append(2 * p - 1)  # 0变-1
                event_t.append(t)
            else:
                continue

        txt_file = os.path.join(os.path.join(base_folder, 'event'), img_name[6:14] + '.txt')
        # 打开文件，以追加模式写入
        with open(txt_file, 'a') as f:
            # 遍历事件列表
            for i in range(len(event_x)):
                # 获取当前事件的 x, y, p, t
                x = event_x[i]
                y = event_y[i]
                p = event_p[i]
                t = event_t[i]

                # 写入到文件，以空格分隔
                f.write(f"{x} {y} {p} {t}\n")

        if VOXEL_FLAG:
            # 计算体素
            event_x = np.array(event_x)
            event_y = np.array(event_y)
            event_p = np.array(event_p)
            event_t = np.array(event_t)
            voxel = events_to_voxel(event_x, event_y, event_t, event_p, 5,
                                    (after_crop[1] - after_crop[0], after_crop[3] - after_crop[2]))
            np_path = os.path.join(os.path.join(base_folder, 'voxel'), img_name[6:14] + '.npy')
            np.save(np_path, voxel)


if __name__ == '__main__':
    main()
