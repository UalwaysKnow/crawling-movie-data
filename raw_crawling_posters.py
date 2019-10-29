import requests,os
import urllib
import urllib.request
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""
    
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
        
def MYImag():
    for i in range(10):
        url='http://maoyan.com/board/4?offset='+str(10*i)
        getMYImag(url)
MYImag()
