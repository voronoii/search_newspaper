import nltk
import codecs
import csv
import re
from nltk.corpus import stopwords
from konlpy.tag import Twitter

## 문장을 미리 어절 단위로 자른 다음 각 단어를 품사태깅하여 조사를 제거 

t = Twitter()

f = codecs.open("E:/magazine/kor.txt","r",'utf-8')
stopwords = [w.strip() for w in f.read().split(',')]
stopwords2 = ['는', '에', '를', '의', '로', '을']  #'으로', '에서'
stopwords3 = ['으로', '에서']


# ff = codecs.open('D:/opinionmining/newspaper/잡지제목 키워드.csv','r')
# rdr = csv.reader(ff)

# fff = open('D:/opinionmining/newspaper/교체된 잡지제목.csv','w', newline='')
# wr = csv.writer(fff)


def erase_special():
	f = codecs.open('E:/magazine/교체할 잡지목록.csv','r', encoding='utf-8-sig')
	rdr = csv.reader(f)

	ff = open('E:/magazine/sp_removed.csv','w', newline='', encoding='utf-8-sig')
	wr = csv.writer(ff)

	for idx, line in enumerate(rdr):
		newlist = line[0].split('[')[0]
		newlist = re.sub(r'[?|$|.|!|(|)|:|-]', ' ', newlist)
			
		
		print(newlist)
		wr.writerow([line[0], newlist])

		
def IsNum(s):
	try:
		int(s)
		return True
	except ValueError:
		return False



def eliminate_stopwords():
	
	f = open('E:/magazine/sp_removed.csv','r', encoding='utf-8-sig')
	rdr = csv.reader(f)

	ff = open('E:/magazine/교체된 잡지목록.csv','w', newline='' , encoding='utf-8-sig')
	wr = csv.writer(ff)

	for idx, line in enumerate(rdr):
		
		replaced_line = ""

		title_words = [w.strip() for w in line[1].split(' ')]
		replaced_line = ""

		  ## 조사가 하나도 없는 단어인 경우를 위해       
		for w in title_words: 

			if w and len(w) > 1 and IsNum(w) == False:  
			
				if len(w) > 2 and w[len(w)-1] in stopwords2:
					replaced_line += w[0:len(w)-1]+', '

					continue
				elif len(w) > 3 and w[len(w)-2:len(w)-1] in stopwords3:
					replaced_line += w[0:len(w)-2]+', '
					
					continue
				else:

					josa_count = 0 				    ## 문제점 : 조사를 re.sub하는 경우에 '의'를 삭제하면 기존 단어의 모든 '의'가 사라짐. 단어가 바뀌는것.
					tags = t.pos(w)
					# print(tags)
					if tags:  ##한 단어를 품사태깅 	
						idx = 0			
						tag_list = [e[0] for e in tags]

						for ele in tags:  ## ele = ('의', 'Josa')					
							
							if ele[1] == 'Josa':  ## 조사가 있으면 해당 단어에서 조사 제거 

								# print("단어: ", w)						
								# print("idx : ", idx, ele[0])
								# print("tag index : ", len(tag_list))
								
								if idx >= len(tag_list)/2:   # 조사가 단어의 끝에 위치할때에만 제거
									josa_len = len(ele[0].strip())
									word = w[0:len(w)-josa_len]						

									replaced_line += word+', '
									josa_count += 1
								else:
									replaced_line += w+', '
									josa_count += 1

								idx+=1

							else:
								idx+=1

						if josa_count == 0:					
							replaced_line += w+', '


					
		# if josa_count == 0:   #한 문장에 조사가 없는 경우 
		# 	replaced_line = line[0]

		print(replaced_line)
		wr.writerow([line[1], replaced_line])

	
	f.close()
	ff.close()




def main():
	eliminate_stopwords()



if __name__ == '__main__':
	main()