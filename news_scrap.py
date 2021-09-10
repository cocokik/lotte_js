
from os import replace
import urllib.request
import bs4
from konlpy.tag import Okt
from numpy import dot
from numpy.linalg import norm 
import numpy as np 
import logging

class News: #뉴스 저장용 클래스 제목, 내용, 링크, 시간, 언론사.
    def __init__(self, name,desc,link,time,media,key):
        self.name = name
        self.desc = desc
        self.link = link
        self.time = time
        self.media = media
        self.key = key
        self.key_num = 0


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

def replace_string(value): # csv로 입력시 인코딩 에러나는 부분
    # re_value = value.replace(u'\xa0', u' ')
    # re_value = re_value.replace(u'\u200b', u' ')
    # re_value = re_value.replace(u'\u2013', u' ')
    # re_value = re_value.replace(u'\u2022', u' ')
    # re_value = re_value.replace(u'\u2027', u' ')
    # re_value = re_value.replace(u'\u2024', u' ')
    # re_value = re_value.replace(u'\u2219', u' ')
    # re_value = re_value.replace(u'\u274d', u' ')
    # re_value = re_value.replace(u'\u3251', u' ')
    
    # re_value = re_value.replace(u'\u22c5', u' ')
    # re_value = re_value.replace(u'\u30fc', u' ')
    # re_value = re_value.replace(u'\u7afd', u' ')
    # re_value = re_value.replace(u'\ufffd', u' ')

    re_value =value
    re_value =re_value.replace(","," ") # CSV로 만들꺼기 때문에 , 제거
    re_value = re_value.replace("\"","“") # 더블쿼터 백더블쿼터로 변경 엑셀에 입력할때 오류 날때 있음
    if(re_value[0] == "=" or re_value[0] == "-" or re_value[0] == "+"): #첫글자가 =-+ 으로 시작하면 삭제
        re_value = re_value[1:] 

    # re_value = re_value.replace('  ', ' ') # 공백 2 -> 1 로
    return re_value

def getTextOfBList(vBList): 
    # 마지막 일치하는 태그 받아오기위해 사용
    # 시간을 일어올때 첫번째 일치하는 태그에 다른 내용이 들어있는 경우가 있어서 마지막 태그를 가져오도록 함.
    if(len(vBList) > 0):
        return vBList[len(vBList) - 1].text
    else :
        return ""

def checkContentKeyword(bsObj, news, logger, vTempCKList):
    tempContent = ''
    try:
        # URL 에서 받아온 소스에서 찾은 뉴스 내용 찾기
        bsNewsObj = bsObj.find("div", {'itemprop':"articleBody"})
        if bsNewsObj != None:
            tempContent = bsNewsObj.text.replace(" ","")
            checkContentKeyword_sub(news, logger, vTempCKList, tempContent)
            if news.key_num != 0:
                logger.info(f'##1##키워드 개수 : {news.key_num}')
                return
        if news.key_num == 0:
            bsNewsObj = bsObj.find("div", class_=['detail-body', 'art_txt', 'article-body', 'cont_cont', 'contentView', 'article_view', 'art_body', 'article_body', 'cont_art', 'textBody', 'content_area', 'article', 'content01 ', 'newsCont', 'articlebody', 'article_detail_body', 'news_body', 'article_content', 'news_contents', 'cnt_view', 'news_article', 'viewbox', 'body2', 'article-text', 'entry-content', 'txt', 'ab_text', 'retxt','nViewBody'])
            if bsNewsObj != None:
                tempContent = bsNewsObj.text.replace(" ","")
                checkContentKeyword_sub(news, logger, vTempCKList, tempContent)
                if news.key_num != 0:
                    logger.info(f'##2##키워드 개수 : {news.key_num}')
                    return
        if news.key_num == 0:
            bsNewsObj = bsObj.find("article", class_=['article'])
            if bsNewsObj != None:
                tempContent = bsNewsObj.text.replace(" ","")
                checkContentKeyword_sub(news, logger, vTempCKList, tempContent)
                if news.key_num != 0:
                    logger.info(f'##3##키워드 개수 : {news.key_num}')
                    return
        if news.key_num == 0:
            bsNewsObj = bsObj.find("article", {'itemprop':'articleBody'})
            if bsNewsObj != None:
                tempContent = bsNewsObj.text.replace(" ","")
                checkContentKeyword_sub(news, logger, vTempCKList, tempContent)
                if news.key_num != 0:
                    logger.info(f'##4##키워드 개수 : {news.key_num}')
                    return
        if news.key_num == 0:
            bsNewsObj = bsObj.find('body').find("script",id='fusion-metadata')
            if bsNewsObj != None:
                tempContent = bsNewsObj.text[:bsNewsObj.text.find('created_date')].replace(" ","")
                checkContentKeyword_sub(news, logger, vTempCKList, tempContent)
                if news.key_num != 0:
                    logger.info(f'##5##키워드 개수 : {news.key_num}')
                    return
        if news.key_num == 0:
            bsNewsObj = bsObj
            if bsNewsObj != None:
                tempContent = bsNewsObj.text.replace(" ","")
                checkContentKeyword_sub(news, logger, vTempCKList, tempContent)
                if news.key_num != 0:
                    logger.info(f'##6##키워드 개수 : {news.key_num}')
                    return
        if news.key_num == 0:
            logger.info(f'실화?? 키워드 개수 0 {news.link}')
    except Exception as e:
            print(f'{e} 키워드 개수찾기 에러')

