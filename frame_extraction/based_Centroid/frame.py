"""
    this file is to split videos into frames and
    get the histogram of every frames by counting attributes of frames' HSV picture
"""

import os
import cv2
import shutil
import numpy as np
import time
import random

def saveFrameOfVideos(filePath):
    """
    get every frames of one video and save them
    :param filePath:the path of target video
    :return:1. the path of frames in color space of RGB
            2. the path of frames in color space of HSV
            3. a list which store all the histogram of every frame
            4. the size of frame
    """

    # # get the name of video
    # video_full_name = os.path.splitext(filePath)
    # video_name = video_full_name[0].split('/')[-1]
    # video_type = video_full_name[-1]  # contains '.'
    #
    # # make dir to store frames
    # frame_path = 'resources/' + video_name + '/'  # the path that save all frames
    # frame_path_rgb = frame_path + 'rgb/'  # the path that save frames in the color space of rgb
    # frame_path_hsv = frame_path + 'hsv/'  # the path that save frames in the color space of hsv
    #
    # if os.path.exists(frame_path):
    #     shutil.rmtree(frame_path)
    #
    # os.makedirs(frame_path)
    # os.makedirs(frame_path_rgb)
    # os.makedirs(frame_path_hsv)

    frames = []  #store all the frames
    cap = cv2.VideoCapture(filePath)
    success = True
    frame_count = 0

    frame_size = [] # store the size of frames and consider that all the frames of one video have the same size
    graycentvalue = []  # store the hist value of all frames
    start = time.time()
    while success:
        success, frame = cap.read()


        if success:
            frames.append(frame)
            # store the size of frame
            if 0 == frame_count:
                frame_size = frame.shape

            # convert to color space of HSV
            # start1=time.time()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # print("gray:")
            # print(time.time()-start1)
            # cv2.imwrite(frame_path_hsv + "%d.jpg" % frame_count, hsv)

            # cv2.imwrite(frame_path_rgb + "%d.jpg" % frame_count, frame)
            frame_count = frame_count + 1

            # store the value of histogram
            # start2=time.time()
            graycentroid = getgraycentroid(gray, gray.shape)
            # print('centroid:')
            # print(time.time()-start2)
            graycentvalue.append(graycentroid)

    # print("你妈死了")
    # print(frame_count)
    cap.release()
    # end = time.time()
    # print(start - end)
    # print(graycentvalue)
    #getsimilize(graycentvalue)
    return frames, graycentvalue, frame_size, frame_count

def getgraycentroid(frame, shape):
    quax = 0.0
    quay = 0.0
    midquay = 0.0
    qua = 0.0
    graycentroid = []

    # for i in range(shape[0]):
    #     for j in range(shape[1]):
    #         quax += frame[i][j] * j
    #         qua  += frame[i][j]
    #
    # for j in range(shape[1]):
    #     for i in range(shape[0]):
    #         quay += frame[i][j] * i
    #
    # graycentroid.append(quax / qua)
    # graycentroid.append(quay / qua)

    frame_mat = np.mat(frame)
    row_total = frame_mat.sum(axis=0)
    column_total = frame_mat.sum(axis=1)

    dotmatrix = np.mat(np.linspace(1, row_total.shape[1], row_total.shape[1]))
    valuematrix = np.multiply(dotmatrix, row_total)
    valuelist = valuematrix.tolist()
    quax = sum(valuelist[0])

    for i in range(len(column_total)):
        midquay += column_total[i] * (i+1)

    quay = midquay.sum(axis=1).tolist()

    qua = frame_mat.sum()

    graycentroid.append(quax / qua)
    graycentroid.append(quay[0][0] / qua)

    # print(graycentroid)
    return graycentroid

