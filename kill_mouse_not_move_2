import pyautogui
import time
import sys
import os
import logging

def startCheck(inputTime):

    print(time.ctime() + " Mouse Kill V2 [inputTime: %d]" % (inputTime))
    checkCount = 0
    mouseCheck = None

    while(True):
        # time.sleep(inputTime)
        time.sleep(2)
        mouseNow = pyautogui.position()

        if mouseCheck == mouseNow:
            checkCount = checkCount + 1
            print(
                time.ctime() + " 현재위치" + mouseNow.__str__() + " 이전 위치" + mouseCheck.__str__() + " count: " + checkCount.__str__())
        else:
            checkCount = 0
            print(
                time.ctime() + " 현재위치" + mouseNow.__str__() + " 이전 위치" + mouseCheck.__str__() + " count: " + checkCount.__str__())
            mouseCheck = mouseNow



        if checkCount == 5:
            checkCount = 0
            for kill_item in kill_list:
                os.popen('taskKILL /f /im ' + kill_item)
                print(time.ctime() + ' ' + kill_item + ' kill')


if len(sys.argv) >= 2 and sys.argv[1].isdecimal():
    inputTime = int(sys.argv[1])
    inputTime = inputTime if (inputTime>3) else 3
else:
    inputTime = 15
if len(sys.argv) >= 3 :
    kill_list = sys.argv[2].split("/")
else:
    kill_list = ['iexplore.exe']

for kill_item in kill_list:
    print('kill list = ' + kill_item )
startCheck(inputTime)

