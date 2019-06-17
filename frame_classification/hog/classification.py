import os
import cv2
from sklearn.model_selection import train_test_split
from sklearn.neighbors.nearest_centroid import NearestCentroid
import numpy as np
import time
from sklearn.svm import SVC
from hog_descriptor import hog_descriptor

def loadTestAndTrainData(filePath, rate):
    """
    split the frames in path of filePath into testing and training data as the rate
    :param filePath: the file path
    :param rate:
    :return: training and testing data3.jpg
    """
    if '/' != filePath[-1]:
        filePath+='/'

    test_data=[]
    test_label=[]
    train_data=[]
    train_label=[]

    # loop the directory
    second_name_list=os.listdir(filePath)
    for dirName in second_name_list:
        label_name=dirName
        second_path=filePath+dirName+'/'

        # filter .DS_Store
        if not os.path.isdir(second_path):
            continue

        video_name_list=os.listdir(second_path)

        train_video_name,test_video_name=train_test_split(video_name_list,test_size=rate)

        # load train frames
        for video_name in train_video_name:
            video_path=second_path+video_name+'/'

            # filter .DS_Store
            if not os.path.isdir(video_path):
                continue

            frame_name_list=os.listdir(video_path)
            if 0 == len(frame_name_list):
                continue

            for frame_name in frame_name_list:
                if '.DS_Store' == frame_name:
                    continue
                frame_path=video_path+frame_name   #图片的全路径


                #修改
                # 1 。读取灰度图
                # 2。修改图片大小
                # 3。hog获得新土
                # 4。将其转化为向量
                img=cv2.imread(frame_path,cv2.IMREAD_GRAYSCALE)
                # img=cv2.resize(img,dsize=(20, 20));
                img = cv2.resize(img,(20, 20))
                hog = hog_descriptor(img, cell_size=8, bin_size=9)
                hog_vector = hog.extract()
                m,n = hog_vector.shape[0],hog_vector.shape[1]
                img=hog_vector.reshape((1,m * n))
                img=img[0]
                # 修改

                train_data.append(img)
                train_label.append(label_name)

        # load test frames
        for video_name in test_video_name:
            video_path = second_path + video_name + '/'

            # filter .DS_Store
            if not os.path.isdir(video_path):
                continue

            frame_name_list = os.listdir(video_path)
            if 0 == len(frame_name_list):
                continue

            video_test=[]
            for frame_name in frame_name_list:
                if '.DS_Store' == frame_name:
                    continue
                frame_path = video_path + frame_name

                # 修改
                img = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
                # crop img of 10%
                # row, column = img.shape[0], img.shape[1]
                # row = int(row / 10)
                # column = int(column / 10)
                # img = img[row:row * 2, column:column * 2]
                # img = img.reshape((1, row * column))
                # img = img[0]
                img=cv2.imread(frame_path,cv2.IMREAD_GRAYSCALE)
                img=cv2.resize(img,(20, 20))
                hog = hog_descriptor(img, cell_size=8, bin_size=9)
                hog_vector = hog.extract()
                m = hog_vector.shape[0]
                n = hog_vector.shape[1]
                img=hog_vector.reshape((1,m * n))
                img=img[0]
                # 修改
                video_test.append(img)

            test_data.append(video_test)
            test_label.append(label_name)

    return test_data, test_label, train_data, train_label

def KNN(test_data, test_label, train_data, train_label):
    """
    use KNN to train and predict data
    :param test_data:
    :param test_label:
    :param train_data:
    :param train_label:
    :return: Accuracy and unpredictable rate
    """
    knn=NearestCentroid()

    knn.fit(train_data,train_label)

    # test the precision
    indices=0
    precision=0
    unpre=0
    for video_list in test_data:
        # # predict all the frame in a video and decide its class based on majority
        videMatrix=np.mat(video_list)
        preResult = knn.predict(videMatrix)
        label_result={}

        for value in preResult:
            label_result[value]=label_result.get(value,0)+1

        # if every class has the same probality
        resultSet=set(label_result.values())
        if len(resultSet) == len(label_result) and len(label_result) != 1:
            unpre += 1
        else:
            sorted_result = sorted(label_result.items(), key=lambda items: items[1])

            if test_label[indices] == sorted_result[0][0]:
                precision += 1

        indices+=1

    return precision,unpre

def SVM(test_data, test_label, train_data, train_label):
    """
        use KNN to train and predict data
        :param test_data:
        :param test_label:
        :param train_data:
        :param train_label:
        :return: Accuracy and unpredictable rate
    """
    svm=SVC(gamma='auto')
    svm.fit(train_data,train_label)
    # test the precision
    indices = 0
    precision = 0
    unpre = 0
    for video_list in test_data:
        # # predict all the frame in a video and decide its class based on majority
        videMatrix = np.mat(video_list)
        preResult = svm.predict(videMatrix)
        label_result = {}

        for value in preResult:
            label_result[value] = label_result.get(value, 0) + 1

        # if every class has the same probality
        resultSet = set(label_result.values())
        if len(resultSet) == len(label_result) and len(label_result) != 1:
            unpre += 1
        else:
            sorted_result = sorted(label_result.items(), key=lambda items: items[1])

            if test_label[indices] == sorted_result[0][0]:
                precision += 1

        indices += 1

    return precision, unpre

if __name__ == '__main__':
    # filePath='/Users/wanghongjin/Desktop/222/'
    # filePath = '../../resources/person_detect/detect_frames/'
    filePath = '/Users/wanghongjin/Desktop/check/'
    test_data, test_label, train_data, train_label=loadTestAndTrainData(filePath,0.1)
    totalSize=len(test_label)
    start=time.time()

    # knn
    # print("KNN start!")
    # precision, unpre=KNN(test_data, test_label, train_data, train_label)

    #svm
    print("SVM start!")
    precision, unpre=SVM(test_data, test_label, train_data, train_label)


    print("Running time:%s"%str(time.time()-start))
    print("Precision:%f"%(precision/totalSize))
    print("Unprecision:%f"%(unpre/totalSize))


