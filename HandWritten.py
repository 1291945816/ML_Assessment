from  PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel,QDesktopWidget,QLineEdit,QMessageBox)
from PyQt5.QtGui import (QPainter, QPen, QFont,QIcon)
from PyQt5.QtCore import Qt
from PIL import ImageGrab
import sys
from work.HandleImage import image_handle
from work.KNN import predict_digital
import numpy as np
import os
class HandWrittenWindow(QWidget):
    def __init__(self):
        super(HandWrittenWindow,self).__init__()
        self.resize(1000,400) ##设置窗体的高度
        self.setMouseTracking(False) #轨迹跟踪 不需要一直跟踪 也就是只有当鼠标被按键的时候才能跟踪轨迹
        self.setWindowTitle("HandWrittenWindow")
        self.center()
        self.pos_xy=[]
        self._filname ="D:\Python_Code\ML_ check\work\handwrittenImage\\data.png"
        self.image_list = None


        ##窗口的基本控件的添加
        #标好画板的边框位置
        self.label_draw = QLabel('',self)
        self.label_draw.setGeometry(2,2,996,350)
        #显示黑色边框
        self.label_draw.setStyleSheet("QLabel{border:1px solid black;}")
        self.label_draw.setAlignment(Qt.AlignCenter)

        self.label_showResult = QLabel("识别结果:",self)
        self.label_showResult.setGeometry(2,350,100,50)
        self.label_showResult.setAlignment(Qt.AlignCenter)
        ##结果显示边框
        self.label_result = QLabel('',self)
        self.label_result.setGeometry(104,350,100,50)
        self.label_result.setStyleSheet("QLabel{border:1px solid black; color: red ;}") #该脚本设置字体颜色 边界的颜色
        self.label_draw.setAlignment(Qt.AlignCenter)
        self.label_result.setFont(QFont("Timers", 15, QFont.Bold))

        self.button_recognize = QPushButton("识别",self)
        self.button_recognize.setGeometry(206,350,100,50)
        self.button_recognize.clicked.connect(self.button_recognize_on_clicked)

        self.button_reset = QPushButton("重置", self)
        self.button_reset.setGeometry(308, 350, 100, 50)
        #为按钮添加监听事件
        self.button_reset.clicked.connect(self.button_reset_on_clicked)

        self.button_stored = QPushButton("保存", self)
        self.button_stored.setGeometry(410, 350, 100, 50)
        self.button_stored.clicked.connect(self.button_store_on_clicked)
        self.setWindowIcon(QIcon("D:\\Python_Code\\ML_ check\\work\\data\\Icon\\pandas.ico"))


        self.button_close = QPushButton("关闭窗口", self)
        self.button_close.setGeometry(512, 350, 100, 50)
        # 为按钮添加监听事件
        self.button_close.clicked.connect(self.button_close_on_clicked)


        self.label_number = QLabel(" 数字:", self)
        self.label_number.setGeometry(610, 350, 70, 50)


        self.number_line_text = QLineEdit("",self)
        self.number_line_text.setGeometry(670,350,100,50)
        self.number_line_text.setFont(QFont("Timers",28,QFont.Bold))

        self.label_number1 = QLabel(" 序号:", self)
        self.label_number1.setGeometry(770, 350, 70, 50)

        self.number_line_text1 = QLineEdit("",self)
        self.number_line_text1.setGeometry(840, 350, 160, 50)
        self.number_line_text1.setFont(QFont("Timers", 28, QFont.Bold))

    ##用于设置屏幕位于桌面的中间
    def center(self):
        #获取屏幕的分辨率
        screen = QDesktopWidget().screenGeometry()
        #获取对象的分辨率
        size = self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2) #设置窗口的位置

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

    def button_reset_on_clicked(self):
        '''
        用于将数据清空
        :return:
        '''
        self.pos_xy = []
        self.label_result.setText("")
        self.number_line_text1.setText("")
        self.number_line_text.setText("")
        self.image_list = None
        self.update()
    def button_close_on_clicked(self):
        self.close()
    def button_store_on_clicked(self):
        '''
        这个用于手动存储手写数字图片
        :return:
        '''
        if self.image_list !=None and self.number_line_text.text() != "" and self.number_line_text1.text() != "":
            filedir = "D:\\Python_Code\\ML_ check\\work\\data\\trainingDigits\\" #存储的目录
            name = "{}_{}.txt".format(self.number_line_text.text(),self.number_line_text1.text())
            filename = os.path.join(filedir,name)
            with open(filename,"w") as fw:
                for index_x in range(1024):
                        if index_x != 0 and index_x %32 == 0:
                            fw.write("\n")
                        if self.image_list[0][index_x]==0:
                            fw.write("0")
                        else:
                            fw.write("1")
            QMessageBox.information(self, "消息", "数字 {}\n存储成功\n路径为: {}".format(self.number_line_text.text(),filename), QMessageBox.Ok)
        else:
            QMessageBox.warning(self,"警告","格式错误!!!\n确认一下你是否正确识别、输入数字、输入序号？",QMessageBox.Ok)




    def button_recognize_on_clicked(self):

        #指定区域进行截图
        bbox = (1565,934,2550,1281)
        im = ImageGrab.grab(bbox)
        im.save(self._filname)
        image_list =image_handle(self._filname)
        self.image_list = image_list
        digital = ""
        if image_list != None:
            data = predict_digital(np.array(image_list))
            for i in data:
                digital += str(i)
            self.label_result.setText(digital)


if __name__=='__main__':
    app =QtWidgets.QApplication(sys.argv)
    test = HandWrittenWindow()
    test.show()
    sys.exit(app.exec())