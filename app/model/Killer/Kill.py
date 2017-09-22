# coding=utf8

import scipy.io as sio
import numpy as np
import math
import sys,os
from Captcha import NNCaptchaKiller
from Convert import codeChange

loadMatName = os.path.join(os.getcwd(), "app/model/Killer/Theta.mat")
loadData = sio.loadmat(loadMatName)
Theta1 = loadData["Theta1"]
Theta2 = loadData["Theta2"]

def sigmoid(num):
    return  1.0 / (1.0 + math.exp(-num))
sigmoid_Matrix = np.frompyfunc(sigmoid,1,1)

def getVCode(imgPath):
    item = NNCaptchaKiller(imgPath)
    XX = np.array(item.startDivideMatrix())
    if XX.shape[0] == 0:
        return
    size_x, size_y = XX.shape
    vcode = ""

    ones = np.ones((size_x, 1))
    XX_ones = np.column_stack((ones, XX))
    a = np.dot(XX_ones, Theta1.transpose())
    a = sigmoid_Matrix(a)

    ones = np.ones((size_x, 1))
    a_ones = np.column_stack((ones, a))
    res = np.dot(a_ones, Theta2.transpose())
    res = sigmoid_Matrix(res)

    for i in range(size_x):
        temp = res[i, :].tolist()
        maxIndex = temp.index(max(temp)) + 1
        code = chr(codeChange(2, maxIndex))
        vcode += code
    return vcode


#
# if __name__ == '__main__':
#     getVCode(r"D:\PyCharm Projects\NNCaptcha\TrainData\img\2.jpg")