
import urllib.request
import bs4
from konlpy.tag import Okt
from numpy import dot
from numpy.linalg import norm 
import numpy as np 
from datetime import datetime
class News: #뉴스 저장용 클래스 제목, 내용, 링크, 시간, 언론사.
    def __init__(self, name,desc,link,time,media,key):
        self.name = name
        self.desc = desc
        self.link = link
        self.time = time
        self.media = media
        self.key = key


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
    vSimilarity = 0.4
    
    vMediaList = str.split(vPara[0],"#")
    vDelList = str.split(vPara[1],"#")
    del vPara[0]
    del vPara[0]

    # 유사도 체크를 위해서 사용할 리스트 여기서 쓰면 전체 체크인데 
    # 검색 뉴스가 증가하면 기하급수로 증가해서 너무 오래걸리는거 같음..
    # vDonusDescList = [] 
    # vDonusNameList = [] 
    vNewsDescList = [] # 내용 중복 체크하기 위해 사용.
    vNewsDict = {} #뉴스 데이터 담을 딕셔너리
    vResultData = ""

    
    totalCount = 0
    
    startTime = datetime.now() # 시간 확인용
    # vPara = 키워드@@@@@url
    # 키워드와 URL을 @@@@@로 구분해서 받은 다음 split 한다.
    for url in vPara: # 키워드별로 루프돌리기
        vSubUrl = str.split(url,"@@@@@")

        # 유사도 체크를 위한 리스트 여기에 뉴스 하나씩 추가하면 새로 찾은 뉴스와 유사도 비교함
        # 키워드마다 초기화
        vDonusDescList = [] 
        vDonusNameList = [] 
        
        vKey = vSubUrl[0]
        vUrl = vSubUrl[1]
        vNewsCount = 0 #뉴스 번호
        vEndFlag = False #완료 체크용 플래그
        
        for _ in range(30): #페이지 변경용 루프 한페이지에 현재 10개씩 나옴
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
                    totalCount += 1
                    try:

                        # 마지막 페이지인지 체크 및 탈출을 위한 부분
                        if vEndFlag : break 
                        if(len(bsNewsObj) == 1):vEndFlag = True #페이지에 결과가 1개인 경우 마지막 뉴스까지 탐색 완료 (다음 페이지가 없는 경우 뉴스 1개만 나옴)
                        

                        vBoolPut = True # 저장할 뉴스인지 체크 하기 위한 불
                        #뉴스 객체에 저장
                        name = infoNews.find("a",class_="news_tit").text # 타이틀 가져오기
                        desc = infoNews.find("a",class_="dsc_txt_wrap").text #설명 가져오기
                        link = infoNews.find("a",class_="dsc_txt_wrap")['href'] #링크 가져오기
                        time = getTextOfBList(infoNews.find_all("span",class_="info")) #시간 가져오기 
                        media = infoNews.find("a",class_="info press").text #언론사 가져오기
                        news = News(name, desc, link, time, media, vKey) # 뉴스 객체
                        vNewsCount += 1
                        # print(name)
                        # print ("{0} 번째 뉴스".format(vNewsCount + 1))
                        # print("제목 : " + name)
                        # print("내용 : " + desc)
                        # print("링크 : " + link)
                        # print("시간 : " + time)
                        # print("언론사 : " + media)
                        

                        if(name in vNewsDict): # 같은 제목이 있는 뉴스면 스킵한다.
                            # vBoolPut = False
                            continue
                        if(len(desc) < 55): # 55글자보다 내용이 적은 뉴스는 스킵한다.
                            # vBoolPut = False
                            continue
                        elif(desc[:20] in vNewsDescList): # 동일한 내용이 있는 경우에 스킵한다.
                            # vBoolPut = False
                            continue
                        
                        # 사용할 언론사인지 체크
                        vBoolPut = False
                        for item in vMediaList:
                            if media == item : 
                                vBoolPut = True
                                break
                        if not vBoolPut : continue

                        # 삭제할 단어가 제목에 있는지 체크
                        for item in vDelList:
                            if name.find(item) > -1:
                                vBoolPut = False
                                break
                        if not vBoolPut : continue

                        # 포토 뉴스 거르기 위한 추가 로직 
                        if(media == "연합뉴스" and link.find("=1196m") != -1): # 연합뉴스의 포토뉴스.
                            continue
                        if(media == "연합뉴스" and link.find("=1136m") != -1): # 연합뉴스의 그래픽뉴스.
                            continue
                        if(name.find("[사진]") != -1): # 제목에 [사진] 이 포함된 경우
                            continue
                        if(media == "뉴시스" and link.find("cID") == -1): # 뉴시스의 포토뉴스
                            continue
                        if(link.find("photo") != -1): # 링크에 포토가 있는 경우 스킵
                            continue
                        if(media == "뉴스핌" and desc[0] == "="):
                            continue
            

                        # 제목 유사도 체크
                        v2 = okt.nouns(name) 
                        for v1 in vDonusNameList:
                            v3 = v1 + v2
                            feats = set(v3) 
                            v1_arr = np.array(make_matrix(feats, v1)) 
                            v2_arr = np.array(make_matrix(feats, v2)) 
                            cs = cos_sim(v1_arr, v2_arr)
                            if (cs > vSimilarity):
                                vBoolPut = False
                                break
                        if not vBoolPut : continue
                        
                        # 내용 유사도 체크
                        # v2 = okt.nouns(name) 
                        # for v1 in vDonusDescList:
                        #     v3 = v1 + v2
                        #     feats = set(v3) 
                        #     v1_arr = np.array(make_matrix(feats, v1)) 
                        #     v2_arr = np.array(make_matrix(feats, v2)) 
                        #     cs = cos_sim(v1_arr, v2_arr)
                        #     if (cs > vSimilarity):
                        #         vBoolPut = False
                        #         break
                        if not vBoolPut : continue

                        # 뉴스내용 20글자 리스트에 넣기
                        vNewsDescList.append(desc[:20])
                        
                        # 뉴스제목 리스트에 넣기 
                        vNewsDict[name] = news

                        # 형태소 배열 리스트에 추가
                        vDonusNameList.append(okt.nouns(name)) # 제목
                        # vDonusDescList.append(okt.nouns(desc)) # 내용

                    except Exception as e:
                        # print ("vNewsCount")
                        continue
                        # return("FAIL-CHECK-02")
    # print(str(type(vNewsDict)))
    # print("selected:", len(vNewsDict))
    # print("total:", totalCount)
    if(len(vNewsDict) > 0): # 검색한 뉴스가 있는 경우
        for _, value in vNewsDict.items(): # 뉴스 정보 vResultData에 누적하기
            vResultData = vResultData + "{0} \t {1} \t{2} \t{3} \t{4} \t{5}\n".format(value.name, value.desc, value.time, value.key, value.link, value.media)
        return vResultData
    else:
        return("뉴스 없음")   
     
