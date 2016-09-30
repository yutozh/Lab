# coding=utf8

import csv
from app.model.User import User
from app import db, mail, app
from jinja2 import Environment, PackageLoader
import pickle
import copy
import emailSender
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

db.create_all()
def readUserInfo():
    reader = csv.reader(file(os.path.join(sys.path[0],"All_Data_Original.csv"), "rb"))
    for line in reader:
        bookInfo = ""
        if reader.line_num == 1:
            continue
        for i in range(18, 29):
            bookInfo += str(line[i])
        name = str(line[29]).decode("gb2312")
        email = str(line[30])
        user = User(username=name, email=email, bookInfo=bookInfo)
        db.session.add(user)
    db.session.commit()

def readBookInfo():
    reader = csv.reader(file(os.path.join(sys.path[0],"bookItems.csv"), "rb"))
    bookItems = {}
    i = 0
    for line in reader:
        book = []
        if reader.line_num == 1:
            continue
        try:
            book.append(str(line[0]))
            book.append('%.2f'%float(line[1]))
            book.append(float(line[2]))
            book.append('%.2f'%float(line[3]))
            bookItems[str(i)] = book
        except:
            print "csv格式有误"
            exit()
        i += 1

    outfile = open("bookdata.pkl",'wb')
    pickle.dump(bookItems, outfile)
    outfile.close()
    print "finish"

def makeEmail():
    users = User.query.all()
    inputfile = open("bookdata.pkl",'rb')
    bookDict = pickle.load(inputfile)
    env = Environment(loader=PackageLoader('app', 'templates'))
    template = env.get_template('bookEmail.html')

    all_price = 0.0
    with mail.connect() as conn:
        for u in users:
            bookStr = u.bookInfo
            bookValid = copy.deepcopy(bookDict)
            price = 0
            for i in range(0, len(bookStr)):
                if bookStr[i] == '2':
                    bookValid.pop(str(i))
            sortedBooks = sorted(bookValid.items())
            for j in sortedBooks:
                price += float(j[1][3])
            htmlContent = template.render(username=u.username,
                                          books = sortedBooks,
                                          booknum = len(sortedBooks),
                                          price=price)
            print price
            all_price += price
            # emailAdd = u.email

            emailAdd = '545023318@qq.com'
            # msg = Message('教材预定情况',
            #               recipients=[emailAdd],
            #               sender=("周于涛", "zyt4321@oattao.cn"),
            #               html=htmlContent)
            # conn.send(msg)


            # emailSender.sendEmail('教材预定情况',
            #                       htmlContent,
            #                       'html',
            #                       emailAdd)
            # print htmlContent
            exit(0)
    print all_price

# readBookInfo()

# makeEmail()
# print ('%.2f'%float(2.0))
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Add args 'user' for readUserInfo(),'book' for readBookInfo()."
        exit(1)
    func = sys.argv[1]
    if func == 'user':
        readUserInfo()
    elif func == 'book':
        readBookInfo()
    print "success"


    # readUserInfo()
    # readBookInfo()
    # makeEmail()