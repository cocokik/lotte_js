import pyautogui
import time
import sys
import os

def startCheck(inputTime):

    print(time.ctime() + " Mouse Kill V1 [inputTime: %d]" % (inputTime))
    checkCount = 0
    mouseCheck = None

    while(True):
        time.sleep(inputTime)

        if mouseCheck == pyautogui.position():
            checkCount = checkCount + 1
        else:
            mouseCheck = pyautogui.position()
            checkCount = 0

        print(time.ctime() + " 현재위치" + pyautogui.position().__str__() + " 이전 위치" + mouseCheck.__str__() + " count: " + checkCount.__str__())

        if checkCount == 5:
            checkCount = 0
            os.popen('taskKILL /f /im iexplore.exe')
            print(time.ctime() + " kill")



if len(sys.argv) >= 2 and sys.argv[1].isdecimal():
    inputTime = int(sys.argv[1])
    inputTime = inputTime if (inputTime>5) else 5
else:
    inputTime = 15
startCheck(inputTime)

