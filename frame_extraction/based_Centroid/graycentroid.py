"""
    this file is based on gray centroid and to get the key frames
"""
import frame_centroid
import os
import cv2
import shutil
import numpy as np
import time
import random
import math

def getsimilize(graycentvalue):
    flag = [0] * len(graycentvalue)
    for i in range(1, len(graycentvalue)):
        if flag[i - 1] == 0:
            if judgeprevious(graycentvalue[i], graycentvalue[i-1]) == True:
                flag[i] = 1
            else:
                flag[i] = 0
        elif flag[i - 1] == 1:
            totx = 0.0
            toty = 0.0
            j = i
            while True:
                totx += graycentvalue[j-1][0]
                toty += graycentvalue[j-1][1]
                if flag[j-1] == 0:
                    break
                j -= 1
            m = i - j + 1
            if judgeprevious(graycentvalue[i], graycentvalue[i-1]) == True and judgeaverage(totx / m, toty / m, graycentvalue[i]) == True:
                flag[i] = 1
            else:
                flag[i] = 0

    return flag

def judgeprevious(currentcv, preiouscv):

    judgewithprex = abs(currentcv[0] - preiouscv[0]) / currentcv[0]
    judgewithprey = abs(currentcv[1] - preiouscv[1]) / currentcv[1]

    if judgewithprex < 0.01 and judgewithprey < 0.01:
        return True
    else:
        return False

def judgeaverage(averagex, averagey, currentcv):

    judgewithprex = abs(currentcv[0] - averagex) / currentcv[0]
    judgewithprey = abs(currentcv[1] - averagey) / currentcv[1]

    if judgewithprex < 0.03 and judgewithprey < 0.03:
        return True
    else:
        return False

def segmentseq(flag, graycentvalue):
    cpdflag = []
    didflag = []
    result = []
    p = 0
    q = 0
    while p < len(flag) - 1:
        if flag[q] == 0:
            if flag[q + 1] == 1:
                mid = q + 1
                while True:
                    if mid >= len(flag) - 1:
                        q = len(flag) - 1
                        break
                    else:
                        if flag[mid + 1] == 1:
                            mid += 1
                        else:
                            q = mid
                            break
                didflag.append([p, q])
                p = q + 1
                q = p
            else:
                p += 1
                q = p

    # getkeyframe(didflag, graycentvalue, 2)
    return didflag

def getkeyframe(didflag, graycentvalue, thresholdvalue):
    thekeynumber = []
    if len(didflag):
        for item in didflag:
            if item[1] - item[0] + 1 >= thresholdvalue:
                item = calkeyframe(item[1], item[0] ,graycentvalue)
                thekeynumber.append(item)
        if len(thekeynumber):
            return thekeynumber
        else:
            calarray = np.array(didflag)
            resarray = calarray[:, 1] - calarray[:, 0]
            keyarray = resarray.tolist().index(max(resarray))
            thekeynumber.append(didflag[keyarray][0])
            return thekeynumber
    else:
        for i in range(thresholdvalue):
            thekeynumber.append(random.randint(0, len(graycentvalue)-1))
        return thekeynumber



def calkeyframe(bigdata, smalldata, graycentvalue):
    totx = 0.0
    toty = 0.0
    smdata = 10000.0
    for i in range(smalldata, bigdata + 1):
        totx += graycentvalue[i][0]
        toty += graycentvalue[i][1]

    number = bigdata - smalldata + 1
    avgx = totx / number
    avgy = toty / number

    midcal = np.array([avgx, avgy])
    for i in range(smalldata, bigdata + 1):
        mideddis = np.linalg.norm(midcal - graycentvalue[i])
        if(mideddis < smdata):
            smdata = mideddis
            key = i

    return key


if __name__ == '__main__':
    filePath = 'resources/21_drink_u_nm_np1_fr_goo_9.avi'

    frames, graycentvalue, frame_size, frame_count = frame_centroid.saveFrameOfVideos(filePath)
    print(frame_count)
    flag = getsimilize(graycentvalue)
    # didflag是第几帧到第几帧的索引号
    didflag = segmentseq(flag, graycentvalue)
    print(didflag)
    # 100为有效序列最小长度，key是第几帧的列表，frames是读出来的每一帧数据，初步设想是大小是帧数的10%的上界
    key = getkeyframe(didflag, graycentvalue, math.ceil(frame_count * 0.1))
    print(key)

