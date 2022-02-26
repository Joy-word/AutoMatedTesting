from contextlib import nullcontext
from ctypes.wintypes import POINT
import datetime
import xml.dom.minidom as minidom
import json

import data

class Step:
    number=0
    action=''
    actionType=''
    actionParam=''
    location=''
    duration=''

    def initActionType(self,action):
        if(action.find('鼠标左键') >= 0):
            self.actionType = 'left_mouse_click'
        elif(action.find('鼠标右键') >= 0):
            self.actionType = 'right_mouse_click'
        elif(action.find('键盘输入') >= 0):
            self.actionType = 'key_down'

        if(action.find('单击') >= 0):
            self.actionParam = '1'
        elif(action.find('双击') >= 0):
            self.actionParam = '2'
        elif(self.action.find('[') >= 0):
            beginIndex = self.action.find('[')
            endIndex = self.action.find(']')
            keyVal = str(self.action[beginIndex+1:endIndex]).replace("-","+").replace(" ... "," ").replace("... ","")
            self.actionParam = keyVal.lower()
            


def readFile(filepath):
    with open(filepath,'rb') as fp:
        content = fp.read()
    return str(content.decode())

def mhtToXmlStr(filepath):
    content = readFile(filepath)
    xmlContentBegin = content.find('<Report')
    xmlContentEnd = content.find('</Report>')
    xmlContent = content[xmlContentBegin:xmlContentEnd + 9]
    print(xmlContent)

    return xmlContent

def writeFile(filepath,content):
    with open(filepath,'wb') as fp:
        fp.write(content)


#先截取 xml 字段中的内容
xmlContent = mhtToXmlStr('data/ceshi.mht')
writeFile('data/xmlContent.xml',xmlContent.encode())

#找到所有 EachAction 节点
dom = minidom.parse('data/xmlContent.xml')
root = dom.documentElement
names = root.getElementsByTagName('EachAction')
print(names.length)


#建立新的 xml doc
doc = minidom.Document()
sessionNode = doc.createElement("Session")
doc.appendChild(sessionNode)

beforeNode = doc.createElement('StepAction')
beforeTime = ''

#开始轮询读取，并写入新的 xml doc
for name in names:
    step = Step()
    step.number = name.getAttribute('ActionNumber')
    time = name.getAttribute('Time')
    action = name.getElementsByTagName('Action')[0].childNodes[0].nodeValue
    step.action=name.getElementsByTagName('Description')[0].childNodes[0].nodeValue
    step.initActionType(action)
    step.location = name.getElementsByTagName('CursorCoordsXY')[0].childNodes[0].nodeValue

    #计算两步的间隔时间，用于填入 Duration 字段
    timedelta = 5.0
    if beforeTime != '':
        before = datetime.datetime.strptime(beforeTime, '%H:%M:%S')
        now = datetime.datetime.strptime(time, '%H:%M:%S')
        timedelta = (now - before).seconds

    stepActionNode = doc.createElement('StepAction')
    stepActionNode.setAttribute('StepNumber',step.number)
    sessionNode.appendChild(stepActionNode)

    locationNode = doc.createElement('Location')
    locationValue = doc.createTextNode('absolute')
    locationNode.appendChild(locationValue)
    stepActionNode.appendChild(locationNode)

    locationXYNode = doc.createElement('LocationXY')
    locationXYValue = doc.createTextNode(step.location)
    locationXYNode.appendChild(locationXYValue)
    stepActionNode.appendChild(locationXYNode)

    actionNode = doc.createElement('Action')
    actionValue = doc.createTextNode(step.action)
    actionNode.appendChild(actionValue)
    actionNode.setAttribute('type',step.actionType)
    actionNode.setAttribute('param',step.actionParam)
    stepActionNode.appendChild(actionNode)

    durationNode = doc.createElement('Duration')
    durationValue = doc.createTextNode(str(timedelta))
    durationNode.appendChild(durationValue)
    beforeNode.appendChild(durationNode)

    beforeNode = stepActionNode
    beforeTime = time

with open("data/test_key.xml", "w", encoding="utf-8") as f:
        # writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
        # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
        sessionNode.writexml(f, indent='', addindent='\t', newl='\n')









    