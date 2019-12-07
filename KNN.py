from  numpy import  *
import pandas as pd
import time
import os
import sys


#KNN核心算法
def classfydigits(newDataset,dataset,lable,k):
    rows = dataset.shape[0]  #获取行数
    #将待识别数据重复与数据集等行，便于相减
    datasetSub = tile(newDataset, (rows, 1))-dataset
    datasetSub = datasetSub ** 2
    datasetSub = datasetSub.sum(axis=1)
    distanceSet = datasetSub ** 0.5

    #排序距离 找出k个最小的
    indexSortedSet = distanceSet.argsort()
    countTimes={}
    for i in range(k):
        index = lable[indexSortedSet[i]]
        #找得到就+1 找不到就set为0后+1
        countTimes[index] = countTimes.get(index,0)+1

    #按值（字典无序转换为 列表 含有元组）排序
    countTimes =sorted(countTimes.items(), key=lambda x:x[1], reverse=True)
    #取最多个数的类别
    return countTimes[0][0]


#32*32 图片的一个二进制读取
def fileRead(filename):
    dataSet = []
    with open(filename) as fr:
        for i in range(32):
            line = fr.readline()
            for j in range(32):
                dataSet.append(int(line[j]))
    return dataSet


def create_DataSetByFile(filedir):
    filelist = os.listdir(filedir)
    lables = []
    dataSet = []
    for filePath in filelist:
        lable = int(filePath.split("_")[0])
        lables.append(lable)
        dataSet.append(fileRead(os.path.join(filedir,filePath)))
    #创造数据集 并且将顺序进行随机打乱
    dataSet = array(dataSet)
    lables = array(lables)
    dataRows = dataSet.shape[0]
    index = arange(dataRows)
    random.shuffle(index)
    dataSet = dataSet[index]
    lables = lables[index]
    return lables,dataSet


def predict_digital(predictSet):
    lables,dataSet = create_DataSetByFile("D:\\Python_Code\\ML_ check\\work\\data\\trainingDigits")
    str = ''
    data = []
    # print(predictSet[0].shape)
    for i in range(len(predictSet)):
        value = classfydigits(predictSet[i],dataSet,lables,5)
        data.append(int(value))
    return data













##test
# if __name__=='__main__':
#     lables,dateSet = create_DataSetByFile("D:\\Python_Code\\ML_ check\\work\\data\\trainingDigits")
#     testlables, testDataSet = create_DataSetByFile("D:\\Python_Code\\ML_ check\\work\\data\\testDigits")
#     countErrorTimes = 0
#     start = time.localtime(time.time()).tm_sec
#     index = arange(testDataSet.shape[0])
#     for i in index:
#         value = classfydigits(testDataSet[i],dateSet,lables,4)
#         # print("值为:{},识别为:{}".format(testlables[i],value))
#         if(value != testlables[i]):
#             countErrorTimes += 1
#
#     end = time.localtime(time.time()).tm_sec
#     d = int(end)-int(start)
#     error = (countErrorTimes*1.0)/len(testDataSet);
#     print("消耗时间为:{},错误率:{}".format(d,error))
#
#


















