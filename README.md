# 3camera_getdata
对于低光双模三相机共光轴系统采集所得原始数据的标定方法以及加工方法。

## 环境要求
需要使用Prophesee的相关基础包，请自行在[官网](https://support.prophesee.ai/portal/en/home)下载。
 
## 数据处理全步骤
### 标定过程
STEP1：用[e2calib](https://github.com/uzh-rpg/e2calib)将事件信号进行重建
STEP2：用STEP2_rename.py将事件重建所得结果重命名，使得它们的结果和图像的结果一致  
STEP3：用STEP3_reverse-image.py将两个图像的文件结果进行翻转，得到正确的图像结果  
STEP4：利用STEP4_merge.py将三组图片合并在一起，并挑出合适的那几张图片  
STEP5：用STEP5_get-image.py得到用于标定的图片组  
STEP6：在matlab中对cam1和cam2进行一次标定，将结果放在stereo_config里面的cam1cam2中  
STEP7：用STEP7_get-co-image.py得到第一次校准后的两组帧图像，同时建议把误差较大的图像删掉（cam1文件夹中的图片删掉就行），因为后续大概只能处理40张图片  
STEP8：在matlab中对co_cam1和event进行一次标定，将结果放在stereo_config里面的cameve中  
  
### 数据集处理过程  
STEP9：用STEP9_test.py来确定裁剪参数以及是否需要调整参数  
STEP10：用STEP10_final-get.py来得到所有的数据  
  
可以用voxel2event得到对应的event-frame
