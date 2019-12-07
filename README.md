# 简易版手写多位数字的识别器

###  综述

这是一个简单的手写多位数字的识别器，不使用任何的机器学习框架（故称其为简单版），通过底层的KNN算法（未优化，粗暴版），进行数据训练后给出识别结果（简易粗暴的UI展示）。

### 核心细谈

**该识别器分为三大块实现：**

1. KNN算法的实现（KNN.py）
2. 图片的处理（HandWritten.py）
3. UI的设计(HandleImage.py)

这里每一步都含有数据的存储处理，是一个常见的操作，故不多讲。

图片的处理是我觉得难处理的问题（至今还存在一些瑕疵...）

```python
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

```

上面所写代码即为分割手写的图像，本来想使用opencv的边缘检测（但发现没必要），我没有对行处理，而是直接通过判断每一列的像素点的来按列的位置切割图片（将图片切割成一张张有助于识别，减少由于数字较多造成数据可能性指数增长的情况，多个数字的同时识别涉及较多的可能，故不建议），这里由于没处理到空白的行，也就是切割的时候没有将数字上下裁剪，这会存在白边的可能（考虑到但是如果在这里裁边的话，进行图片的压缩时还会存在问题，故没有进行更改）

**UI手写板的设计**

```python
    def paintEvent(self,event):
        '''
        用于将鼠标移动的点绘画出来
        :param event:
        :return:
        '''
        painter = QPainter()  ## 用于接下来的绘制线条
        painter.begin(self)
        pen = QPen(Qt.black,35,Qt.SolidLine) #用于绘制几何图形的边缘 颜色 大小 风格
        painter.setPen(pen)

        '''
        首先判断 保存的点中是否是至少是两个点？
        然后 ponit_start刚开始的是起始的点
        将相邻的点都连接起来
        '''

        if len(self.pos_xy) > 1:
            point_start = self.pos_xy[0]
            for pos_tmp in self.pos_xy:
                point_end = pos_tmp
                if point_end == (-1,-1):
                    point_start = (-1,-1)
                    continue
                if point_start == (-1,-1) :
                    point_start = point_end
                    continue
                #设置画的范围
                if point_start[1] > 340  or point_start[0] > 980 or point_start[0] < 0 or point_start[1] < 0 :
                    point_start = point_end
                    continue
                painter.drawLine(point_start[0],point_start[1],point_end[0],point_end[1])
                point_start = point_end
        painter.end()

    def mouseMoveEvent(self,event):
        '''
        按住鼠标移动的时候，将这些点加入到列表中
        '''
        pos_tmp = (event.pos().x(),event.pos().y())
        #将获取的坐标加入到列表中
        self.pos_xy.append(pos_tmp)
        #update 是调用paintEvent函数  将 鼠标移动的轨迹画出来
        self.update()
    def mouseReleaseEvent(self,event):
        """
        鼠标松开后，用一个断点(-1,-1) 表示到此断掉
        """
        pos_temp = (-1,-1)
        self.pos_xy.append(pos_temp)
        self.update()

```

上面手写板比较有意思，就是捕捉鼠标的坐标，就是当鼠标被按压进行移动的时候，就把移动经过的坐标加入到列表中，这样就能保存到轨迹了，鼠标松开的地方加入断点，这样就可以保证画出独立的数字（paintEvent两个两个点的绘线）

**程序的运行效果**

1. 

![](https://github.com/1291945816/ML_Assessment/blob/master/Image/%E6%88%90%E5%8A%9F%E6%A0%B7%E4%BE%8B.png)

2. 

![](https://github.com/1291945816/ML_Assessment/blob/master/Image/%E6%88%90%E5%8A%9F%E6%A0%B7%E4%BE%8B%20(2).png)

3. 

![]()

**以上程序比较简单，不具备实际的生活应用的作用，但对于学习机器学习的基础算法有较大的帮助，同时也有助于对验证码识别的一个自我优化实现。**

