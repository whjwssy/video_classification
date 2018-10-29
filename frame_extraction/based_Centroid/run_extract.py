import frame_centroid
import graycentroid
import math
import cv2
import os
import shutil
import time

def extractFrame(filePath, savePath):
    """
    save the key frames to the path of sav epath
    :param filePath:
    :param savePath:
    :return:
    """
    frames, graycentvalue, frame_size, frame_count = frame_centroid.saveFrameOfVideos(filePath)
    flag = graycentroid.getsimilize(graycentvalue)
    # didflag是第几帧到第几帧的索引号
    didflag = graycentroid.segmentseq(flag, graycentvalue)
    # 100为有效序列最小长度，key是第几帧的列表，frames是读出来的每一帧数据，初步设想是大小是帧数的10%的上界
    key = graycentroid.getkeyframe(didflag, graycentvalue, math.ceil(frame_count * 0.1))


    i=0
    for indices in key:
        # print(frames[indices])
        # img=cv2.cvtColor(frames[indices],cv2.COLOR_GRAY2RGB)
        cv2.imwrite(savePath+"%s.jpg"%str(i),frames[indices])
        i+=1

def extractRecursive(path, savePath):
    """
    extract the key frames and save them, all key frames of one type saved in a same directory
    :param path: the current visiting path
    :param savePath: the path that save
    :param threshold: the threshold to judge similarity when clustering
    :param weight: weight which assign to HSV
    :return:
    """

    num_frames={}
    # get all the directory in path,filter .de_store
    dirs=os.listdir(path)
    dirs=[x for x in dirs if os.path.isdir(path+x)]

    # loop all directory in path
    for second_directory_name in dirs:
        second_directory_path=path+second_directory_name+'/'
        second_directory_save=savePath+second_directory_name+'/'

        # todo: do not need to save them when testing for making sure thrshold
        # make dir for save
        if not os.path.exists(second_directory_save):
            os.mkdir(second_directory_save)
        else:
            shutil.rmtree(second_directory_save)

        # get all the video_name of second directory
        video_names=os.listdir(second_directory_path)
        video_name_list=[x for x in video_names if len(x.split('.'))>1]

        # # todo: extract 10% files for testing
        # extract_num=int(len(video_name_list)*0.1)
        # video_name_list=video_name_list[:extract_num]

        # get all the videos in this directory
        for video_full_name in video_name_list:

            video_name=video_full_name.split('.')[:-1]
            video_name='.'.join(video_name)
            video_type=video_full_name.split('.')[-1]
            video_full_path=second_directory_path+video_full_name

            # make dir for key frames of video
            video_full_path_save=second_directory_save+video_name+'/'
            if not os.path.exists(video_full_path_save):
                os.mkdir(video_full_path_save)

            # save the key frames
            extractFrame(video_full_path,video_full_path_save)


    return num_frames

if __name__ == '__main__':
    start=time.time()
    filePath='/Users/xuweijie/Downloads/data/UCF-101/'
    savePath='/Users/xuweijie/Downloads/frames_centroid/'
    extractRecursive(filePath,savePath)

    print("Running time:")
    print(time.time()-start)