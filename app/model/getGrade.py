#coding: utf-8

from app import r
import sys
import requests
from bs4 import BeautifulSoup
import hashlib
import pytesseract
from PIL import Image
from captcha import clearNoise, threshold

from config import PATH
from app.doc import createDocx

reload(sys)
sys.setdefaultencoding("utf-8")

url = "http://210.42.121.133/servlet/Login"
url_img = "http://210.42.121.133/servlet/GenImg"
url_grade = "http://210.42.121.133/servlet/Svlt_QueryStuScore?csrftoken={csrf}&year=0&term=&learnType=&scoreFlag=0&t=Wed%20Aug%2031%202016%2014:10:43%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)"

head = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/44.0.2403.157 Safari/537.36"
}


def getImg(type=''):
    html_img = requests.get(url = url_img, headers = head)
    # 验证码对应的JESSEIONID
    JSESSIONID = html_img.headers['set-cookie'].split("=")[1].split(";")[0]
    cookie = str(JSESSIONID)
    if (type == ''):
        return (html_img.content, cookie)

    img = open(PATH + "app/temp/imgs/yzm{rand}.png".format(rand=type), "wb")
    img.write(html_img.content)
    img.close()

    img = Image.open(PATH + "app/temp/imgs/yzm{rand}.png".format(rand=type))
    img = img.convert("L")
    clearNoise(img, 200, 3, 5)  # 去噪
    threshold(img)  # 二值化
    return (img, cookie)

def login(username, password, captcha='', JSESSIONID=''):
    html_login = requests.get(url = url, headers = head)
    html_img = requests.get(url = url_img, headers = head)

    # rand = str(int(time.time()))+str(int(random.random()*1000))
    # img = open("../temp/imgs/yzm{rand}.png".format(rand=rand), "wb")
    # img.write(html_img.content)
    # img.close()
    #
    # img = Image.open("../temp/imgs/yzm{rand}.png".format(rand=rand))
    # img = img.convert("L")
    # clearNoise(img, 200, 3, 5)  # 去噪
    # threshold(img) # 二值化

    img_code = ''
    JID = ''
    if(captcha == ''):
        # 获取图片
        imgInfo = getImg(username)
        # 自动识别
        autoCode = pytesseract.image_to_string(imgInfo[0],lang="LAN" ,config="-psm 7 nobatch").replace(" ","")
        img_code = autoCode
        r.incrby("ALL",1)
        JID = str(imgInfo[1])
    else:
        img_code = captcha
        JID = JSESSIONID

    # img_code = raw_input("Please input the yzm:")

    cookie = {"JSESSIONID":JID}
    m = hashlib.md5()
    m.update(password)
    pwdMD5 = m.hexdigest()
    data = {
        "id":username,
        "pwd":pwdMD5,
        "xdvfb":img_code
    }

    html_index = requests.post(url = url , data= data, cookies = cookie, headers = head)
    if u"验证码错误" in html_index.text:
        print u"验证码错误"
        return (False,-1)
    if u"用户名/密码错误" in html_index.text:
        print u"用户名/密码错误"
        return (False,-2)
    if u"超时" in html_index.text:
        print u"超时"
        return (False,-3)

    read_index = BeautifulSoup(html_index.content.decode("gb2312"), "html.parser")
    if captcha == '':
        r.incrby("SUCCESS", 1)
    # 从首页中寻找csrf
    try:
        src = str(read_index.find_all("iframe")[1]["src"])
        name = read_index.find(id="nameLable").text.strip()
    except Exception,e:
        print read_index.text
        return (False,-4)
    place = src.find("csrftoken=") + len("csrftoken=")

    csrf = src[place:]

    return (True,csrf,JID,name)


def parseGrade(MYcsrf, JID, username, name, year="2015"):
    # 获取成绩信息
    url_grade_final = url_grade.format(csrf=MYcsrf)
    cookie = {"JSESSIONID": JID}

    html_grade = requests.get(url = url_grade_final, cookies = cookie, headers = head)
    text = html_grade.content.decode("gb2312")
    reader = BeautifulSoup(text, "html.parser")
    child = reader.find_all("tr")

    # 读取详细成绩
    grade = []
    for course in child:
        text = course.find_all("td")
        try:
            if not text:
                continue
            if not text[9].text:
                continue
        except Exception,e:
            continue
        grade.append({"name":text[1].text, "type":text[2].text, "point":text[3].text,
                      "putong":text[6].text, "year":text[7].text, "grade":int(float(text[9].text)),"used":False})
        # print text[1].text
        # print text[2].text
        # print text[3].text
        # print text[9].text
        # print "**************************"
    res_cal = cal(grade, year)
    statistics = res_cal[0:3]
    createDocx(grade, name, username)
    return (statistics,grade)

