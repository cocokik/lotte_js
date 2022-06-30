
import urllib.request
import json
# running 상태일때 status = UPDATE
def main():
    url="http://CR/v1/authentication"
    data = {}
    data["username"] = "id"
    data["password"] = "pw"
    
    data = json.dumps(data)
    data = str(data)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data=data)
    html = urllib.request.urlopen(req, timeout=10)
    txt =  html.read().decode('utf-8')
    dict = json.loads(txt)
    token = dict['token']
    getUpdateDevice(token)

def getUpdateDevice(tokens):
    url="http://CR/v2/activity/list"
    headers = {}
    headers["X-Authorization"] = tokens

    data ={}
    data["sort"] = [{"field":"startDateTime","direction":"desc"}]
    data["filter"] ={"operator":"eq","value":"UPDATE","field":"status"}
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

main()
