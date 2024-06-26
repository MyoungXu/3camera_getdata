import os
import cv2
import numpy as np

def get_timestamp(file_name):
    timestamp = []
    with open(file_name, encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i == 0:
                start_t = int(line.strip().split()[0])/1000
                continue
            t = int(line.strip().split()[0])/1000 - start_t
            timestamp.append(str(int(t)) + '\n')
    return timestamp

def getForwardMap(K, D, R, P, W, H):
    tempmap = np.zeros((W, H))
    WHs_sep = np.where(tempmap == 0)
    points_raw = np.vstack((WHs_sep[0], WHs_sep[1])).astype(np.float64)
    points_new = np.squeeze(cv2.undistortPoints(points_raw, K, D, R=R, P=P))
    maps_f = np.reshape(points_new, (W, H, 2))
    return maps_f

def getRectifyTransform(height, width, config, alpha):
    left_K = config.cam_matrix_left
    right_K = config.cam_matrix_right
    left_distortion = config.distortion_l
    right_distortion = config.distortion_r
    R = config.R
    T = config.T
    R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(left_K, left_distortion, right_K, right_distortion, (width, height), R, T, alpha=alpha)
    map1x, map1y = cv2.initUndistortRectifyMap(left_K, left_distortion, R1, P1, (width, height), cv2.CV_32FC1)
    map2x, map2y = cv2.initUndistortRectifyMap(right_K, right_distortion, R2, P2, (width, height), cv2.CV_32FC1)
    maps1_f = getForwardMap(left_K, left_distortion, R1, P1, width, height)
    maps2_f = getForwardMap(right_K, right_distortion, R2, P2, width, height)
    return map1x, map1y, map2x, map2y, maps1_f, maps2_f

def getImgMapF(img, events, maps_f):
    img = img.copy()
    img_events = 255 * np.ones([img.shape[0], img.shape[1], 3], dtype=np.uint8)
    img_events_p = 255 * np.ones([img.shape[0], img.shape[1], 3], dtype=np.uint8)
    img_events_n = 255 * np.ones([img.shape[0], img.shape[1], 3], dtype=np.uint8)

    for event in events:
        x, y, p, t = event
        x = 1279 - x
        x_new = int(maps_f[x, y, 0])
        y_new = int(maps_f[x, y, 1])
        if 0 <= x_new < img.shape[1] and 0 <= y_new < img.shape[0]:
            if p:
                img[y_new, x_new] = (0, 0, 255)
                img_events[y_new, x_new] = (0, 0, 255)
                # cv2.circle(img_events, (x_new, y_new), 1, (0, 0, 255), -1)
                img_events_p[y_new, x_new] = (0, 0, 255)
            else:
                img[y_new, x_new] = (255, 0, 0)
                img_events[y_new, x_new] = (255, 0, 0)
                # cv2.circle(img_events, (x_new, y_new), 1, (255, 0, 0), -1)
                img_events_n[y_new, x_new] = (255, 0, 0)
    return img, img_events, img_events_p, img_events_n

def img_show(win_name, img, scale):
    cv2.imshow(win_name, cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale))))


