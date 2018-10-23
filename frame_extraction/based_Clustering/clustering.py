"""
    this file is based on clustering and to get the key frames
"""
import frame
import sys
import math
import cv2

def calSimilarity(source, target, frame_size, weight):
    """
    calculate the similarity of two histogram data
    :param source: the source data which is in the form of list
    :param target: the target data which is in the form of list
    :param frame_size: the size of one frame
    :param weight: the weight of values
    :return: the similarity
    """
    similarity=0.0
    if len(source) != len(target) or len(source) != len(weight):
        return similarity

    sizeData=len(source)
    for row in range(sizeData):
        w=0.0
        for (a, b) in zip(source[row],target[row]):
            w+=min(a,b)

        similarity+=weight[row]*w

    similarity=similarity / (frame_size[0] * frame_size[1])
    return similarity

def updateCentroid(origin, newOne, size):
    """
    update the value of centroid of histogram
    :param origin: the origin centroid
    :param newOne: the new centroid which need to be added
    :param size: the size of this cluster
    :return:
    """
    for i in range(len(origin)):
        length=len(origin[i])
        for j in range(length):
            origin[i][j]+=newOne[i][j]/size



def frameCluster(histogram, frame_size, threshold, weight, rate):
    """
    cluster the frames and get the key frames on the basis of similarity between frames
    :param histogram: the histogram of target video
    :param frame_size: the size of target frames
    :param threshold: the threshold value which used to calculate similarity
    :param weight: the weight of values of HSV which used to calculate similarity
    :param rate: the rate which define number of class should be merged
    :return: the index of final cluster
    """

    # cluster data, the value 'centroid' store the center of one class,
    # 'value' stores the index of frames belongs to this class
    cluster={}
    frame_index=0
    for hist in histogram:
        # if there is no class in the cluster, add a new one
        if 0==len(cluster):
            newClass={}
            newClass['centroid']=hist
            newClass['value']=[]
            newClass['value'].append(frame_index)

            cluster[frame_index]=newClass

        # compare the similarity between current histogram data and centroid
        else:
            findCluster=False
            for source in cluster:
                similarity=calSimilarity(cluster[source]['centroid'],hist,frame_size,weight)

                # if similarity is smaller threshold,we can think this histogram belong to this class
                # add the index of this histogram to the cluster and update centroid
                if similarity<threshold:
                    cluster[source]['value'].append(frame_index)
                    updateCentroid(cluster[source]['centroid'], hist, len(cluster[source]['value']))
                    findCluster=True
                    break

            # if this histogram has no similar class let it be a new class
            if not findCluster:
                newClass = {}
                newClass['centroid'] = hist
                newClass['value'] = []
                newClass['value'].append(frame_index)

                cluster[frame_index] = newClass

        frame_index += 1

    # # print the current cluster
    # for v in cluster:
    #     print(cluster[v]['value'])
    # print()

    # merge some class which size is smaller than rate*number_of_frames into the nearest class
    minMerge=rate*len(histogram)
    mergeCluser={}  # store illegal classes

    # delete the illegal classes from origin cluster and store them into mergeCluster
    i=0
    for v in list(cluster):
        if len(cluster[v]['value']) <= minMerge:
            mergeCluser[i]=cluster[v]
            cluster.pop(v)
            i += 1


    # merge
    if 0==len(cluster):
        cluster=mergeCluser
    else:
        for v in mergeCluser:
            minSimilarty=sys.maxsize
            mergeIndex=list(cluster.keys())[0]

            for source in cluster:
                similarity=calSimilarity(cluster[source]['centroid'],mergeCluser[v]['centroid'],frame_size,weight)
                if similarity < minSimilarty:
                    minSimilarty=similarity
                    mergeIndex=source

            cluster[mergeIndex]['value'].extend(mergeCluser[v]['value'])
            updateCentroid(cluster[mergeIndex]['centroid'],mergeCluser[v]['centroid'],len(cluster[mergeIndex]['value']))

    # # print the merged cluster
    # for v in cluster:
    #     print(cluster[v]['value'])

    histogramCluster=[]
    for v in cluster:
        histogramCluster.append(cluster[v]['value'])

    return histogramCluster

def keyFramesExtracte(histogram,cluster, frames, savePath=None, filePrefix=''):
    """
    extract key frames by calculating entropy of each cluster
    :param histogram: the histogram of frames
    :param cluster: the indices of cluster
    :param frames: all the frames of target video
    :param savePath: the path which save the key frames,
        if not pass the param it means don't need to save the pictures
    :param filePrefix: the prefix of saving file
    :return: the key frames in the form of list
    """

    # extract the key frames
    keyFrames=[]
    fileNameIndex=0
    for oneCluster in cluster:
        maxEntropy=-sys.maxsize
        targetIndex=[oneCluster][0]

        for index in oneCluster:
            hvalue=histogram[index][0]  # the histogram of h
            total=sum(hvalue)

            p=[-(x/total)*math.log(x/total) for x in hvalue if x != 0]
            entropy=sum(p)

            if entropy > maxEntropy:
                maxEntropy=entropy
                targetIndex=index

        keyFrames.append(frames[targetIndex])

        # save the frames
        if savePath != None:
            cv2.imwrite(savePath+filePrefix+"_%d.jpg" % fileNameIndex,frames[targetIndex])
            fileNameIndex+=1

    return keyFrames


if __name__ == '__main__':
    filePath = 'resources/21_drink_u_nm_np1_fr_goo_9.avi'
    savePath='/Users/xuweijie/'
    prefix='test2'
    threshold=0.0125
    weight=[0.5, 0.3, 0.2]

    frames, histogram, frame_size = frame.saveFrameOfVideos(filePath)
    histogramCluster = frameCluster(histogram,frame_size, threshold,weight,0.05)
    keyFrames = keyFramesExtracte(histogram, histogramCluster,frames)

