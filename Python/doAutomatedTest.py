from os import read
from ctypes.wintypes import POINT
import os
import xml.dom.minidom as minidom
import pyautogui
import time
import keyboard

import data


def readFile(filepath):
    with open(filepath,'rb') as fp:
        content = fp.read()
    return str(content.decode())


def mouseClick(location,clickTimes,lOrR):
    # 执行鼠标移动点击的事件
    pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.5,button=lOrR)

def mouseMove(location):
    # 执行鼠标移动点击的事件
    pyautogui.moveTo(location.x,location.y,duration=0.5)

def keyDown(key):
    #两个格式，如果是 “+” 串联两个按键，那么就是同时按下，如果是 “ ” 串联两个符号，那么就是依次按下
    #这里会有个小问题，加号键就不能用“+”了
    keyList = str(key).split(" ")
    for keyValue in keyList:
        mutiKeyList = str(keyValue).split("+")
        for mutiKeyValue in mutiKeyList:
            pyautogui.keyDown(mutiKeyValue)
        for mutiKeyValue in mutiKeyList:
            pyautogui.keyUp(mutiKeyValue)



def switchAction(root,location,actionType,actionParam,loopBegin='',loopEnd='',vars=''):
    if actionType == "left_mouse_click":
        mouseClick(location,int(actionParam),"left")
    elif actionType == "right_mouse_click":
        mouseClick(location,int(actionParam),"right")
    elif actionType == "mouse_move":
        mouseMove(location)
    elif actionType == "key_down":
        keyDown(actionParam)
    elif actionType == "loop":
        loopBeginBodys = loopBegin.split(",")
        loopEndBodys = loopEnd.split(",")
        varsBodysStr = vars.split(";")
        varsBodys = []
        for body in varsBodysStr:
            varsBody = body.split(",")
            varsBodys.append(varsBody)
        disassembleStep(root, loopBeginBodys, loopEndBodys, varsBodys)


def stopAction():
    print('stop action.')
    os._exit(0)


def disassembleStep(root, loopBeginBodys, loopEndBodys, vars):
    steps = []
    names = root.getElementsByTagName('StepAction')
    for name in names:
        if name.parentNode == root:
            step = data.Step()
            step.node = name
            location = name.getElementsByTagName('Location')[0]
            print(location.childNodes[0].nodeValue, end='\n')

            locationValue = str
            locationValueSplit = str()
            locationPValue = POINT
            visualImagePath = str


            action = name.getElementsByTagName('Action')[0]
            actionType = action.getAttribute('type')
            actionParam = action.getAttribute('param')
            if actionType != "loop":
                print(action.childNodes[0].nodeValue, end='\n')

            if(str(actionType).find("mouse") >= 0):
                if location.childNodes[0].nodeValue == 'absolute':
                    locationValue = name.getElementsByTagName('LocationXY')[0].childNodes[0].nodeValue
                    locationValueSplit = locationValue.partition(',')
                    locationPValue = POINT(int(locationValueSplit[0]),int(locationValueSplit[2]))
                elif location.childNodes[0].nodeValue == 'visualization':
                    visualImagePath = name.getElementsByTagName('VisualImagePath')[0].childNodes[0].nodeValue
                    locationPValue=pyautogui.locateCenterOnScreen(visualImagePath,confidence=0.9)

            duration = name.getElementsByTagName('Duration')[0].childNodes[0].nodeValue

            step.stepNumber = name.getAttribute('StepNumber')
            step.location = location.childNodes[0].nodeValue
            step.locationXY = locationValue
            step.locationPValue = locationPValue
            step.visualImagePath = visualImagePath
            step.action = action
            step.actionType = actionType
            step.actionParam = actionParam
            step.duration = duration
            steps.append(step)

    for var in vars:
        for loopBegin in loopBeginBodys:
            for step in steps:
                if step.stepNumber == loopBegin:
                    print(step.stepNumber, end=': ')
                    if(str(step.actionType).find("mouse") >= 0):
                        if step.location == 'visualization':
                            step.locationPValue=pyautogui.locateCenterOnScreen(step.visualImagePath,confidence=0.9)
                    switchAction(step.node,step.locationPValue,step.actionType,step.actionParam)
                    time.sleep(float(step.duration))
                    break
        for sigleVar in var:
            for step in steps:
                if step.stepNumber == sigleVar:
                    print(step.stepNumber, end=': ')
                    if(str(step.actionType).find("mouse") >= 0):
                        if step.location == 'visualization':
                            step.locationPValue=pyautogui.locateCenterOnScreen(step.visualImagePath,confidence=0.9)
                    switchAction(step.node,step.locationPValue,step.actionType,step.actionParam)
                    time.sleep(float(step.duration))
                    break
        for loopEnd in loopEndBodys:
            for step in steps:
                if step.stepNumber == loopEnd:
                    print(step.stepNumber, end=': ')
                    if(str(step.actionType).find("mouse") >= 0):
                        if step.location == 'visualization':
                            step.locationPValue=pyautogui.locateCenterOnScreen(step.visualImagePath,confidence=0.9)
                    switchAction(step.node,step.locationPValue,step.actionType,step.actionParam)
                    time.sleep(float(step.duration))
                    break


    


# 加监听，esc 中断脚本的运行
keyboard.add_hotkey('esc', stopAction)

# 解析 xml 文件 
# getElementsByTagName 拿到子节点，childNodes[0].nodeValue 就是子节点的值
# getAttribute 拿到该节点的对应的属性值
dom = minidom.parse('data/test_key.xml')
root = dom.documentElement
names = root.getElementsByTagName('StepAction')
print(names.length)
for name in names:
    #判断是否父节点就是 root 节点
    if name.parentNode == root:
        print(name.getAttribute('StepNumber'), end=': ')
        location = name.getElementsByTagName('Location')[0]
        print(location.childNodes[0].nodeValue, end='\n')

        locationValue = str
        locationValueSplit = str()
        locationPValue = POINT
        visualImagePath = str
        loopBegin=str
        loopEnd=str
        vars=str


        action = name.getElementsByTagName('Action')[0]
        actionType = action.getAttribute('type')
        actionParam = action.getAttribute('param')
        if actionType != "loop":
            print(action.childNodes[0].nodeValue, end='\n')
        else:
            loopBegin=action.getAttribute('loopBegin')
            loopEnd=action.getAttribute('loopEnd')
            vars=action.getAttribute('vars')

        if(str(actionType).find("mouse") >= 0):
            if location.childNodes[0].nodeValue == 'absolute':
                locationValue = name.getElementsByTagName('LocationXY')[0].childNodes[0].nodeValue
                locationValueSplit = locationValue.partition(',')
                locationPValue = POINT(int(locationValueSplit[0]),int(locationValueSplit[2]))
            elif location.childNodes[0].nodeValue == 'visualization':
                visualImagePath = name.getElementsByTagName('VisualImagePath')[0].childNodes[0].nodeValue
                locationPValue=pyautogui.locateCenterOnScreen(visualImagePath,confidence=0.9)

    
        switchAction(action,locationPValue,actionType,actionParam,loopBegin,loopEnd,vars)

        duration = name.getElementsByTagName('Duration')[0].childNodes[0].nodeValue
        time.sleep(float(duration))