# coding=utf8

import csv
from app.model.User import User, Book
from app import db, mail, app
from jinja2 import Environment, PackageLoader
import pickle
import copy
import emailSender
import os
import sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")

db.drop_all()

db.create_all()
def readBookInfo():
    reader = csv.reader(file(os.path.join(sys.path[0],"books.csv"), "rb"))
    for line in reader:
        if reader.line_num == 1:
            continue
        try:
            bookName = str(line[0])
            priceBefore = int(float(line[1])*100)
            priceOff = int(float(line[2])*100)
            priceAfter = int(float(line[3])*100)
            newBook = Book(bookName=bookName, priceBefore=priceBefore,
                           priceOff=priceOff, priceAfter=priceAfter)
            db.session.add(newBook)
            db.session.commit()
        except Exception, e:
            print  e
            exit()

    print "Book info reading is completed..."

def readUserInfo():
    reader = csv.reader(file(os.path.join(sys.path[0],"All_Data_Original.csv"), "rb"))
    try:
        for line in reader:
            if reader.line_num == 1:
                continue
            name = str(line[27]).decode("gb2312")
            email = ""
            user = User(username=name, email=email)
            db.session.add(user)
    except Exception,e:
        print e
    db.session.commit()
    print "User info reading is completed..."


def readPurchase():
    reader = csv.reader(file(os.path.join(sys.path[0],"All_Data_Original.csv"), "rb"))
    try:
        for line in reader:
            if reader.line_num == 1:
                continue
            name = str(line[27]).decode("gb2312")
            print name
            user = db.session.query(User).filter_by(username=name).one()
            for i in range(18, 27):
                if line[i] == '1':
                    oneOfBooks = db.session.query(Book).filter_by(id=i-17).one()
                    user.books.append(oneOfBooks)
    except Exception,e:
        print e
    db.session.commit()
    print "Purchase info reading is completed..."



def makeEmail():
    users = User.query.all()

    env = Environment(loader=PackageLoader('app', 'templates'))
    template = env.get_template('bookEmail.html')

    all_price = 0.0
    with mail.connect() as conn:
        for u in users:
            price = 0
            for item in u.books:
                price += item.priceAfter



            # htmlContent = template.render(username=u.username,
            #                               books = sortedBooks,
            #                               booknum = len(sortedBooks),
            #                               price=price)
            print u.username,price
            all_price += price
            # emailAdd = u.email
            # print emailAdd

            # emailAdd = '545023318@qq.com'
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

    print all_price

# readBookInfo()

# makeEmail()
# print ('%.2f'%float(2.0))
if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print "Add args 'user' for readUserInfo(),'book' for readBookInfo()."
    #     exit(1)
    # func = sys.argv[1]
    # if func == 'user':
    #     readUserInfo()
    # elif func == 'book':
    #     readBookInfo()
    # elif func == 'purchase':
    #     readPurchase()
    # print "success"

    readBookInfo()
    readUserInfo()
    readPurchase()
    # makeEmail()
    pass
