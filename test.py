import os
import time

def check_process():

    print(time.ctime() + " Start v2.1.1 60Sec")

    while(True):

        result = os.popen('tasklist /V /fi "IMAGENAME eq iexplore.exe" /fi "STATUS eq Not Responding"')
        tasklist_read = result.read().strip()
        time.sleep(1)
        kill_len = (len(tasklist_read.split("\n")))

        if kill_len >= 3:
            print(time.ctime() + " IE 응답없음")
            time.sleep(60)
            result = os.popen('tasklist /V /fi "IMAGENAME eq iexplore.exe" /fi "STATUS eq Not Responding"')
            time.sleep(1)
            tasklist_read = result.read().strip()
            kill_len = (len(tasklist_read.split("\n")))

            if kill_len >= 3:
                print(time.ctime() + " IE 응답없음으로 인한 IE킬")
                os.popen('taskKILL /f /im iexplore.exe')
            else :
                print(time.ctime() + " IE 응답없음 해제됨")
            time.sleep(10)


        result = os.popen('tasklist /V /fi "IMAGENAME eq aaplayer.exe" /fi "STATUS eq Not Responding"')
        tasklist_read = result.read().strip()
        time.sleep(1)
        kill_len = (len(tasklist_read.split("\n")))

        if kill_len >= 3:
            print(time.ctime() + " AA 응답없음")
            time.sleep(60)
            result = os.popen('tasklist /V /fi "IMAGENAME eq aaplayer.exe" /fi "STATUS eq Not Responding"')
            time.sleep(1)
            tasklist_read = result.read().strip()
            kill_len = (len(tasklist_read.split("\n")))

            if kill_len >= 3:
                print(time.ctime() + " AA 응답없음 으로인한 IE킬")
                os.popen('taskKILL /f /im iexplore.exe')
            else :
                print(time.ctime() + " AA 응답없음 해제됨")
            time.sleep(10)

        time.sleep(25)
check_process()