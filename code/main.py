#爬取豆瓣电影top100 和猫眼电影top100
import requests
from bs4 import BeautifulSoup
import bs4
import traceback
import re
import csv
import codecs
import os
import urllib
import urllib.request
import rawconduct
import matplotlib.pyplot as plt

#使用requests读取html内容
def getHTMLText(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""
    
#以下是爬取豆瓣的基本信息    
#寻找并提取基本信息 
def fillDBList(lst1,DBURL):
    html=getHTMLText(DBURL)
    soup=BeautifulSoup(html,'html.parser')
    #找到含有所有电影信息的大标签<li>
    li=soup.find("ol",attrs={'class':'grid_view'}).find_all("li")
    for i in li:
        try:
            #爬取电影的名称
            name=i.find("span",attrs={'class':'title'})
            #爬取电影的评分
            score=i.find("span",attrs={'class':'rating_num'})
            #爬取电影的别称，使用split函数
            wwname=i.find("span",attrs={'class':'other'}).text.split("/")[1]
            wname="".join(wwname.split())
            #爬取电影的评价人数，使用正则表达式
            x=i.find("div",attrs={'class':'star'}).text
            count=re.findall(r"\d+",x)[2]
            #所有电影信息中，第76位的电影并没有<简语>标签树，用判断语句来避免这一部电影被遗漏
            if i.find("span",attrs={'class':'inq'}):
                com=i.find("span",attrs={'class':'inq'}).string
            else:
                com='无'
            lst1.append([name.string,score.string,wname,count,com])
        except:
            continue
        
#将所提取信息写入表中并打印
def printDBList(lst1):
    count=0
    tplt1="{0:^5}\t{1:{6}^10}\t{2:{6}^3}\t{3:{6}<15}\t{4:{6}^10}\t{5:{6}<20}"
    print(tplt1.format("排名","名称","评分","别称","评价人数","简语",chr(12288)))
    for i in lst1:
        count=count+1
        print(tplt1.format(count,i[0],i[1],i[2],i[3],i[4],chr(12288)))
        
#打印出豆瓣电影TOP100的基本信息并将所有信息存入csv文件中
def main_DB():
    uinfo1=[]
    depth=4
    #网页每一页有25部电影，用循环来对网页挨个读取
    for i in range(depth):
        try:
            url='https://movie.douban.com/top250?start='+str(25*i)+'&filter='
            fillDBList(uinfo1,url)
        except:
            continue
    #printDBList(uinfo1)                          #打印豆瓣TOP榜所有爬取信息
    
#将列表的内容存在csv文件中，使用codecs来使文件以utf-8格式编码
    csvFile=codecs.open("DBmovie.csv","w+","utf_8_sig")
    try:
        count=0
        writer=csv.writer(csvFile)
        writer.writerow(('排名','名称','评分','别称','评价人数','简语'))
        for i in range(100):
            count=count+1
            x=uinfo1[i]
            #利用if语句消除储存第34部电影信息时的UnicodeDecodeError
            if count==34:
                x[2]='TenkvnoshiroRapyuta'
            writer.writerow((count,x[0],x[1],x[2],x[3],x[4]))
    finally:
        csvFile.close()

#对豆瓣电影海报的爬取
def getDBImag(url):
    html=getHTMLText(url)
    soup=BeautifulSoup(html,'html.parser')
    #创建路径，即创建一个存储图片的文件夹，引用os库
    #倘若存在folder_path，则略过，否则创建这个路径
    folder_path = "豆瓣电影海报/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    #爬取图片
    for i in range(25):
        div=soup.find_all('div',attrs={'class','pic'})[i]
        imglist=div.find('img')
        name=imglist.attrs['alt']
        img=imglist.attrs['src']
        #引用urllib库，对图片进行下载
        request=urllib.request.Request(img)
        response=urllib.request.urlopen(request)
        get_img=response.read()
        #创建一个格式为jpg的文件，将图片存储
        with open(folder_path+name+".jpg",'wb')as fp:
            fp.write(get_img)
            #print('图片下载完成')
            
#引用getDBImag函数，挨个网页进行爬取
def DBImag():
    for i in range(4):
        url='https://movie.douban.com/top250?start='+str(25*i)+'&filter='
        getDBImag(url)

#以下是爬取猫眼的基本信息
#提取信息
def fillMYList(lst2,MYURL):
    html=getHTMLText(MYURL)
    soup=BeautifulSoup(html,'html.parser')
    #找到包含电影基本信息的大标签<div>
    div=soup.find_all('div',attrs={'class':'board-item-content'})
    for i in div:
        try:
            #爬取电影名称
            name=i.find('p',attrs={'class':'name'})
            #爬取电影评分，该网站将评分拆分在两个并列的标签中
            score1=i.find('i',attrs={'class':'integer'})
            score2=i.find('i',attrs={'class':'fraction'})
            #爬取发行时间等，使用split函数
            rt=i.find('p',attrs={'class':'releasetime'}).text.split("：")[1]
            #爬取主演名字，使用split函数
            actorr=i.find('p',attrs={'class':'star'}).text.split("：")[1]
            actor="".join(actorr.split('\n'))
            lst2.append([name.string,score1.string+score2.string,rt,actor])
        except:
            continue

#把信息填入表中并进行打印
def printMYList(lst2):
    count=0
    tplt2="{0:^5}\t{1:{5}^10}\t{2:{5}^5}\t{3:{5}<15}\t{4:{5}<15}"
    print(tplt2.format("排名","名称","评分","上映时间","主演",chr(12288)))
    for i in lst2:
        count=count+1
        print(tplt2.format(count,i[0],i[1],i[2],i[3],chr(12288)))

#打印出猫眼电影top100的基本信息并将所有信息存入csv文件中
def main_MY():
    uinfo2=[]
    depth=10
    #网页每一页有10部影片，通过循环来对网页挨个读取
    for i in range(depth):
        try:
            url='http://maoyan.com/board/4?offset='+str(10*i)
            fillMYList(uinfo2,url)
        except:
            continue
    #printMYList(uinfo2)                 #打印爬取猫眼TOP榜的所有信息
    
#将列表的内容存在csv文件中，使用codecs来使文件以utf-8格式编码
    csvFile=codecs.open("MYmovie.csv","w+","utf_8_sig")
    try:
        count=0
        writer=csv.writer(csvFile)
        writer.writerow(('排名','名称','评分','上映时间','主演'))
        for i in range(100):
            count=count+1
            x=uinfo2[i]
            #利用if语句消除储存第80和第85部电影信息时的UnicodeDecodeError
            if count==80:
                x[3]='内山昂辉,佐仓绫音,Hiroki Goto'
            if count==85:
                x[3]='乌尔里希·穆埃,赛巴斯汀·柯赫,马蒂娜·戈黛特'
            writer.writerow((count,x[0],x[1],x[2],x[3]))
    finally:
        csvFile.close()

#对猫眼电影海报的爬取，与豆瓣海报爬取流程类似，“创建路径-下载图片-存储”
def getMYImag(url):
    html=getHTMLText(url)
    soup=BeautifulSoup(html,'html.parser')
    folder_path = "猫眼电影海报/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    imglist=soup.find_all('img',attrs={'class':'board-img'})
    for i in range(10):
        name=imglist[i].attrs['alt']
        img=imglist[i].attrs['data-src']
        request=urllib.request.Request(img)
        response=urllib.request.urlopen(request)
        get_img=response.read()        
        with open(folder_path+name+".jpg",'wb')as fp:
            fp.write(get_img)
            #print('图片下载完成')

#引用getMYImag函数，挨个网页进行爬取        
def MYImag():
    for i in range(10):
        url='http://maoyan.com/board/4?offset='+str(10*i)
        getMYImag(url)
        
def MAIN():
    main_DB()
    print("*****************************豆瓣电影数据爬取完毕*****************************")
    main_MY()
    print("*****************************猫眼电影数据爬取完毕*****************************")
    DBImag()
    print("*****************************豆瓣电影海报爬取完毕*****************************")
    MYImag()
    print("*****************************猫眼电影海报爬取完毕*****************************")
    print("******************************************************************************")
    if __name__=="__main__":
        rawconduct.main()
MAIN()




















