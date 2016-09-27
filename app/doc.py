# coding=utf8
from docx import Document
from config import PATH

def createDocx(list, num, grade='2015'):
    document = Document()
    document.add_paragraph(u'以下是参与计算平均分的所有课程,可直接复制到申请表中.')
    document.add_paragraph(u'若一次性粘贴格式有误,可以按行分别粘贴.')
    cnt = 0
    for i in list:
        if i["used"] == True:
            cnt += 1
    table = document.add_table(rows=3, cols=cnt + 1)

    cnt = 0
    for i in list:
        if u"必修" in i["type"] and float(i["grade"]) != 0 \
                and i["year"] == grade and i["putong"] == u"普通" and i["used"] == True:
            cells =  table.rows[0].cells
            cells[cnt].text = i["name"]
            cells = table.rows[1].cells
            cells[cnt].text = i["point"]
            cells = table.rows[2].cells
            cells[cnt].text = str(i["grade"])
            cnt += 1

    cells = table.rows[0].cells
    cells[cnt].text = ""
    cells = table.rows[1].cells
    cells[cnt].text = ""
    cells = table.rows[2].cells
    cells[cnt].text = ""
    cnt += 1

    for i in list:
        if (u"公共选修" in i['type'] or u"辅修" in i["putong"]) and i["year"] == grade and i["used"] == True:
            cells = table.rows[0].cells
            cells[cnt].text = i["name"]
            cells = table.rows[1].cells
            cells[cnt].text = i["point"]
            cells = table.rows[2].cells
            cells[cnt].text = str(i["grade"])
            cnt += 1

    document.save(PATH + "app/temp/file_doc/result_{}.docx".format(str(num)))


