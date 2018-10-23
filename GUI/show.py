import tkinter as tk

if __name__ == '__main__':
    # produce a window and set its attribute
    window = tk.Tk()
    window.title("图片分类器")
    window.geometry('512x300')

    # extract the key frames
    tk.Label(window, text='关键帧提取').grid(row=0, column=0)

    button_upload=tk.Button(window, text='视频上传')
    button_upload.grid(row=0, column=4)

    button_cluster=tk.Button(window, text='基于聚类')
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

