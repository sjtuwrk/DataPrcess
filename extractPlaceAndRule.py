import json
import os
import re
from nltk.tokenize import WordPunctTokenizer
import nltk

def fn(appstr):
    c = nltk.word_tokenize(appstr[4:])
    print(c)
    strArr = ["CO.LTD.", "CO.,LTD", "CO., LTD", "MILL C O,." "LTD  CO.", "LTD", "MILL",
              "CO LTD", "CO.,LIMITED", "CO LTD", "COMPANY", "MANUFACTURING", "LLC", "CO,. LTD",
              "CO.,LT", "CORPORATION LIMITED", "CO.,LTD", "CO.,LTD.","CO.,LIMITED.","CO. LTD",
              "LTD. CO.","LTD.","CO.", "LTD"]  # 公司标识符字符串数组

    if c[0].startswith('/'):
        companyStartLabel = 1
    else:
        companyStartLabel = 0

    placeEndLabel = len(c) - 1

    placeStartLabel = 2
    companyEndLabel = 1

    for i in range(len(c)):
        # print(c[i])
        for str in strArr:
           if c[i].find(str.strip()) != -1:
                #print(c[i])
                companyEndLabel = i
                placeStartLabel = i + 1

    print(companyStartLabel)
    print(companyEndLabel)
    print(placeStartLabel)
    print(placeEndLabel)

    for p in range(len(c)):
        if (p == companyStartLabel):
            print(c[p], "-ORGB")
        elif (p <= companyEndLabel and p > companyStartLabel):
            print(c[p], "-ORGI")

        elif (p == placeStartLabel):
            print(c[p], "-ADRB")
        elif (p <= placeEndLabel and p > placeStartLabel):
            print(c[p], "-ADRI")

# input 59.txt
#:59:HANGZHOU WEIGUANG ELECTRONIC CO.LTD.365 XINGZHONG ROAD, YUHANG REGION,HANGZHOU, CHINA
#:59:SIPING TIANHONG TEXTILE THREAD MANUFACTURING MILL NO.43 HAIFENG ROAD SIPING CITY JILIN PROVINCE
#:59:/33014021600229000099 HAINING JINDA COATING CO.,LTD NO.2 ZHENBEI ROAD WARP INDUSTRIAL ZONE, HAINING ZHEJIANG, CHINA

if __name__ == '__main__':
    f = open("D:/场景验证第三组/59.txt", "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回
    for text in lines:
        fn(text)
        print('\n')


