from konlpy.tag import Okt
from numpy import dot
from numpy.linalg import norm 
import numpy as np 


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
okt = Okt() 
text1 = '안녕 나는 애플을 만든 스티브잡스야' 
text2 = '안녕 나는 페이스북을 만든 주커버그야' 
text3 = '나는 애플과 스티브잡스를 좋아해. 주커버그는 별로야' 
v1 = okt.nouns(text1) 
v2 = okt.nouns(text2) 
v3 = okt.nouns(text3) 
# 단어들을 중복제거를 위해, set에 데이터를 쌓는다 
v4 = v1 + v2 + v3 
feats = set(v4) 
v1_arr = np.array(make_matrix(feats, v1)) 
v2_arr = np.array(make_matrix(feats, v2)) 
v3_arr = np.array(make_matrix(feats, v3)) 
cs1 = cos_sim(v1_arr, v2_arr) 
cs2 = cos_sim(v1_arr, v3_arr) 
cs3 = cos_sim(v2_arr, v3_arr)
print('v1 <-> v2 = ', cs1) 
print('v1 <-> v3 = ', cs2) 
print('v2 <-> v3 = ', cs3)
