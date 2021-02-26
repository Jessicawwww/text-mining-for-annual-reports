# -*- coding: utf-8 -*-

import docx
import glob
import re
import jieba.analyse
import pandas as pd


def getAllFile(path):  # convert the format of pdf to format of doc
    doc_list = []
    for doc in glob.glob("{}/*.docx".format(path)):
        doc = doc.replace("\\", "/")
        doc_list.append(doc)
    return doc_list


def get_standard():
    ################################################################################################
    # get the key words
    path = "D:/银河证券/BCG评选future50/17年报"
    doc_list = getAllFile(path)

    keywords_standard1 = []  # without repetition
    keywords1 = []  # repetitive
    keywords_standard2 = []  # withou repetition
    keywords2 = []  # repetitive
    for doc in doc_list:
        # name=doc.split("/")[7].split(".")[0]
        print(doc)
        file = docx.Document(doc)
        passage = ""
        for para in file.paragraphs:
            passage = passage + para.text
        try:
            for result in re.findall(r'详见.*?公司业务概要', str(passage)):
                if len(result) < 20:
                    passage = passage.replace(result, "")
        except:
            passage = passage
        try:
            for result in re.findall(r'参见.*?公司业务概要', str(passage)):
                if len(result) < 20:
                    passage = passage.replace(result, "")
        except:
            passage = passage
        try:
            for result in re.findall(r'详见.*?经营情况讨论与分析', str(passage)):
                if len(result) < 20:
                    passage = passage.replace(result, "")
        except:
            passage = passage
        try:
            for result in re.findall(r'参见.*?经营情况讨论与分析', str(passage)):
                if len(result) < 20:
                    passage = passage.replace(result, "")
        except:
            passage = passage
        chapter_info1 = re.findall(r'公司业务概要.*?经营情况讨论与分析', str(passage), re.DOTALL)
        if chapter_info1 == []:
            chapter1 = ""
            print("chapter1 error")
        else:
            count = [len(info) for info in chapter_info1]
            chapter1 = chapter_info1[count.index(max(count))]
            if len(chapter1) < 300:
                chapter1 = ""
                print("chapter1 error")
        chapter_info2 = re.findall(r'经营情况讨论与分析.*?重要事项', str(passage), re.DOTALL)
        if chapter_info2 == []:
            print("chapter2 error")
        else:
            count = [len(info) for info in chapter_info2]
            chapter2 = chapter_info2[count.index(max(count))]
            if len(chapter2) < 300:
                chapter2 = ""
                print("chapter2 error")
                # chapter_data=chapter_data.append({"name":str(name),"chapter1":chapter1,"chapter2":chapter2},ignore_index=True)
        # chapter_data.to_excel("f:/echow/work/银河证券实习/work/年报/second_edition/chapter_info.xlsx")
        # CHAPTER1、2 keywords by TF-IDF
        chapter1_keywords = "  ".join(
            jieba.analyse.extract_tags(chapter1, topK=100, withWeight=False, allowPOS=(['v']))).split("  ")
        chapter2_keywords = "  ".join(
            jieba.analyse.extract_tags(chapter2, topK=100, withWeight=False, allowPOS=(['v']))).split("  ")
        for word in chapter1_keywords:
            keywords1.append(word)
            if word not in keywords_standard1:
                keywords_standard1.append(word)
        for word in chapter2_keywords:
            keywords2.append(word)
            if word not in keywords_standard2:
                keywords_standard2.append(word)

        data1 = pd.DataFrame(columns=('word', 'num'))
        data2 = pd.DataFrame(columns=('word', 'num'))
        for word in keywords_standard1:
            num = keywords1.count(word)
            data1 = data1.append({'word': str(word), "num": num}, ignore_index=True)
        for word in keywords_standard2:
            num = keywords2.count(word)
            data2 = data2.append({'word': str(word), "num": num}, ignore_index=True)
    return (data1, data2)


(data1, data2) = get_standard()

data1.to_excel("D:/银河证券/BCG评选future50/关键字表/keywords_1.xlsx")
data2.to_excel("D:/银河证券/BCG评选future50/关键字表/keywords_2.xlsx")