# 平均分计算
def cal(list, grade="2015"):
    sum1 = 0.0
    sum2 = 0.0
    allpoint = 0.0
    xx_grade = {"0.5":[],"1.0":[],"1.5":[],"2.0":[],"2.5":[],"3.0":[],"3.5":[],"4.0":[],"4.5":[],"5.0":[]}

    for i in list:
        if u"必修" in i["type"] and float(i["grade"]) != 0 \
                and i["year"] == grade and (i["putong"] == u"普通" or i["putong"] == u"重修"):
           sum1 += float(i["point"]) * float(i["grade"])
           allpoint += float(i["point"])
           i["used"] = True
        elif (u"选修" in i['type'] or u"辅修" in i["putong"]) and i["year"] == grade:
            if u"专业选修" in i['type']:
                sum2 += float(i["point"]) * float(i["grade"])
                i["used"] = True
            else:
                xx_grade[str(i["point"])].append(i)

    xx_grade_len = {}
    xx_grade_len_list = []
    for i in xx_grade:
        xx_grade[i].sort(key=lambda x:x["grade"], reverse=True)
        xx_grade_len.setdefault(i,len(xx_grade[i]))
    xx_grade_len_list = sorted(xx_grade_len.iteritems(),key=lambda d:d)
    xx_grade_len_list = map(lambda d:d[1], xx_grade_len_list)

    print xx_grade_len_list
    res_list = []
    max_ = 0.0
    isOverflow = False
    try:
        for a in range(xx_grade_len_list[0], -1, -1):
            for b in range(xx_grade_len_list[1], -1, -1):
                for c in range(xx_grade_len_list[2], -1, -1):
                    for d in range(xx_grade_len_list[3], -1, -1):
                        for e in range(xx_grade_len_list[4],-1, -1):
                            for f in range(xx_grade_len_list[5], -1, -1):
                                for g in range(xx_grade_len_list[6], -1, -1):
                                    for h in range(xx_grade_len_list[7], -1, -1):
                                        for i in range(xx_grade_len_list[8], -1, -1):
                                            for j in range(xx_grade_len_list[9], -1, -1):
                                                total = 0.5*a+b+1.5*c+2*d+2.5*e+3*f+3.5*g+4*h+4.5*i+5*j
                                                sum_ = 0.0
                                                if(total <= 16):
                                                    # for x in xx_grade["0.5"][0:int(a)]:
                                                    #     sum += float(x["grade"])
                                                    sum_ += sum(map(lambda d: float(d["grade"])*0.5, xx_grade["0.5"][0:int(a)]))
                                                    sum_ += sum(map(lambda d: float(d["grade"])*1.0, xx_grade["1.0"][0:int(b)]))
                                                    sum_ += sum(map(lambda d: float(d["grade"])*1.5, xx_grade["1.5"][0:int(c)]))
                                                    sum_ += sum(map(lambda d: float(d["grade"])*2.0, xx_grade["2.0"][0:int(d)]))
                                                    sum_ += sum(map(lambda d: float(d["grade"])*2.5, xx_grade["2.5"][0:int(e)]))
                                                    sum_ += sum(map(lambda d: float(d["grade"])*3.0, xx_grade["3.0"][0:int(f)]))
                                                    sum_ += sum(map(lambda d: float(d["grade"])*3.5, xx_grade["3.5"][0:int(g)]))
                                                    sum_ += sum(map(lambda d: float(d["grade"])*4.0, xx_grade["4.0"][0:int(h)]))
                                                    sum_ += sum(map(lambda d: float(d["grade"])*4.5, xx_grade["4.5"][0:int(i)]))
                                                    sum_ += sum(map(lambda d: float(d["grade"])*5.0, xx_grade["5.0"][0:int(j)]))


                                                    if sum_ > max_:
                                                        max_ = sum_
                                                        res_list = [a, b, c, d, e, f, g, h, i, j]
                                                        # print total,a,b,c,d,e,f,g,h,i,j,max_
                                                    if not isOverflow:
                                                        raise Exception
                                                else:
                                                    isOverflow = True
    except Exception:
        pass

    sum2 += max_
    try:
        a, b, c, d, e, f, g, h, i, j = res_list
    except:
        print "error"
        return ("","","")
    (map(add, xx_grade["0.5"][0:int(a)]))
    (map(add, xx_grade["1.0"][0:int(b)]))
    (map(add, xx_grade["1.5"][0:int(c)]))
    (map(add, xx_grade["2.0"][0:int(d)]))
    (map(add, xx_grade["2.5"][0:int(e)]))
    (map(add, xx_grade["3.0"][0:int(f)]))
    (map(add, xx_grade["3.5"][0:int(g)]))
    (map(add, xx_grade["4.0"][0:int(h)]))
    (map(add, xx_grade["4.5"][0:int(i)]))
    (map(add, xx_grade["5.0"][0:int(j)]))

    if allpoint>0:
        F1 = sum1/allpoint
    else:
        F1 = 0
    F2 = sum2 * 0.002
    F3 = F1 + F2


    return ("%0.6f"%F1,("%0.6f"%F2).zfill(9),"%0.6f"%F3)

def add(z):
    z["used"] = True
    