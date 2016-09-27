# coding=utf8
import os,sys
from PIL import Image

class CaptchaKiller:
    def __init__(self, path):
        f, e = os.path.splitext(path)
        if e not in [".jpg", ".bmp", ".jpeg"]:
            print "File Format ERROR", e
            exit(1)
        img = Image.open(path)
        if e != "bmp":
            newpath = f + ".bmp"
            img.save(newpath)
            img = Image.open(newpath)
        self.img = img

    def getResult(self):
        # removeNoise(img=self.img)
        self.img = self.img.convert("L")

        clearNoise(self.img, 200, 3, 5)

        threshold(img=self.img)

        # thining(img=self.img)
        # divide(img=self.img)
        # rotate()
        self.img.save("temp.bmp")


def threshold(img):
    x,y = img.size
    R = 0
    G = 0
    B = 0
    for i in xrange(x):
        for j in xrange(y):
            pos = (i,j)
            # rgb = img.getpixel(pos)
            # r,g,b = rgb
            # R = R + r
            # G = G + g
            # B = B + b
            # rate = r+g+b
            rate = img.getpixel(pos)
            if rate > 195:
                img.putpixel(pos, 255)
            else:
                img.putpixel(pos, 0)
    for i in xrange(x):
        img.putpixel((i, 0), 255)
        img.putpixel((i, y-1),255)
    for j in xrange(y):
        img.putpixel((0, j), 255)
        img.putpixel((x-1, j),255)
    return img

def clearNoise(image,G,N,Z):
    for i in xrange(0,Z):
        for x in xrange(1,image.size[0] - 1):
            for y in xrange(1,image.size[1] - 1):
                color = getPixel(image,x,y,G,N)
                if color != None:
                    image.putpixel((x,y),color)

def getPixel(image,x,y,G,N):
    L = image.getpixel((x,y))
    if L > G:
        L = True
    else:
        L = False

    nearDots = 0

    if L == (image.getpixel((x - 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y + 1)) > G):
        nearDots += 1

    if nearDots < N:
        return image.getpixel((x,y-1))
    else:
        return None

def removeNoise(img):
    x, y = img.size
    for i in xrange(x):
        for j in xrange(y):
            pos = (i,j)
            if i!=0 and i!=x-1 and j!= 0 and j!=y-1:
                # list1 = [img.getpixel((n,m))[0] for m in range(j-1,j+2) for n in range(i-1,i+2)]
                # list1.sort()
                # list2 = [img.getpixel((n, m))[1] for m in range(j - 1, j + 2) for n in range(i - 1, i + 2)]
                # list2.sort()
                # list3 = [img.getpixel((n, m))[2] for m in range(j - 1, j + 2) for n in range(i - 1, i + 2)]
                # list3.sort()
                # img.putpixel(pos, (list1[4],list2[4],list3[4]))
                list =  [img.getpixel((n, m)) for m in range(j - 1, j + 2) for n in range(i - 1, i + 2)]
                list.sort()
                img.putpixel(pos, list[4])
    return img

def divide(img):
    x,y= img.size
    pre_num = 0
    now_num = 0
    border = []
    for i in xrange(x):
        for j in xrange(y):
            value = img.getpixel((i,j))
            if value == 255:
                now_num = 1
                break
        if pre_num ^ now_num == 1:
            border.append(i)
        pre_num = now_num
        now_num = 0
    for i in [ x for x in range(len(border)) if x % 2 ==0]:
        im = img.crop((border[i],0, border[i+1], y+10))
        im.save("image/dividedImg/" + str(i/2) + ".bmp")

def rotate():
    imgNum = len([x for x in os.listdir(os.path.dirname("../yzm/image/dividedImg/"))])
    for m in range(imgNum):
        img = Image.open("../yzm/image/dividedImg/"+str(m)+".bmp")
        bestAngle = 0

        minWidth = 1000
        for n in range(-15, 16):
            img2 = img.rotate(n)
            # img2.save("/home/zyt/PycharmProjects/yzm/image/dividedImg/" + str(m) + ".bmp")
            x,y = img2.size
            pre_num = 0
            now_num = 0
            border = []

            for i in xrange(x):
                for j in xrange(y):
                    value = img2.getpixel((i, j))
                    if value == 255:
                        now_num = 1
                        break
                if pre_num ^ now_num == 1:
                    border.append(i)
                pre_num = now_num
                now_num = 0
            if len(border) < 2:
                border.append(x)
            width = border[1] - border[0]
            if width < minWidth:
                bestAngle = n
                minWidth = width
        # thining(img)
        img2 = img.rotate(bestAngle)

        img2.save(r"D:\PyCharm Projects\yzm\image\dividedImg"+str(m)+".bmp")

def thining(img):
    x ,y = img.size
    scanner = []
    for i in xrange(x):
        for j in xrange(y):
            index = 0
            if img.getpixel((i,j)) == 0 and i!=0 and i!=x-1 and j!= 0 and j!=y-1:
                for k in range(j-1, j+2):
                    for l in range(i-1, i+2):
                        scanner.append(0) if img.getpixel((l, k)) == 0 else scanner.append(1)
                scanner.pop(4)
                for m in range(8):
                    index += scanner[m]*pow(2, m)
                value = (erasetable[index] + 1 ) % 2 * 1
                img.putpixel((i,j),value)
                del scanner[:]

    # rate1 = R * 1000 / (R + G + B)
    # rate2 = G * 1000 / (R + G + B)
    # rate3 = B * 1000 / (R + G + B)
    #
    # print "rate:", rate1, rate2, rate3
    #
    # for i in xrange(x):
    #     for j in xrange(y):
    #         pos = (i, j)
    #         rgb = img.getpixel(pos)
    #         (r, g, b) = rgb
    #         n = r * rate1 / 1000 + g * rate2 / 1000 + b * rate3 / 1000
    #         if n >= 102:
    #             img.putpixel(pos, (255, 255, 255))
    #         else:
    #             img.putpixel(pos, (0, 0, 0))

erasetable = [
    0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
    1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
    0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
    1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
    1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
    1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,
    0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
    1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0,
    1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0
]

#
# c = CaptchaKiller(r"D:\PyCharm Projects\yzm\image\originImg\1472599958.jpeg")
# c.getResult()