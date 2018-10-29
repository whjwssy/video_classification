import tkinter as tk
from tkinter.filedialog import askopenfilename

import frame_extraction.based_Clustering.clustering as cluster_cluster
import frame_extraction.based_Clustering.frame as cluster_frame

def uploadFunction(filePath):
    filePath=askopenfilename()
    print(filePath)

def extract_cluster(filePath, savePath):
    print(filePath)
    threshold = 0.0125
    weight = [0.5, 0.3, 0.2]

    frames, histogram, frame_size = cluster_frame.saveFrameOfVideos(filePath)
    histogramCluster = cluster_cluster.frameCluster(histogram, frame_size, threshold, weight, 0.05)
    keyFrames = cluster_cluster.keyFramesExtracte(histogram, histogramCluster, frames, savePath)

if __name__ == '__main__':
    # attribute
    filePath=''
    savePath='/Users/xuweijie/Downloads/gui_test/'

    # produce a window and set its attribute
    window = tk.Tk()
    window.title("图片分类器")
    window.geometry('512x300')

    # extract the key frames
    tk.Label(window, text='关键帧提取').grid(row=0, column=0)

    button_upload=tk.Button(window, text='视频上传',command=lambda: uploadFunction(filePath))
    button_upload.grid(row=0, column=4)

    button_cluster=tk.Button(window, text='基于聚类',command=lambda: extract_cluster(filePath, savePath))
    button_cluster.grid(row=1, column=1, pady=15, sticky='W')

    button_centroid=tk.Button(window,text='基于灰度质心')
    button_centroid.grid(row=1, column=3, pady=20, sticky='W')

    # classification
    tk.Label(window,text='图片分类').grid(row=2, column=0)

    button_knn=tk.Button(window,text='KNN')
    button_knn.grid(row=3, column=1, sticky='W')

    button_svm=tk.Button(window, text='SVM')
    button_svm.grid(row=3, column=3, sticky='W')


    # output
    textField=tk.Text(window)
    textField.grid(row=4, column=0, rowspan=16, columnspan=6)
    window.mainloop()

