# -*- coding: utf-8 -*-

## 주요 메서드 ##
## crawl_link() : 디지털화 자료의 신문 70만건 링크 크롤링 [신문이름,신문제목,날짜,img원본링크, lod, mods]
##              result.csv 파일들 생성, 중간에 끊기면 1, 11, 111...번째 페이지부터 시작해야함 
## newspaper() : result.csv를 통해 목차 크롤링 [신문이름, 신문제목, 날짜, 목차]
##            table_contents.csv 파일들 생성

from bs4 import BeautifulSoup
import requests
import urllib.parse
import urllib.request
import operator
import os
import sys
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
global driver, opts
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import re
import numpy
import json
from bs4.element import NavigableString
# ua = UserAgent().random
# opts = Options()
# opts.add_argument("user-agent="+ua)
driver = webdriver.Firefox(executable_path=r"D:/geckodriver.exe")

# driver.implicitly_wait(3)
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))




def crawler(url):

    # ua = UserAgent().random
    try:
        driver.get(url)
        html = driver.page_source
        # req = urllib.request.Request(url, headers = {'User-Agent' : ua.random})
        # sourceCode = urllib.request.urlopen(req))

        soup = BeautifulSoup(html, 'lxml')
        return soup
    except urllib.error.HTTPError as e:
        if e.code == 408:
            pass
    except UnicodeEncodeError :
        pass
    return driver.get(url)


def crawl_links():  ## 주어진 링크에서 페이지네이션을 따라 모든 신문기사들을 크롤링 
                    ## [신문이름,신문제목,날짜,img원본링크, lod, mods]

  global f, wr, count, file_flag
  count = 0
  file_flag = 27
  
  pagenum = str(60*file_flag+1)
  # pagenum= str(381)

  url = 'http://www.nl.go.kr/nl/search/search_wonmun.jsp?pageNavTotal=&reSrchFlag=false&searchType=&topF1=title_author&kwd=&type=&typeCode=&facetDocYn=&facetYear=19451950&facetKdc=&facetFile=null&facetFile2=null&facetLang=null&facetGov=null&facetLicYn=&facetManageCode=null&facetSeShelfCode=null&facetTypeCode=&category=wonmun&subCategory=book&all=&dan=&yon=&disabled=&media=&web=&map=&music=&etc=null&archive=&cip=&korcis=&kolisNet=&pageNum='\
        +pagenum+'&pageSize=30&detailSearch=true&f1=&v1=&f2=&v2=&f3=&v3=&f4=&v4=&f5=&v5=&and1=&and2=&and3=&and4=&and5=&and6=&and7=&and8=&and9=&and10=&and11=&and12=&isbnOp=&isbnCode=&gu1=&guCode1=&and6=&gu2=&guCode2=&and7=&guCode3=&guCode4=&guCode5=&guCode6=&and8=&guCode7=&and9=&guCode8=&and10=&gu9=&and11=&guCode11=&gu12=&gu13=&gu14=&gu15=&gu16=&lib=null&sYear=19490000&eYear=19491232&sort=&desc=desc&selectedCount=0&hanja=y&total=180389&img=n&kdcddc=kdc&kdcddcCode=&acConNo=&acConNoSubject=null&acControlNoInfo=null&offer_dbcode_2s=CH49&media_code=&yearType=P&subject=&wonmunTabYn=Y&preKwd=#none'
  f = open('D:/newspaper/'+str(file_flag)+'.csv','w',newline='',encoding='utf-8-sig')
  wr = csv.writer(f)


  

  driver.get(url)
  temp = driver.find_element_by_tag_name('h4').find_element_by_tag_name('span').text
  endpage = int(re.sub('[(),]','',temp))
  pageCount = int(numpy.ceil(endpage/30)) ##페이지 총 개수 
  pagenation = int(numpy.floor(pageCount/10))  ## 페이지 10개 단위 개수 
  remainder = numpy.mod(pageCount, 10)
  
  # 페이지 1부터 페이지 pagenation*10까지 
  for page in range(1, pagenation+1):   
    firstpage = find_firstpage()
    print("firstpage : ", firstpage.text)
    find_searchList()

    for index in range(1, 10):      

      nextpage = find_nextpage(index)
      # print("nextpage : ", nextpage.text)
      nextpage.click()
      # driver.implicitly_wait(2)
      find_searchList()

    flip = driver.find_element_by_xpath('//*[@id="contentsArea"]/div[1]/div[32]/a[1]//following-sibling::span').find_element_by_tag_name('a')  
    flip.click()
    driver.implicitly_wait(3)

  # 페이지 pagenagion*10+1 부터 남은 remainder 페이지까지 
  for page in range(1, remainder+1):
    firstpage = find_firstpage()
    print("firstpage : ", firstpage.text)
    find_searchList()

    for index in range(1, 10):      

      nextpage = find_nextpage(index)
      # print("nextpage : ", nextpage.text)
      nextpage.click()
      # driver.implicitly_wait(2)
      find_searchList()

  f.close()

