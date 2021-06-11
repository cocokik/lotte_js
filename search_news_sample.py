from os import name
from typing import Dict, List, Text
import urllib.request
import bs4
class News: #뉴스 저장용 클래스
    def __init__(self, name,desc,link,time,media):
        self.name = name
        self.desc = desc
        self.link = link
        self.time = time
        self.media = media
def getTextOfBList(vBList): # 마지막 일치하는 태그 받아오기윟해 사용
    if(len(vBList) > 0):
        return vBList[len(vBList) - 1].text
    else :
        return ""
def getArticle_custom(vPara):
    #vPara = 키워드@@@@@url
    vSubUrl = str.split(vPara,"@@@@@")

    vKey = vSubUrl[0]
    vUrl = vSubUrl[1]

    vNewsCount = 0 #뉴스 번호
    vNewsDict = {} #뉴스 데이터 담을 딕셔너리
    vEndFlag = False #완료 체크용 플래그

    for _ in range(10): #페이지 변경용 루프 한페이지에 현재 10개씩 나옴
        if vEndFlag : break #마지막 페이지 까지 체크시 Break
        url = vUrl + "&start={0}".format(vNewsCount + 1) # 검색 시작점 변경
        try: #URL 소스 받아오기
            html = urllib.request.urlopen(url)
        except Exception as e:
            print("F")

        bsObj = bs4.BeautifulSoup(html, "html.parser") # 뷰티솝 라이브러리로 파싱하기
        bsNewsObj = bsObj.find_all("div",class_="news_area") #URL 에서 받아온 소스에서 찾은 뉴스 기사 리스트
        if (len(bsNewsObj) > 0 ): #뉴스가 있는 경우에만 조회
            for infoNews in bsNewsObj:   #해당 페이지의 뉴스기사 찾아서 반복 
                try:
                    #뉴스 객체에 저장
                    name = infoNews.find("a",class_="news_tit").text # 타이틀 가져오기
                    desc = infoNews.find("a",class_="dsc_txt_wrap").text #설명 가져오기
                    link = infoNews.find("a",class_="dsc_txt_wrap")['href'] #링크 가져오기
                    time = getTextOfBList(infoNews.find_all("span",class_="info")) #시간 가져오기 
                    media = infoNews.find("a",class_="info press").text #언론사 가져오기
                    news = News(name, desc, link, time, media)
                    vNewsCount += 1

                    # print ("{0} 번째 뉴스".format(vNewsCount + 1))
                    # print("제목 : " + name)
                    # print("내용 : " + desc)
                    # print("링크 : " + link)
                    # print("시간 : " + time)
                    # print("언론사 : " + media)
                        
                    #딕셔너리에 뉴스 추가
                    if(not name in vNewsDict):
                        vNewsDict[name] = news

                    if(len(bsNewsObj) == 1):vEndFlag = True #페이지에 결과가 1개인 경우 마지막 뉴스까지 탐색 완료
                    if vEndFlag : break 
                    # print("--------------------------------------------------------------")
                    
                except Exception as e:
                    print("F")
            
        else: #모든 페이지 조회 완료시 종료
            return("뉴스 없음") 

    # print(len(vNewsDict))
    # print(type(vNewsDict[0].name))
    vResultData = ""
    if(len(vNewsDict) > 0):

        for _, value in vNewsDict.items():
            # 탭으로 구분하여 스트링으로 만들기
            vResultData = vResultData + "{5}\t{0}\t{1}\t{2}\t{3}\t{4}\n".format(value.name, value.link, value.time, value.media, value.desc, vKey)
            # vResultData = vResultData + """<link>""" + value.link + """</link>""" +"\n"
            # vResultData = vResultData + """<description>""" + value.desc + """</description>""" +"\n"
            # vResultData = vResultData + """<pubDate>""" + value.time + """</pubDate>""" +"\n"
            # vResultData = vResultData + """<source>""" + value.media + """</source></item>""" +"\n"
            # vResultData = vResultData + """</item>"""

        # XML 버젼
        # vResultData = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><rss><channel>""" +"\n"
        # for _, value in vNewsDict.items():
        #     vResultData = vResultData + """<item><title>""" + value.name + """</title>""" +"\n"
        #     vResultData = vResultData + """<link>""" + value.link + """</link>""" +"\n"
        #     vResultData = vResultData + """<description>""" + value.desc + """</description>""" +"\n"
        #     vResultData = vResultData + """<pubDate>""" + value.time + """</pubDate>""" +"\n"
        #     vResultData = vResultData + """<source>""" + value.media + """</source></item>""" +"\n"
        #     vResultData = vResultData + """</item>"""
        #     # print("제목 : " + value.name)
        #     # print("내용 : " + value.desc)
        #     # print("링크 : " + value.link)
        #     # print("시간 : " + value.time)
        #     # print("언론사 : " + value.media)
        #     # print("--------------------------------------------------------------!")
        # vResultData = vResultData + """</channel></rss>"""

        return vResultData
    else:
        return("F")
     

# for i in range(10):
print(getArticle_custom("고려아연_온산_5@@@@@https://search.naver.com/search.naver?where=news&query=%22%EC%98%A8%EC%82%B0%22&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2021.06.11&de=2021.06.11&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20210611to20210611&is_sug_officeid=0"))

