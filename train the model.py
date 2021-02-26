# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 09:19:58 2019

@author: Administrator
"""

import matplotlib.pyplot as plt
import docx
import glob
import re
#import jieba.analyse
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression


#clean the data and unfify the form of data
def getAllFile(path):#convert the form
    doc_list=[]
    for doc in glob.glob("{}/*.docx".format(path)):
        doc=doc.replace("\\" ,"/")
        doc_list.append(doc)
    return doc_list
 

def getMatrix(load_path,saved_path):
    data1=pd.read_csv(".../关键字表/chapter1_keywords.csv",engine='python')#这个engine='python'可以能读取地址有中文字符串的文件
    data2=pd.read_csv(".../关键字表/chapter2_keywords.csv",engine='python')
    del data1['Unnamed: 0']
    del data2['Unnamed: 0']

    chapter1_words=list(data1.word.values)
    chapter2_words=list(data2.word.values)
    total_word=len(chapter1_words)+len(chapter2_words)
    doc_list=getAllFile(path)
    x=np.ones((len(doc_list),total_word))    
    stock_num=0
    for doc in doc_list:
        print(stock_num)
        file=docx.Document(doc)
        passage=""
        for para in file.paragraphs:
            passage=passage+para.text
        try:
            for result in re.findall(r'详见.*?公司业务概要',str(passage)):
                if len(result)<20:
                    passage=passage.replace(result,"")
        except:
            passage=passage
        try:
            for result in re.findall(r'参见.*?公司业务概要',str(passage)):
                if len(result)<20:
                    passage=passage.replace(result,"")
        except:
            passage=passage
        try:
            for result in re.findall(r'详见.*?经营情况讨论与分析',str(passage)):
                if len(result)<20:
                    passage=passage.replace(result,"")
        except:
            passage=passage
        try:
            for result in re.findall(r'参见.*?经营情况讨论与分析',str(passage)):
                if len(result)<20:
                    passage=passage.replace(result,"")
        except:
            passage=passage
        try:
            for result in re.findall(r'详见.*?重要事项',str(passage)):
                if len(result)<20:
                    passage=passage.replace(result,"")
        except:
            passage=passage
        try:
            for result in re.findall(r'参见.*?重要事项',str(passage)):
                if len(result)<20:
                    passage=passage.replace(result,"")
        except:
            passage=passage
        chapter_info1=re.findall(r'公司业务概要.*?经营情况讨论与分析',str(passage),re.DOTALL)      
        if chapter_info1==[]:                                                                    
            print("chapter1 error")      
     
            chapter1=""                                                       
        else:
            count=[len(info) for info in chapter_info1]                                          
            chapter1=chapter_info1[count.index(max(count))] 
                                        
            if len(chapter1)<300:                                                                
                chapter1=""
                print("chapter1 error")

        chapter_info2=re.findall(r'经营情况讨论与分析.*?重要事项',str(passage),re.DOTALL)

        if chapter_info2==[]:
            print("chapter2 error")
            chapter2=""
        else:
            count=[len(info) for info in chapter_info2]                                          
            chapter2=chapter_info2[count.index(max(count))]                                      
            if len(chapter2)<300:                                                                
                chapter2=""
                print("chapter2 error") 
          
        for word_code in range(len(chapter1_words)):
            word_count=chapter1.count(chapter1_words[word_code])
            x[stock_num][word_code]=word_count
        for word_code in range(len(chapter2_words)):
            word_count=chapter2.count(chapter2_words[word_code])
            x[stock_num][len(chapter1_words)+word_code]=word_count    
        stock_num+=1
    np.savetxt(saved_path,x)

#train the model
#use the data from 2016 annual reports to train the model
load_path=".../16年年报/"
saved_path=".../模型预测/x.txt"
getMatrix(load_path,saved_path)
stock_earning=pd.read_excel(".../A股17年每股净利润.xlsx")
x=np.loadtxt(saved_path)
y=np.zeros((len(x),1))
count=0
doc_list=getAllFile(load_path)
for doc in doc_list:
    name=doc.split("/")[9].split("16")[0]
    print(name)
    earning=stock_earning[stock_earning['name']==name].EPS.values[0]
    y[count][0]=earning
    count+=1
X_train,X_test,Y_train,Y_test = train_test_split(x,y,train_size=0.6)
model = LinearRegression() 
model.fit(X_train,Y_train)#linear regression 
a  = model.intercept_#get the intercept
b = model.coef_#get the coefficient
Y_pred = model.predict(X_test)#predict the test dataset
s=0
for i in range(len(Y_pred)):
    s=s+(abs(Y_pred[i]-y[i]))
"""
plt.plot(range(len(Y_pred)),Y_pred,'red', linewidth=2.5,label="predict data")
plt.plot(range(len(Y_test)),Y_test,'green',label="test data")
plt.legend(loc=2)
plt.show()#显示预测值与测试值曲线
"""
np.savetxt(".../模型预测/k.txt",b)
np.savetxt(".../模型预测/b.txt",a)