def checkContentKeyword_sub(news, logger, vTempCKList, tempContent):
    for ckItem in vTempCKList:
        news.key_num += tempContent.count(ckItem)
    if ckItem == "ess":
        for ckItem in vTempCKList:
            news.key_num += tempContent.count('ESS')
        

def getArticle_custom(vPara):
    okt = Okt()
    vSimilarity = 0.4
    # 결과 파일 경로 (work폴더의 뉴스정리.csv) -> 나중에 5번 서브테스크에서 매크로로 메인파일에 입력한다.
    # 엑셀로 저장가능한데 엑셀 오류가 난 경우가 있어서 csv로 변경함.. ㅂㄷㅂㄷ
    csvPath = vPara[0]
    # 로그 경로
    path = vPara[1]
    # 사용할 언론사 리스트 (여기에 있는 언론사 제외한 언론사 뉴스는 스킵한다. 예외있음)
    vMediaList = str.split(vPara[2],"#")
    # 삭제할단어 리스트 (뉴스 제목중에 여기있는 단어가 포함된 뉴스는 스킵한다.)
    vDelList = str.split(vPara[3],"#")
    # 언론사 제한없이 검색할 키워드 : 여기리스트에 있는 키워드는 검새할때 제한언론사 필터링을 하지 않는다.
    vUnLimitedKeywordList = str.split(vPara[4],"#")
    # 키워드 묶음 확인 같은 묶음인 경우에 같이 중복체크한다. (빈값이거나 묶음이 바뀌면 중복체크위한 리스트 초기화함)
    vGroupKeywordList = str.split(vPara[5],"#")
    # 카운트할 키워드 리스트 만들기
    vCountKeywordList = str.split(vPara[6],"#")
    vNowKeywordGroup = ""
    # 위에서 뽑은 5개 데이터는 파라미터에서 삭제한다.
    del vPara[0]
    del vPara[0]
    del vPara[0]
    del vPara[0]
    del vPara[0]
    del vPara[0]
    del vPara[0]


    # 검색 뉴스가 증가하면 기하급수로 증가해서 너무 오래걸리는거 같음.. 아래 쪽 루프문에서 사용
    vDonusDescList = [] 
    vDonusNameList = [] 
    vNewsDescList = [] # 내용 중복 체크하기 위해 사용.
    vNewsDict = {} #뉴스 데이터 담을 딕셔너리

    # 로그 세팅
    logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
    logger = logging.getLogger()
    # 로그의 출력 기준 설정
    logger.setLevel(logging.INFO)
    # logger.setLevel(logging.DEBUG)
    # log 출력 형식
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # log 출력
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    # log를 파일에 출력
    file_handler = logging.FileHandler(path, encoding="UTF-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # vPara = 키워드@@@@@url
    # 키워드와 URL을 @@@@@로 구분해서 받은 다음 split 한다.
    i = -1
    for url in vPara: # 키워드별로 루프돌리기
        i += 1
        vSubUrl = str.split(url,"@@@@@")
        # 유사도 체크를 위한 배열 여기에 뉴스 하나씩 추가하면 새로 찾은 뉴스와 유사도 비교함
        # 키워드묶음 변경되거나 키워드묶음이 없으면 초기화
        if (vNowKeywordGroup != vGroupKeywordList[i] or vGroupKeywordList[i] == ""):
            vDonusDescList = [] # 내용
            vDonusNameList = [] # 제목 (형태소의 배열로 담는다.)
            logger.info(f'{vGroupKeywordList[i]} 키워드 묶음 변경으로 초기화')
        vNowKeywordGroup = vGroupKeywordList[i]
        
        vKey = vSubUrl[0]
        vUrl = vSubUrl[1]

        
        logger.info(f'{vKey} 시작 CK = {vCountKeywordList[i]}')
        logger.info(f'{vSubUrl}')

        vNewsCount = 0 # 뉴스 번호
        vEndFlag = False # 완료 체크용 플래그
        
        for _ in range(100): #페이지 변경용 루프 한페이지에 현재 10개씩 나옴
            if vEndFlag : break #마지막 페이지 까지 체크시 Break
            url = vUrl + "&start={0}".format(vNewsCount + 1) # 검색 시작점 변경 여기서 처음 시작시 1번부터 이후에는 11, 21, 31 번쨰 기사부터 찾아온다.
            
            vUrlFlag = True
            for _ in range(3): # 소스 받아올때 에러날수도 있어서 3회까지 시도
                try: #URL 소스 받아오기
                    html = urllib.request.urlopen(url)
                    vUrlFlag = True
                    break
                except Exception as e:
                    logger.info(f'{e} 에러발생')
                    vUrlFlag = False

            if (not vUrlFlag): continue # 소스 안받아지면 Continue

            bsObj = bs4.BeautifulSoup(html, "html.parser") # 뷰티솝 라이브러리로 파싱하기
            bsNewsObj = bsObj.find_all("div",class_="news_area") # URL 에서 받아온 소스에서 찾은 뉴스 기사 리스트
            if (len(bsNewsObj) > 0 ): # 뉴스가 있는 경우에만 조회
                for infoNews in bsNewsObj:   # 해당 페이지의 뉴스기사 찾아서 반복 
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
                        vNewsCount += 1 # 뉴스 개수 + 1
                        
                        # 제목이 10글자가 안되는 경우 스킵
                        if(len(name) < 10): continue

                        # 같은 제목이 있는 뉴스면 스킵한다.
                        if(name in vNewsDict): continue
                        
                        # 55글자보다 내용이 적은 뉴스는 스킵한다.
                        if(len(desc) < 55): continue
                        # 동일한 내용이 있는 경우에 스킵한다.
                        elif(desc[:20] in vNewsDescList): continue
                        
                        # 사용할 언론사인지 체크 (vUnLimitedKeywordList에 포함안된 키워드인 경우에만)
                        if(not vKey in vUnLimitedKeywordList):
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

                        # 삭제할 단어가 내용에 있는지 체크
                        for item in vDelList:
                            if desc.find(item) > -1:
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
                        dv2 = okt.nouns(desc) 
                        if(not vKey in vUnLimitedKeywordList):
                            if(len(v2) > 3):
                                for v1 in vDonusNameList:
                                    v3 = v1 + v2
                                    feats = set(v3) 
                                    v1_arr = np.array(make_matrix(feats, v1)) 
                                    v2_arr = np.array(make_matrix(feats, v2)) 
                                    cs = cos_sim(v1_arr, v2_arr)
                                    if (cs > vSimilarity):
                                        vBoolPut = False
                                        break
                            # 내용 유사도 체크 내용 유사도까지 체크하려면 주석 해제..
                            for v1 in vDonusDescList:
                                v3 = v1 + dv2
                                feats = set(v3) 
                                v1_arr = np.array(make_matrix(feats, v1)) 
                                v2_arr = np.array(make_matrix(feats, dv2)) 
                                cs = cos_sim(v1_arr, v2_arr)
                                if (cs > vSimilarity):
                                    vBoolPut = False
                                    break
                            if not vBoolPut : continue
                        
                        

                        # 뉴스내용 20글자 배열에 넣기 : 중복검사에 사용
                        vNewsDescList.append(desc[:20])
                        
                        # 뉴스제목 딕셔너리에 넣기 : 중복검사에 사용 / key = 뉴스제목 value = News인스턴스
                        vNewsDict[name] = news
                        # vResultData = vResultData + "{0} \t {1} \t{2} \t{3} \t{4} \t{5}\n".format(news.name, news.desc, news.time, news.key, news.link, news.media)

                        # 형태소 배열 vDonusNameList에 추가
                        if(len(v2) > 3):
                            vDonusNameList.append(v2) # 제목
                            vDonusDescList.append(dv2) # 내용 유사도까지 체크하려면 주석 해제..

                        # 뉴스에서 키워드가 몇게있는지 체크 
                        for _ in range(3): # 소스 받아올때 에러날수도 있어서 3회까지 시도
                            try: # URL 소스 받아오기
                                # headers = {'User-Agent':'Chrome/66.0.3359.181'}
                                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
                                req = urllib.request.Request(news.link, headers=headers)
                                html = urllib.request.urlopen(req)
                                vUrlFlag = True
                                break
                            except Exception as e:
                                vUrlFlag = False

                        if (not vUrlFlag): continue # 소스 안받아지면 Continue
                        
                        # 본문에서 찾을 키워드 리스트
                        vTempCKList = str.split(vCountKeywordList[i],',')
                        bsObj = bs4.BeautifulSoup(html, "html.parser") # 뷰티솝 라이브러리로 파싱하기

                        # 키워드 개수 체크
                        checkContentKeyword(bsObj, news, logger, vTempCKList)
                        
                        
                    except Exception as e:
                        logger.info(f'{e} 스킵')
                        vNewsCount += 1
                        continue
            else:
                if(vNewsCount == 0): logger.info('해당키워드 뉴스 검색 결과 없음') 
                logger.info('해당키워드 검색 종료')    
                break    
        logger.info(f'{vKey} 완료')
    try:
        if(len(vNewsDict) > 0): # 검색한 뉴스가 있는 경우
            # with open(csvPath, "a", -1, 'utf-8') as file:
            # with open(csvPath, "a") as file:
            with open(csvPath, "w",encoding='utf-8-sig') as file: # 이거 잘되면 replacestring 삭제 ㄱ
                logger.info('CSV생성 시작')
                for _, value in vNewsDict.items(): # 뉴스 정보 csv파일에 누적.
                    
                    name = replace_string(str(value.name)) # cp949 인코딩 오류나는 문자 제거
                    desc = replace_string(str(value.desc)) # 내용
                    key = replace_string(str(value.key)) # 키값 (여러개인 경우가 있음.)
                    text = f"""{name} ,'{desc} ,{value.time},{key},{value.link},{value.media}, {value.key_num}"""
                    try:
                        file.write(f"{text}\n")
                    except Exception as e:
                        logger.info(f'{e} 에러발생 (str 만드는중)')
            file.close()
            logger.info('CSV생성 완료')
            return "GOOD"
        else:
            logger.info(f'뉴스 없음.')
            return("뉴스 없음")
    except Exception as e:
            logger.info(f'{e} 에러발생')
            return("FAIL-CHECK-01")
