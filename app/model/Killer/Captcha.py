# coding=utf8
import os
from PIL import Image

class NNCaptchaKiller:
    def __init__(self, pathImg, pathCode=None, cnt=None):
        filename ,postfix = os.path.splitext(pathImg)
        if postfix not in [".jpg",".jpeg",".bmp"]:
            print "Format ERROR:", postfix
            exit(1)
        img = Image.open(pathImg)
        self.img = img
        self.originX, self.originY = img.size

        if pathCode:
            code = open(pathCode,'r')
            self.code = code.readline()
        if cnt:
            self.cnt = cnt

        self.baseDir = os.path.dirname(os.path.realpath(__file__))

    def startDivide(self):
        self.img = self.img.convert("L")

        self.expand()

        self.clearNoise(205,3,2)

        self.reduce()

        self.threshold(threshValue=195)
        # self.img.save("./MidData/"+"thre.jpg")

        self.divide(matrix=False)

    def startDivideMatrix(self):
        self.img = self.img.convert("L")

        self.expand()
        self.clearNoise(205,3,2)
        self.reduce()

        self.threshold(threshValue=195)
        # self.img.save(self.baseDir + "/MidData/"+"thre.jpg")

        self.res = []
        self.divide(matrix=True)
        return self.res

    def expand(self):
        # 扩大图像范围，以消除边缘噪声
        newBG = Image.new("L", (self.originX+10,self.originY+10), 255)
        newBG.paste(self.img, (5,5,5+self.originX,5+self.originY))
        self.img = newBG

    def reduce(self):
        # 恢复图像范围
        self.img = self.img.crop((5,5,5+self.originX,5+self.originY))

    def threshold(self, threshValue=195):
        x, y = self.img.size
        R = 0
        G = 0
        B = 0
        for i in xrange(x):
            for j in xrange(y):
                pos = (i, j)
                # rgb = img.getpixel(pos)
                # r,g,b = rgb
                # R = R + r
                # G = G + g
                # B = B + b
                # rate = r+g+b
                rate = self.img.getpixel(pos)
                if rate > threshValue:
                    self.img.putpixel(pos, 255)
                else:
                    self.img.putpixel(pos, 0)

        return

    # 过滤噪声
    def clearNoise(self, G, N, Z):
        for i in xrange(0, Z):
            for x in xrange(1, self.img.size[0] - 1):
                for y in xrange(1, self.img.size[1] - 1):
                    color = self._getPixel(self.img, x, y, G, N)
                    if color != None:
                        self.img.putpixel((x, y), color)

    def divide(self,matrix=False):
        x, y = self.img.size
        pre_num = 0
        now_num = 0
        border = []
        for i in xrange(x):
            for j in xrange(y):
                value = self.img.getpixel((i, j))
                if value == 0:
                    now_num = 1
                    break
            if pre_num ^ now_num == 1:
                border.append(i)
            pre_num = now_num
            now_num = 0
        if pre_num ^ 0 == 1:
            border.append(x-1)

        # 删除分割间隔小于3像素的坐标对
        itemToDel = []
        for i in [x for x in range(len(border)) if x % 2 == 0]:
            if(border[i+1]-border[i]<3):
                itemToDel.append(border[i])
                itemToDel.append(border[i+1])
        for i in itemToDel:
            border.remove(i)

        # 若监测出的字符数小于4个，则删除
        if len(border)<8:
            return None

        # 获取字符顶部和底部的边缘位置
        for i in [x for x in range(len(border)) if x % 2 == 0]:
            im = self.img.crop((border[i], 0, border[i + 1], y))
            imSizeX, imSizeY = im.size
            top = -1
            bottom = -1
            for m in xrange(imSizeY):
                for n in xrange(imSizeX):
                    value = im.getpixel((n, m))
                    if value == 0:
                        top = m
                        break
                if top > 0:
                    break

            for m in xrange(imSizeY-1,-1,-1):
                for n in xrange(imSizeX-1,-1,-1):
                    value = im.getpixel((n, m))
                    if value == 0:
                        bottom = m
                        break
                if bottom > 0:
                    break

            # 截取顶部和底部的空白部分
            im = im.crop((0, top, imSizeX, bottom+1))
            im = im.resize(im.size,Image.ANTIALIAS)

            bg = Image.new("L",(20,20),255)
            bg.paste(im,((20-im.size[0])/2,(20-im.size[1])/2,(20+im.size[0])/2,(20+im.size[1])/2))

            if not matrix:
                bg.save(self.baseDir + "/TrainData/items/" + self.code[(i / 2)] + "." + str(self.cnt) + ".bmp")
            else:

                x_, y_ = bg.size
                datas = []
                for i in xrange(x_):
                    for j in xrange(y_):
                        datas.append(1 if bg.getpixel((i, j)) == 255 else  0)
                self.res.append(datas)

    def _getPixel(self, image, x, y, G, N):
        L = image.getpixel((x, y))
        if L > G:
            L = True
        else:
            L = False

        nearDots = 0

        if L == (image.getpixel((x - 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y + 1)) > G):
            nearDots += 1

        if nearDots < N:
            return image.getpixel((x, y - 1))
        else:
            return None

if __name__ == "__main__":
    baseDir = os.path.dirname(os.path.realpath(__file__))
    rootDir = os.path.join(baseDir, "TrainData/img")
    listImg = os.listdir(rootDir)
    cnt = 1
    allDataNum = len(listImg)
    for i in range(allDataNum):
        imgPath = os.path.join(rootDir, listImg[i])
        if not os.path.isfile(imgPath):
            continue
        f, e = os.path.splitext(imgPath)
        if e==".dat":
            continue

        # 对于每一个jpg文件
        tagPath = f+".dat"
        filename = f.split('\\')[-1]
        item = NNCaptchaKiller(imgPath,
                               tagPath,
                               filename)
        item.startDivide()
        print "\r已完成{}/{}".format(str(cnt),allDataNum/2)
        cnt += 1