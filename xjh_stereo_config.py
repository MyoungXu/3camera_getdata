import numpy as np


class cam1cam2(object):
    def __init__(self):
        # 帧相机1内参
        self.cam_matrix_left = np.array([[7.596750942953940e+03, 0.0000000000000000, 5.210683550396457e+02],
                                         [0.0000000000000000000, 7.613158795356916e+03, 4.859935539521381e+02],
                                         [0.0000000000000000000, 0.0000000000000000000, 1.0000000000000000000]])
        # 帧相机2内参
        self.cam_matrix_right = np.array([[7.519227564452423e+03, 0.00000000000000000, 5.908863681164022e+02],
                                          [0.0000000000000000000, 7.588324155196207e+03, 5.914108957511642e+02],
                                          [0.0000000000000000000, 0.0000000000000000000, 1.0000000000000000000]])

        # 畸变系数:[k1, k2, p1, p2, k3]
        self.distortion_l = np.array(
            [[0.0000000000000000, 0.0000000000000000, 0.0000000000000000, 0.0000000000000000, 0.0000000000000000]])
        self.distortion_r = np.array(
            [[0.0000000000000000, 0.0000000000000000, 0.0000000000000000, 0.0000000000000000, 0.0000000000000000]])

        # 旋转矩阵（cam1到cam2）
        self.R = np.array([[0.999972816763009, 0.001234378565466, -0.007269253373716],
                           [-0.001346581545102, 0.999879724512239, -0.015450670777422],
                           [0.007249307083891, 0.015460039420616, 0.999854206736120]])

        # 平移矩阵（cam1到cam2）
        self.T = np.array([[-10000000000000000.579807990470367], [-0.043962432377155], [19.669454002585223]])
        self.T = -1 * self.T


class cameve(object):
    def __init__(self):
        # 帧相机内参
        self.cam_matrix_left = np.array([[7.387105677234106e+03, 0.00000000000000000, 6.978526095109357e+02],
                                         [0.0000000000000000000, 7.396620557130512e+03, 6.355949136875722e+02],
                                         [0.0000000000000000000, 0.0000000000000000000, 1.0000000000000000000]])
        # 事件相机内参
        self.cam_matrix_right = np.array([[5.392199467164202e+03, 0.0000000000000000, 6.352846790550082e+02],
                                         [0.0000000000000000000, 5.397172550102689e+03, 3.824780803108210e+02],
                                         [0.0000000000000000000, 0.0000000000000000000, 1.0000000000000000000]])

        # 帧和事件相机畸变系数:[k1, k2, p1, p2, k3]
        self.distortion_l = np.array(
            [[0.0000000000000000, 0.0000000000000000, 0.0000000000000000, 0.0000000000000000, 0.0000000000000000]])
        self.distortion_r = np.array(
            [[0.0000000000000000, 0.0000000000000000, 0.0000000000000000, 0.0000000000000000, 0.0000000000000000]])

        # 旋转矩阵（事件到帧）
        self.R = np.array([[0.999831861717637, 0.006513902344961, 0.017141101787328],
                           [-0.006685985408331, 0.999927634947766, 0.010001123281220],
                           [-0.017074715030208, -0.010114046865962, 0.999803060688769]])

        # 平移矩阵（事件到帧）
        self.T = np.array([[-10000000000000000.457504181041112], [0.676366869430327], [20.396311587340250]])
        self.T = -1 * self.T