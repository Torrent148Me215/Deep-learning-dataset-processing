# -*- coding: utf-8 -*-
"""

@author: Lucas
"""

import pickle
from PIL import Image
import matplotlib.image as plimg
import numpy as np
import os

#PIL pillow : image library to process image (read image)
#matplotlib: transfer image type to array type
#numpy: process array
#pickle: basic sequencize data to write and read file 
# for example: pickle.dump(obj, file, [,protocol]) write obj to file
# for example: pickle.load(file)  read file and reconstruct obj

# Procedure
#　　(1) read the images
#　　(2) transfer image to array
#　　(3) processing array and merge all images into one whole array
#　　(4) Serialize with pickle, save text 

class DictSave(object):
    def __init__(self,filenames):
        self.filenames = filenames
        self.arr = []
        self.all_arr = []

    def image_input(self, filenames):
        for filename in filenames:
            self.arr = self.read_file(filename)
            if self.all_arr == []:
                self.all_arr = self.arr
            else:
                self.all_arr = np.concatenate((self.all_arr, self.arr))

    def read_file(self, filename):
        im = Image.open(filename) # 打开一个图像
         # 将图像的RGB分离
        r, g, b = im.split()
        # 将PILLOW图像转成数组
        r_arr = plimg.pil_to_array(r)
        g_arr = plimg.pil_to_array(g)
        b_arr = plimg.pil_to_array(b)
        # 将32*32二位数组转成1024的一维数组
        r_arr1 = r_arr.reshape(1024)
        g_arr1 = g_arr.reshape(1024)
        b_arr1 = b_arr.reshape(1024)
        # 3个一维数组合并成一个一维数组,大小为3072
        arr = np.concatenate((r_arr1, g_arr1, b_arr1))
        return arr

    def pickle_save(self, arr):
        print("Saving: ")
        # 构造字典,所有的图像数据都在arr数组里,我这里是个一维数组,目前并没有存label
        contact = {'data': arr}
        f = open('dataset', 'wb+')  ###还有此处用wb+ ，原作者用的 w ，一直报错
        pickle.dump(contact, f) # 把字典存到文本中去
        f.close()
        print("Save finished")

if __name__ == "__main__":
    filenames = []    
    for i in range(100):        
        filename = [os.path.join("images/","img%d" % i)+".png"]
        print(filename)
        filenames = filenames+filename
        print(filenames)    
        ds = DictSave(filenames)    
        ds.image_input(ds.filenames)    
        ds.pickle_save(ds.all_arr)    
        print("The size of final array:"+str(ds.all_arr.shape)) 
