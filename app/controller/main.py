# coding=utf8

from app import app, db, r
from flask import request, render_template, make_response, redirect, send_file
from app.model.User import User
from app.model.getGrade import login, getImg, parseGrade
import pickle
import json
import rsa
import urllib
from config import PATH

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


@app.route("/grade", methods=["GET","POST"])
def gradeIndex():
    r.incrby("PV",1)
    PV = r.get("PV")
    rate = float(r.get("SUCCESS")) * 100/ float(r.get("ALL"))
    return render_template("gradeIndex.html", PV=PV, rate="%.2f"% rate)

@app.route("/gradeDetail", methods=["GET"])
def getDetail():
    r.incrby("PV", 1)
    PV = r.get("PV")
    JSESSIONID = request.cookies.get("JID", '')
    username = request.cookies.get("username", '')
    name = request.cookies.get("name", '')
    csrf = request.args.get("csrf","")
    gradeRes = parseGrade(MYcsrf=csrf, JID=JSESSIONID, username=username)
    name = urllib.unquote(name).encode("ISO-8859-1","ignore") # urlZ中文解码

    if len(gradeRes[1]) == 0:
        return redirect("grade")

    pub_key = rsa.PublicKey(0x97928102320e3d9d8595cecf86cc00f178c02bd993e85f0d5f6f06566e3927a614fd124692ebc3a287803a98e968ab242d988d96fb971b0c6b3d266d7732d1e087dd34f15f975ae8f10a02707c2ac4f740e137b8860a635d866c11f458f4c57275bdeb6f26ac891c848d7a7bb2e98eb52dbad3a9daa575966346da5fad3b47dfL,65537)
    pri_key = rsa.PrivateKey(106437675396665291355483678683370935545014971346886683858098538997539181498749975904654335388357903533654172770006344449760253962620102013552573464919353349744158544580566670398633304931321053747230022121117499506744922822874453964939167344456875694371012527737487160712570108556931205055569151496386374223839,
                             65537, 56985903448711288937260041162123981665372008401659520014845988317220116887073548599150271146172423504110008303004144438304893282274350968941707677089843226288097318882343762530703368413457596803204391921702995756014021364157709738593798341316750911639599033651927197676848789110514897491071714558547839256449,
                             48553728192389990907083109690313643284407929600557979098864933929318943528026815319001213688729303263835476392919183570773981139836111276868576781802473995573281083,2192162772236873665766415549128272633431381665466475274237953690847839085492294631452598324525663858453701686796273292992518676571633438744930733)

    signature = rsa.encrypt(gradeRes[0][0] + '|'
                            +gradeRes[0][1] + '|'
                            +gradeRes[0][2]+'|'
                            +name+'|'
                            +str(username), pub_key).encode('base64')
    return render_template("gradeResult.html", statistics=gradeRes[0],
                           grade=gradeRes[1], name=name, username=username,
                           signature=str((signature)), PV=PV)

@app.route('/gradeSubmit', methods=["POST"])
def getGrade():
    username = request.form.get('username','')
    password = request.form.get('password','')
    captcha = request.form.get('captcha','')
    JSESSIONID = request.cookies.get("JSESSIONID", '')
    csrf = login(username, password, captcha, JSESSIONID)

    if csrf[0] == False:
        result = {"res": "false", "session": str(csrf[1])}
    else:
        result = {"res": "true", "session": str(csrf[1]), "JID":csrf[2], "nameLable":csrf[3]}
    return json.dumps(result)

@app.route('/image', methods=["GET", "POST"])
def image():
    img_info = getImg()
    response = make_response(img_info[0])
    response.headers['Content-Type'] = 'image/png'
    response.set_cookie("JSESSIONID", img_info[1])
    return response

@app.route("/gradeDetail/getDoc", methods=["GET"])
def getDoc():
    username = request.cookies.get("username", '')
    JSESSIONID = request.cookies.get("JID", '')
    user = request.args.get("target", '')
    if (user == username and JSESSIONID != ''):
        try:
            filename = "result_" + username + ".docx"
            response = make_response(send_file(PATH + "app/temp/file_doc/" + filename))
            response.headers["Content-Disposition"] = "attachment; filename={};".format(filename)
            return response
        except Exception,e:
            print e
            return redirect("grade")
    return redirect("grade")
