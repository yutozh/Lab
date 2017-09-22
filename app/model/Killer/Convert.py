# coding=utf8
from PIL import Image
import os

# 为每一个字符生成一个像素值list
def getImgMatrix(img):
    x, y = img.size
    datas = []
    for i in xrange(x):
        for j in xrange(y):
            datas.append(1 if img.getpixel((i,j)) == 255 else  0)
    return datas

def goThrough(dirPath):
    fileList = os.listdir(dirPath)
    allDataNum = len(fileList)
    resultXFile = open("X.dat","w")
    resultYFile = open("y.dat","w")
    for i in range(allDataNum):
        filePath = os.path.join(dirPath, fileList[i])
        f,e = os.path.splitext(filePath)
        img = Image.open(filePath)

        # 像素值
        value = getImgMatrix(img)
        # 标签值
        code = ord(f.split('\\')[-1].split('.')[0])
        code = codeChange(1, code)

        resultXFile.writelines(str(value).replace("[","").replace("]","").replace(","," "))
        resultXFile.writelines("\n")
        resultYFile.writelines(str(code))
        resultYFile.writelines("\n")

def codeChange(type,code):
    # 1-10 表示数字0-9
    # 11-36 表示字母A-Z
    # 37-62 表示字母a-z
    if type==1:
        # ascii to val
        if code>= 48 and code<= 57:
            return code - 47
        elif code>=65 and code<= 90:
            return code - 54
        elif code>=97 and code<=122:
            return code - 60
    elif type==2:
        # val to ascii
        if code>= 1 and code<= 10:
            return code + 47
        elif code>=11 and code<= 36:
            return code + 54
        elif code>=37 and code<=62:
            return code + 60
if __name__ == '__main__':
    baseDir = os.path.dirname(os.path.realpath(__file__)) + '\\TrainData\\items'
    print baseDir
    goThrough(baseDir)
    print "OK"
