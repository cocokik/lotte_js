
import urllib.request
import json

def getToken():
    url="http://scazrdevw1:7777/v1/authentication"
    data = {}
    data["username"] = "rpa-api-test"
    data["password"] = "tjfls123!"
    
    data = json.dumps(data)
    data = str(data)
    data = data.encode('utf-8')
    req = urllib.request.Request(uWrl, data=data)
    html = urllib.request.urlopen(req, timeout=10)
    txt =  html.read().decode('utf-8')
    dict = json.loads(txt)
    token = dict['token']
    return token

def checkUpdateDevice():

    url="http://scazrdevw1:7777/v2/activity/list"
    headers = {"X-Authorization":getToken()}

    data ={}
    data["sort"] = [{"field":"startDateTime","direction":"desc"}]
    # data["filter"] ={"operator":"eq","value":"UPDATE","field":"status"}
    data["fields"] =[]
    data["page"] ={"length": 5}

    data = json.dumps(data)
    data = str(data)
    data = data.encode('utf-8')
    
    req = urllib.request.Request(url,headers=headers, data=data)
    html = urllib.request.urlopen(req, timeout=10)
    
    txt =  html.read().decode('utf-8')
    dict = json.loads(txt)
    dict_list = dict['list']
    # print(dict['list'])
    for item in dict_list:
        print (f"{item['deviceName']} / {item['status']}")

def checkMSSQL():
    pass

def insertMSSQL():
    pass

checkUpdateDevice()
