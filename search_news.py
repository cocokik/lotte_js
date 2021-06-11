import urllib.request
import bs4

def getArticle(vUrl):
    url = vUrl
    vTagArray = ["article-body-container","article"]
    
    try:
        html = urllib.request.urlopen(url)
    except Exception as e:
        return "F"
         
    bsObj = bs4.BeautifulSoup(html, "html.parser")
    
    for i in vTagArray:
        try:
            vFindArticle = ""

            vArticle = bsObj.find(i).find_all(["p","a", "span"])

            for p in vArticle:
                if "".join(p.find_all(text = True)) not in vFindArticle:
                    vFindArticle += "\n" + "".join(p.find_all(text = True)).strip()
                    
            return vFindArticle
                
        except Exception as r:
            vArticle = []
            if i == vTagArray[-1]:
                return "F"
            else:
                continue
