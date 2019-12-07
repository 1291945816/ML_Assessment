import numpy as np
import cv2


def image_to_bin(img):
    '''

    :param img: 一幅已被处理好的图片
    :return:
    '''
    tempimage = []
    h,w,_=img.shape
    for x in range(h):
        tempimage_temp = []
        for y in range(w):
            if int(img[x][y][0])+int(img[x][y][1])+int(img[x][y][2]) == 0:
                tempimage.append(int(1))
            else:
                tempimage.append(int(0))
    return  tempimage


def image_handle(filename):
    img = cv2.imread(filename)
    img = cv2.resize(img,(128,64),interpolation=cv2.INTER_CUBIC)
    pic = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #将图片灰度化




    #将每一个元素进行二值化 保持只有黑白统一的像素值
    for index_x,i in enumerate(img):
        for index_y,j in enumerate(i):
            if (j>200).all():
                img[index_x][index_y] = 240 # 白色
            else:
                img[index_x][index_y] = 0 # 黑色
    #根据列的白像素大小来判断
    (h,w,_)=img.shape
    w -= 1
    col_nz = [0] * w;
    for x in range(w):
        for y in range(h):
            if img[y,x][0] == 240:
                col_nz[x] += 1

    #获取每一个数字的范围
    count_scope = []
    temp = 0
    tempValue=-1
    for i in range(len(col_nz)):
        if col_nz[i] <= 60 and temp==0:
            tempValue = i
            temp = 1
        elif temp == 1 and col_nz[i] > 60:
            count_scope.append((tempValue,i))
            temp = 0
    image_list = []
    if(len(count_scope)>=1):
        for x in count_scope:
            tempImage = img[:,x[0]:x[1]]
            tempImage = cv2.resize(tempImage, (32, 32), interpolation=cv2.INTER_CUBIC)
            tempImage = image_to_bin(tempImage)
            image_list.append(tempImage)
        return image_list
    else:
        return None





