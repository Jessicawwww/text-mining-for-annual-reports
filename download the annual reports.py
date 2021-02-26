# -*- coding: utf-8 -*-


#download the 2017 annual reports of all A-listed companies

###########################################
#导入必要的库
import requests  
import pandas as pd 
import re
from bs4 import BeautifulSoup  
import numpy as np
###########################################

file1=".../下载年报/17公司公告.xlsx"  #used for storing the links through which we can  downloading the annual reports
df_17 = pd.DataFrame(pd.read_excel(file1))  #read the spreadsheet above and load the data as dataframe for processing
stock_list=pd.read_excel(".../下载年报/stock_list.xlsx")


def get_16address(code,error_list):
#return to the download link
    try:
        info = df_17[df_17['code'] == code]
        raw_url=info.url.values[0]
        url=re.findall(r'LINK\("(.*?)",',str(raw_url))[0]
        if url!=None:
            return url
        else:
            error_list.append(code)
    except:
        error_list.append(code)



def getHTMLText(url):
    
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding="utf-8"
        return r.text
    except:
        print("获取网站失败")
        return ""


def outputTxt(address,lst):
    temp = np.array(lst)
    np.save(address,temp)
  
def loadTxt(address):
    data_a=np.load(address+".npy")
    return data_a.tolist()



#get the links to download the annual reports



error_list16=[]
error_list17=[]
num=len(stock_list.code)
root_path=".../17年报/"
for code in stock_list.code:
    print(num)
    url16=get_16address(code,error_list16)
    if url16!=None:
        html=getHTMLText(url16)
        soup=BeautifulSoup(html,'html.parser')
        info=soup.find_all('div',attrs={'class':'box4'})[0].a['href']
        pdf_url="http://news.windin.com/ns/"+info
        r=requests.get(pdf_url,stream=True)
        name=stock_list.ix[stock_list['code']==code].name.values[0]
        path=root_path+name+"17年年报.pdf"
        with open(path,'wb') as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
    else:
        error_list16.append(code)
    num-=1



name_16=[]
for code in error_list16:
    name=stock_list.ix[stock_list['code']==code].name.values[0]
    if name not in name_16:
        name_16.append(name)
             
outputTxt('.../17年缺失名单.txt',name_16)
