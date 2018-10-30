import cv2
import os
import time

def detectPeople(filePath):
    img = cv2.imread(filePath)
    rows, cols = img.shape[:2]
    sacle = 1.0
    # print('img',img.shape)
    img = cv2.resize(img, dsize=(int(cols * sacle), int(rows * sacle)))
    # print('img',img.shape)

    # 创建HOG描述符对象
    # 计算一个检测窗口特征向量维度：(64/8 - 1)*(128/8 - 1)*4*9 = 3780
    #
    # winSize = (64,128)
    # blockSize = (16,16)
    # blockStride = (8,8)
    # cellSize = (16,8)
    # nbins = 9
    # hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins)

    hog = cv2.HOGDescriptor()
    # hist = hog.compute(img)
    # print(hist.shape)
    detector = cv2.HOGDescriptor_getDefaultPeopleDetector()
    print('detector', type(detector), detector.shape)
    hog.setSVMDetector(detector)

    # 多尺度检测，found是一个数组，每一个元素都是对应一个矩形，即检测到的目标

    found, w = hog.detectMultiScale(img)
    i=0
    for v in found:
        y, x, h, w = v
        pic = img[x:x+w,y:y+h]
        cv2.imwrite("_%d.jpg" %i, pic)
        i+=1
    print(found)


def detectPerson(filePath, hog, savePath, indicies, picSize):

    img = cv2.imread(filePath)
    rows, cols = img.shape[:2]
    sacle = 1.0
    img = cv2.resize(img, dsize=(int(cols * sacle), int(rows * sacle)))
    # hog = cv2.HOGDescriptor()
    # detector = cv2.HOGDescriptor_getDefaultPeopleDetector()
    # hog.setSVMDetector(detector)

    # 多尺度检测，found是一个数组，每一个元素都是对应一个矩形，即检测到的目标框
    found, w = hog.detectMultiScale(img)

    for v in found:
        y, x, h, w = v
        pic=img[x:x+w,y:y+h]
        #pic=cv2.resize(pic,picSize)
        cv2.imwrite(savePath+'%d.jpg'%indicies,pic)
        indicies+=1

    return indicies

def detect_and_save(filePath, savePath, saveSize):
    """
    detect person and save it
    :param filePath:
    :param savePath:
    :param saveSize:
    :return:
    """
    hog = cv2.HOGDescriptor()
    detector = cv2.HOGDescriptor_getDefaultPeopleDetector()
    hog.setSVMDetector(detector)

    dirs_name_list=os.listdir(filePath)
    for dir_name in dirs_name_list:
        if '.DS_Store' == dir_name:
            continue

        dir_path = filePath + dir_name + '/'
        dir_path_save = savePath + dir_name + '/'

        if not os.path.exists(dir_path_save):
            os.mkdir(dir_path_save)

        video_file_list=os.listdir(dir_path)
        for video_name in video_file_list:
            if '.DS_Store' == video_name:
                continue
            video_path=dir_path+video_name+'/'
            video_path_save=dir_path_save+video_name+'/'

            if not os.path.exists(video_path_save):
                os.mkdir(video_path_save)

            frame_list=os.listdir(video_path)
            picI=0
            for frame_name in frame_list:
                if '.DS_Store' == frame_name:
                    continue

                frame_path=video_path+frame_name

                picI=detectPerson(frame_path,hog,video_path_save,picI,saveSize)

            frame_list = os.listdir(video_path_save)
            if 0 == len(frame_list):
                os.rmdir(video_path_save)
        video_file_list = os.listdir(dir_path_save)
        if 0 == len(video_file_list):
            os.rmdir(dir_path_save)




if __name__ == '__main__':
    filePath='/Users/xuweijie/DownLoads/frames_centroid/'
    savePath='/Users/xuweijie/DownLoads/detect_frames_centroid/'

    start=time.time()
    detect_and_save(filePath,savePath,(20,20))
    print("Running time:")
    print(time.time()-start)