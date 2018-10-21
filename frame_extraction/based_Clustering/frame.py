"""
    this file is to split videos into frames and
    get the histogram of every frames by counting attributes of frames' HSV picture
"""

import os
import cv2
import shutil


def saveFrameOfVideos(filePath):
    """
    get every frames of one video and save them
    :param filePath:the path of target video
    :return:1. the path of frames in color space of RGB
            2. the path of frames in color space of HSV
            3. a list which store all the histogram of every frame
    """

    # get the name of video
    video_full_name = os.path.splitext(filePath)
    video_name = video_full_name[0].split('/')[-1]
    video_type = video_full_name[-1]  # contains '.'

    # make dir to store frames
    frame_path = 'resources/' + video_name + '/'  # the path that save all frames
    frame_path_rgb = frame_path + 'rgb/'  # the path that save frames in the color space of rgb
    frame_path_hsv = frame_path + 'hsv/'  # the path that save frames in the color space of hsv

    if os.path.exists(frame_path):
        shutil.rmtree(frame_path)

    os.makedirs(frame_path)
    os.makedirs(frame_path_rgb)
    os.makedirs(frame_path_hsv)

    cap = cv2.VideoCapture(filePath)
    success = True
    frame_count = 1

    histValue=[]  # store the hist value of all frames
    while success:
        success, frame = cap.read()
        # params = []
        # params.append(cv2.CV_IMWRITE_PXM_BINARY)
        # params.append(1)
        if success:
            # convert to color space of HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cv2.imwrite(frame_path_hsv + "%d.jpg" % frame_count, hsv)

            cv2.imwrite(frame_path_rgb + "%d.jpg" % frame_count, frame)
            frame_count = frame_count + 1

            # store the value of histogram
            h=getHistogram(hsv)
            histValue.append(h)
    cap.release()

    return frame_path_rgb, frame_path_hsv, histValue


def getHistogram(frame):
    """
    get the histogram of one frame in color space of HSV
    :param frame: target frmae
    :return:
    """

    # get the hist value of h,s,v
    hist=[]
    hist_h = cv2.calcHist(frame, [0], None, [12], [0, 256])
    hist_s = cv2.calcHist(frame, [1], None, [5], [0, 256])
    hist_v = cv2.calcHist(frame, [2], None, [5], [0, 256])

    hist.append(hist_h)
    hist.append(hist_s)
    hist.append(hist_v)

    return hist


if __name__ == '__main__':
    # frame_path_rgb, frame_path_hsv = saveFrameOfVideos('resources/21_drink_u_nm_np1_fr_goo_9.avi')
    # getHistogramFromRGBtoHSV(frame_path_rgb,frame_path_hsv)
    frame=cv2.imread('resources/21_drink_u_nm_np1_fr_goo_9/hsv/1.jpg')
    hist=getHistogram(frame)
    for v in hist:
        print(v)