def extract_not_in_700k():

  lodList = []
  f = open('D://newspaper/3차년도 작업/발송용/3차_20만_29만.csv', 'r', encoding='utf-8-sig')
  rdr = csv.reader(f)
  for idx, line in enumerate(rdr):
    lodList.append(line[8].strip())

  f = open('D://newspaper/3차년도 작업/1,2차년도 통합본.csv', 'r', encoding='utf-8-sig')
  rdr = csv.reader(f)
  for idx, line in enumerate(rdr):
    lodList.append(line[8].strip())

  print(len(lodList))
  print(lodList[0])
  print(lodList[100000])





def find_searchList():
  
  global count, f, wr, file_flag
  searchList = driver.find_elements_by_class_name('searchList') 

  for item in searchList:
    newspaper = (item.find_element_by_class_name('info')).find_elements_by_tag_name('li')[1].text.split(':')[1]
    temp = item.find_element_by_class_name('bookName').find_element_by_tag_name('a')
    papername = temp.text.split('.')[1]
    
    temp2 = (temp.get_attribute('href').split('&')[0])
    lod_link = 'https://lod.nl.go.kr/page/CNTS-'+temp2[len(temp2)-11:]    
    original_link = item.find_element_by_class_name('onLine_original').find_element_by_tag_name('a').get_attribute('href')
    date = original_link.split('=')[4]    
    
    mods_link = 'http://nl.go.kr/app/nl/search/common/jangseoModsView.jsp?contents_id=CNTS-'+temp2[len(temp2)-11:]
    
   
    if count!= 1800:
      wr.writerow([newspaper, papername, date, original_link, lod_link,  mods_link])
      count += 1
    else:
      f.close()
      file_flag += 1
      f = open('D:/newspaper/'+str(file_flag)+'.csv','w',newline='',encoding='utf-8-sig')
      wr = csv.writer(f)
      wr.writerow([newspaper, papername, date, original_link, lod_link,  mods_link])      

      count = 1
      
     

def find_firstpage():
  firstpage = driver.find_element_by_class_name('pageRapper').find_element_by_xpath('//*[@id="contentsArea"]/div[1]/div[32]/a[1]')
  return firstpage

def find_nextpage(index):
  nextpage = driver.find_element_by_xpath('//*[@id="contentsArea"]/div[1]/div[32]/a[1]//following-sibling::a'+'['+str(index)+']')
  return nextpage


#====================================================================================================#
# 밑으로는 모듈들 



