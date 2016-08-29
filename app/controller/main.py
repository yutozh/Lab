# coding=utf8

from app import app, db
from flask import request, render_template
from app.model.User import User
import pickle
import json

@app.route("/bookSearch", methods=["POST","GET"])
def main():
    if request.method == 'GET':
        return render_template('bookSearch.html')
    else:
        username = request.form.get('name','')
        user = User.query.filter_by(username=username).first()
        if user is not None:
            inputfile = open("bookdata.pkl", 'rb')
            bookDict = pickle.load(inputfile)
            bookStr = user.bookInfo

            for i in range(0, len(bookStr)):
                if bookStr[i] == '2':
                    bookDict.pop(str(i))
            sortedBooks = sorted(bookDict.items())

            print json.dumps(sortedBooks)
            return json.dumps(sortedBooks)
        else:
            return json.dumps({'result':'False'})
