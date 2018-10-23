"""
    this script aims to extract key frames of testing data
"""

import os
import clustering
import frame
import time
import matplotlib.pyplot as plt
import shutil

def extractRecursive(path, savePath,threshold, weight):
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

            # extract the key frames and save them
            frames, histogram, frame_size = frame.saveFrameOfVideos(video_full_path)
            histogramCluster = clustering.frameCluster(histogram, frame_size, threshold, weight, 0.05)

            # todo: do not need to save them when testing for making sure thrshold
            # keyFrames = clustering.keyFramesExtracte(histogram, histogramCluster, frames)
            keyFrames = clustering.keyFramesExtracte(histogram, histogramCluster, frames,
                                                     video_full_path_save, video_name)

            # # todo draw plt
            # # record the number of key frames
            # count_frames=len(keyFrames)/len(frames)
            # num_frames[count_frames]=num_frames.get(count_frames,0)+1

    return num_frames


if __name__ == '__main__':
    path='/Users/xuweijie/Downloads/data2/'
    savePath='/Users/xuweijie/Downloads/frames/'
    threshold = 0.0125
    weight = [0.5, 0.3, 0.2]

    start = time.time()
    print("Start!Time is:%s"%(str(start)))
    num_frames = extractRecursive(path, savePath, threshold,weight)
    end=time.time()
    print("End!Time is:%s" % (str(end)))
    # print running time
    print("Running time is %s"%(end-start))

    # # show the number of key frame
    # sorted_frames=sorted(num_frames.keys())
    #
    # x=[]
    # y=[]
    # for v in sorted_frames:
    #     x.append(v)
    #     y.append(num_frames[v])
    #
    # total=sum(y)
    # y=[x/total for x in y]
    # plt.title("threshold:%s" % threshold)
    # plt.plot(x,y)
    # pic_name='/Users/xuweijie/Downloads/data/test_pic/'+str(threshold)+'.png'
    # plt.savefig(pic_name)
    # plt.show()