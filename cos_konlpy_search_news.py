from os import name
from typing import Dict, List, Text
import urllib.request
import bs4
from konlpy.tag import Okt
from numpy import datetime64, dot
from numpy.linalg import norm 
import numpy as np 
from datetime import datetime

class News: #뉴스 저장용 클래스 제목, 내용, 링크, 시간, 언론사.
    def __init__(self, name,desc,link,time,media):
        self.name = name
        self.desc = desc
        self.link = link
        self.time = time
        self.media = media


# 코사인 유사도를 구하는 함수 
def cos_sim(a, b): 
	return dot(a, b)/(norm(a)*norm(b)) 

# 기준이 되는 키워드와 벡터 키워드 리스트를 받아서 키워드별 빈도를 구하는 함수
def make_matrix(feats, list_data): 
	freq_list = [] 
	for feat in feats: 
		freq = 0 
		for word in list_data: 
			if feat == word: 
				freq += 1 
		freq_list.append(freq) 
	return freq_list 

def getTextOfBList(vBList): 
    # 마지막 일치하는 태그 받아오기위해 사용
    # 시간을 일어올때 첫번째 일치하는 태그에 다른 내용이 들어있는 경우가 있어서 마지막 태그를 가져오도록 함.
    if(len(vBList) > 0):
        return vBList[len(vBList) - 1].text
    else :
        return ""