def crawl_lod():  ##lod가 있는 경우 #안쓰는 모듈
  result_dir = 'E:/newspaper/data_700k_ver2/'

  for filename in [f for f in os.listdir(result_dir) if f[0]!='.']:

    path = os.path.join(result_dir, filename)
    ff = open('E:/newspaper/newspaper/data_700k_lod/'+filename, 'w' ,newline = '',encoding='utf-8-sig')
    wr = csv.writer(ff)
    f = open(path,'r', encoding='utf-8-sig')
    rdr = csv.reader(f)

    for idx, line in enumerate(rdr):  

      link = line[4]
      soup = crawler(line[4])
      contents = ""

      if soup.find('table', {'class' : 'box_table'}):
        data = soup.find('table', {'class' : 'box_table'}).find_all('tr')
        
        string = ""
        
        for tr in data:
          # string += (tr.th.a.script.next_sibling.strip()+" : ")
          string += tr.td.li.find_all()[1].next_sibling.strip()+"\n"        
          

        lod = string.split('\n')
        lod_list = [ele for ele in lod if ele]
        #신문이름, 목차, 발행일, lod링크, 주제명, lod리스트
        completed = [line[0], line[1], line[2], line[4], line[6]] + lod_list
        wr.writerow(ele for ele in completed)
        completed = ""
        string = ""
        # wr.writerow([line[0], line[1], line[2], contents])


      elif soup.find_all('table', {'class' : 'tblStyle01'}) :
        data = soup.find_all('table', {'class' : 'tblStyle01'})[1].find_all('tr')[1:]
        string = ""
        for tr in data:
          tds = tr.find_all('td')
          # string += tds[0].find_all()[0].get_text()+" : "
          string += tds[1].find_all()[0].get_text()+"\n"
          contents += string
    
          string = ""
        

        lod = string.split('\n')
        lod_list = [ele for ele in lod if ele ]
        completed = [line[0], line[1], line[2], line[4]] + lod_list
        wr.writerow(ele for ele in completed)
        completed = ""
        string = ""
        # wr.writerow([line[0], line[1], line[2], contents])

      else:  ## lod 부재, mods 찾아야 하는 경우 
        contents = crawl_mods(line[5]).split('\n')
        completed = [line[0], line[1], line[2], line[5]]+contents
        wr.writerow(ele for ele in completed)



    f.close()
    ff.close()



#안쓰는 모듈
def get_mods(detail_link):
  driver.get(detail_link)
  mods_link = driver.find_elements_by_class_name('link_bk')[0].get_attribute('href')
  return mods_link

#안쓰는 모듈
def link_iterator_find_subject():
  result_dir = 'D:/opinionmining/newspaper/step1/'
  #for filename in [f for f in os.listdir(result_dir) if f[0]!='.']:
    # path = os.path.join(result_dir, filename)
  ff = open('D:/opinionmining/newspaper/step2/result-112.csv', 'w' ,newline = '',encoding='utf-8-sig')
  wr = csv.writer(ff)
  f = open('D:/opinionmining/newspaper/result111/result-112.csv','r', encoding='utf-8-sig')
  rdr = csv.reader(f)

  for idx, line in enumerate(rdr):  
    # responses = requests.get(line[5])
    driver.get(line[5])
    content = driver.page_source
    
    soup = BeautifulSoup(content, 'lxml-xml')
    if soup.find('subject'):
      subject = soup.find('subject').find('topic').text
      wr.writerow([line[0], line[1], line[2], line[3], line[4], line[5], subject])
    else:
      subject = ""
      wr.writerow([line[0], line[1], line[2], line[3], line[4], line[5], subject])


  ff.close()
  f.close()


#안쓰는 모듈
def crawl_mods(url):
  # fff = open('./testformod.csv','w',newline='',encoding='utf-8-sig')
  # wr = csv.writer(fff)

  # url = 'http://nl.go.kr/app/nl/search/common/jangseoModsView.jsp?contents_id=CNTS-00048204608'
  responses = requests.get(url)
  soup = BeautifulSoup(responses.content, 'lxml-xml')
  root = soup.find('mods')
  children = root.findChildren()
  string = ""
  for element in children:
    string += element.text+"\n"
  
  return string

# mods를 이용해 xml 파싱  
def crawl_keywords():  
  # data_dir = 'D:/2차 - 30만/'
  # for filename in [f for f in os.listdir(data_dir) if f[0]!='.']:
  #   path = os.path.join(data_dir, filename)

  f = open('D:/newspaper/30만-4.csv','r', encoding='utf-8-sig')
  rdr = csv.reader(f)
  with open('D:/newspaper/30만(키워드추출)-2.csv','w',newline='', encoding='utf-8-sig') as ff:
    wr = csv.writer(ff)
    for idx, line in enumerate(rdr):

      responses = requests.get(line[5])
      soup = BeautifulSoup(responses.content, 'lxml-xml')

      temp = []
      title = soup.find('title')
      if title:
        title = title.text
      else:
        title = " "
      
      titleHanja = ""
      try:
        titleHanja = soup.find('titleInfo').find('title').text
      except AttributeError:
        titleHanja = line[1]

      if soup.find('subject'):
        
        root = soup.find('subject')  
        children = root.findChildren()  #topic, genre, geographic, keyword
        tags = [ele.name for ele in children]

        
        sub_dict = {}
        for item in children:
          sub_dict[item.name] = item.text

        
        if 'topic' in tags:
          temp.append(sub_dict['topic']) 
        else:
          temp.append("")
        if 'genre' in tags:
          temp.append(sub_dict['genre']) 
        else:
          temp.append("")
        if 'geographic' in tags:
          temp.append(sub_dict['geographic']) 
        else:
          temp.append("")
        if 'keyword' in tags:
          temp.append(sub_dict['keyword']) 
        else:
          temp.append("") 

         
        write_list = [line[0],line[1],titleHanja,line[2],line[3],line[4],line[5]]+temp
        wr.writerow(ele for ele in write_list)

      else:
        wr.writerow([line[0],line[1],titleHanja,line[2],line[3],line[4],line[5]])

  f.close()

  
  


def newspaper():  ## result 파일을 이용해 신문 내 목차들 크롤링
                  ## [ 신문이름, 신문제목, 날짜, 목차]
  results_dir = 'D:/opinionmining/newspaper/results/' 
  file_count = 0 

  
  # for filename in [f for f in os.listdir(results_dir) if f[0]!='.']:

  file = open('D:/opinionmining/newspaper/results/result-0.csv', 'r', encoding='utf-8-sig')
  rdr = csv.reader(file)
  with open('D:/opinionmining/newspaper/test_step2/table_contents-0.csv','w',newline='', encoding='utf-8-sig') as f:
    wr = csv.writer(f)
    for idx, line in enumerate(rdr):

      soup = crawler(line[3])
      contentList = soup.find('div', {'id' : 'tocList'}).find_all('li')
      tostring = ""
      for string in contentList:
        tostring += string.get_text()+" "

      wr.writerow([line[0], line[1], line[2], tostring])
    file.close()


    # file_count += 1
 

def seperateLOD():
  loddir = 'D:/opinionmining/newspaper/result_to_lod/'  
  spdir = 'D:/opinionmining/newspaper/seperated/'  

  filenames = ['result-0.csv', 'result-1.csv', 'result-2.csv', 'result-3.csv', 'result-4.csv', 'result-5.csv', 'result-6.csv', 'result-7.csv', 'result-8.csv' ]
  for file in filenames:
    f = open(loddir+file, 'r', encoding='utf-8-sig')
    rdr = csv.reader(f)

    with open(spdir+file, 'w', encoding='utf-8-sig', newline='') as f:
      print(file)
      wr = csv.writer(f)
      for idx, line in enumerate(rdr):
        lod = line[3].split('\n')
        lod_list = [ele.split(':')[1].strip() for ele in lod if ele ]
        completed = [line[0], line[1], line[2]] + lod_list

        wr.writerow(ele for ele in completed)

    f.close()


def seperate():
  f = open('D:/opinionmining/newspaper/샘플.csv', 'r')
  rdr = csv.reader(f)

  ff = open('D:/opinionmining/newspaper/merge.csv','w',newline='',encoding='utf-8-sig')
  wr = csv.writer(ff)

  for idx, line in enumerate(rdr):
    menu = line[5].split('\n')
    menu = [ele.strip() for ele in menu if len(ele.strip()) >0]
    for ele in menu:
      wr.writerow([line[0], line[1], line[2], line[3], line[4], ele, line[6], line[7]])

    

  f.close()
  ff.close()
  


def main():
  crawl_links()


if __name__ == '__main__':
  main()