def getArticle_custom(vPara):
    okt = Okt() 
    # vPara = 키워드@@@@@url
    # 키워드와 URL을 @@@@@로 구분해서 받은 다음 split 한다.
    vSubUrl = str.split(vPara,"@@@@@")

    startTime = datetime.now()
    vKey = vSubUrl[0]
    vUrl = vSubUrl[1]

    vNewsCount = 0 #뉴스 번호
    vNewsDict = {} #뉴스 데이터 담을 딕셔너리
    vEndFlag = False #완료 체크용 플래그

    vCheckerList = []
    for _ in range(70): #페이지 변경용 루프 한페이지에 현재 10개씩 나옴
        if vEndFlag : break #마지막 페이지 까지 체크시 Break
        url = vUrl + "&start={0}".format(vNewsCount + 1) # 검색 시작점 변경 여기서 처음 시작시 1번부터 이후에는 11, 21, 31 번쨰 기사부터 찾아온다.
        try: #URL 소스 받아오기
            html = urllib.request.urlopen(url)
        except Exception as e:
            return("FAIL-CHECK-01")

        bsObj = bs4.BeautifulSoup(html, "html.parser") # 뷰티솝 라이브러리로 파싱하기
        bsNewsObj = bsObj.find_all("div",class_="news_area") # URL 에서 받아온 소스에서 찾은 뉴스 기사 리스트
        if (len(bsNewsObj) > 0 ): # 뉴스가 있는 경우에만 조회
            for infoNews in bsNewsObj:   # 해당 페이지의 뉴스기사 찾아서 반복 
                try:
                    #뉴스 객체에 저장
                    name = infoNews.find("a",class_="news_tit").text # 타이틀 가져오기
                    desc = infoNews.find("a",class_="dsc_txt_wrap").text #설명 가져오기
                    link = infoNews.find("a",class_="dsc_txt_wrap")['href'] #링크 가져오기
                    time = getTextOfBList(infoNews.find_all("span",class_="info")) #시간 가져오기 
                    media = infoNews.find("a",class_="info press").text #언론사 가져오기
                    news = News(name, desc, link, time, media) # 뉴스 객체
                    vNewsCount += 1

                    # print ("{0} 번째 뉴스".format(vNewsCount + 1))
                    # print("제목 : " + name)
                    # print("내용 : " + desc)
                    # print("링크 : " + link)
                    # print("시간 : " + time)
                    # print("언론사 : " + media)
                        
                    if(not name in vNewsDict): # 같은 제목이 있는 뉴스면 스킵한다.
                        #딕셔너리에 뉴스 추가
                        vNewsDict[name] = news

                    if(len(bsNewsObj) == 1):vEndFlag = True #페이지에 결과가 1개인 경우 마지막 뉴스까지 탐색 완료 (다음 페이지가 없는 경우 뉴스 1개만 나옴)
                    if vEndFlag : break 
                    # print("--------------------------------------------------------------")
                    
                except Exception as e:
                    # print (vNewsCount)
                    continue
                    # return("FAIL-CHECK-02")
    # 완벽 일치 제거
    i = 0
    vLiKey = []
    if(len(vNewsDict) > 0):
        
        for key, value in vNewsDict.items():
            i +=1
            # 탭으로 구분하여 스트링으로 만들기
            # 내용이 짧은 뉴스는 스킵한다.
            if(len(value.desc) > 55): # 55글자보다 내용이 적은 뉴스는 스킵
                checker = value.desc[:20] # 내용의 앞에서 20글자가 동일한 경우 같은 뉴스로 보고 스킵한다.
                if(checker not in vCheckerList):
                    vCheckerList.append(checker)
                else:    
                    vLiKey.append(key)
        for key in vLiKey:
            vNewsDict.pop(key)

    vResultData = ""
    vCheckCount = 0
    vSelectedNewsCount = 0

    if(len(vNewsDict) > 0):
        for _ in range(len(vNewsDict)):
            # print ("개수 : ", len(vNewsDict))
            if len(vNewsDict) == 1 : break
            vSelectedSubj = ""
            v1 = okt.nouns(vSelectedSubj)
            vLiKey = []
            for key, value in vNewsDict.items():
                # i +=1
                if(vSelectedSubj == "" ): 
                    v1 = okt.nouns(value.name) 
                    vSelectedSubj = value.name
                    vLiKey.append(key)
                    vSelectedNewsCount += 1
                    # vNewsDict.pop(key)
                    vResultData = vResultData + "{5} \t {0} \t{1} \t{2} \t{3} \t {4} \n".format(value.name, value.link, value.time, value.media, value.desc, vKey)
                else:
                    v2 = okt.nouns(value.name) 
                    v3 = v1 + v2
                    feats = set(v3) 
                    v1_arr = np.array(make_matrix(feats, v1)) 
                    v2_arr = np.array(make_matrix(feats, v2)) 
                    cs = cos_sim(v1_arr, v2_arr)
                    if (cs > 0.4):
                        vCheckCount += 1
                        # print (vSelectedSubj)
                        # print (value.name)
                        # print (cs)
                        vLiKey.append(key)

            for key in vLiKey:
                vNewsDict.pop(key)

                    # 읽어온 모든 뉴스 vResultData에 누적한다. (엑셀에 그대로 입력하기 위해서 탭으로 구분)
                    # 0, 4번은 내용중에 탭이 씹히게 만드는 문자가 있어서 공백 한칸 추가함.
                    # vResultData = vResultData + "{5} \t {0} \t{1} \t{2} \t{3} \t {4} \n".format(value.name, value.link, value.time, value.media, value.desc, vKey)
        #     # print("키워드 : " + vKey)
        #     # print("내용 : " + value.desc)
        #     # print("링크 : " + value.link)
        #     # print("시간 : " + value.time)
        #     # print("언론사 : " + value.media)
        #     # print("--------------------------------------------------------------!")
        
        # print("전체 : {0} / 중복 : {1} / 남은 뉴스 : {2}\n시작시간 : {3}, 종료시간 {4}".format(len(vCheckerList), vCheckCount, vSelectedNewsCount,startTime, datetime.now()))
        
        return vResultData
    else:
        return("뉴스 없음")
     
# 테스트용
# getArticle_custom("고려아연_고려아연_5@@@@@https://search.naver.com/search.naver?where=news&query=%22%EB%85%B8%EB%8F%99%22&sm=tab_opt&sort=1&photo=0&field=0&pd=3&ds=2021.06.21&de=2021.06.21&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20210621to20210621&is_sug_officeid=0")



