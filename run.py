#!/usr/bin/env python    
# -*- coding: utf-8 -*

'''
A tool to extract browser familiy and major version from user agents.

'''

import sys
from sklearn.ensemble import RandomForestClassifier

def read_train_file(file_name, train_output):
    # load trainging data
    train_list = []
    with open(file_name) as f:
        for line in f:
            one = line.find('\t')
            train_list.append(line[:one])
            two = line.find('\t', one+1)
            train_output.append(line[one+1:two])
    return train_list

def read_test_file(file_name, initial_vector):
    # load test data 
    test_vector = []
    with open(file_name) as f:
        for line in f:
            line=line.strip('\n')
            initial_vector.append(line)
            index = line.find('\t')
            test_vector.append(line[:index])
    return test_vector

def build_feature_vectors(data_list):
    # build 25-feature vectors for classifier
    feature_vec = []
    dict = {
        '(':1, '2':2, 'A':3, 'C':4, 'B':5, 'E':6, 'D':7, 'G':8, 'I':9, 'H':10,
        'K':11, 'M':12, 'L':13, 'O':14, 'N':15, 'P':16, 'S':17, 'U':18, 'T':19,
        'V':20, 'Y':21, 'X':22, 'Z':23, 'a':24, 'i':25, 'm':26, 's':27, 'u':28, 'v':29
    }
    for str in data_list:
        row = []
        str_lower = str.lower()
        prefix = str_lower[:20]
        # 1st feature, OS
        if "(windows" in prefix:
            row.append(1)
        elif "(linux" in prefix:
            row.append(2)
        elif "(compatible" in prefix:
            row.append(3)
        else:
            row.append(4)
        # 2nd feature, Maxthon
        if "maxthon" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 3rd feature, Mobile 
        if "mobile" in prefix:
            row.append(1)
        else:
            row.append(0)
        # 4th feature, KHTML 
        if "khtml" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 5th feature, Compatible 
        if "compatible" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 6th feature, FBAV 
        if "fbav" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 7th feature, QQ 
        if "qq" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 8th feature, .NET 
        if ".net" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 9th feature, Roccat 
        if "roccat" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 10th feature, Android 
        if "android" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 11th feature, first letter
        ch_1 = str[0]
        row.append(dict[ch_1])
        # 12th feature, Iphone
        if "ihpne" in prefix:
            row.append(1)
        else:
            row.append(0)
        # 13th feature, Ipad
        if "ipad" in prefix:
            row.append(1)
        else:
            row.append(0)
        # 14th feature, OPR
        if "opr" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 15th feature, Mini
        if "mini" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 16th feature, UCBrowser
        if "ucbrowser" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 17th feature, Sogou
        if "metasr" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 18th feature, firefox
        if "firefox" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 19th feature, fxIOS
        if "fxios" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 20th feature, Edge
        if "edge" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 21st feature, AppleWebKit
        if "applewebkit" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 22nd feature, Puffin
        if "puffin" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 23rd feature, YandexSearch
        if "yandexsearch" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 24th feature, BlackBerry
        if "blackberry" in str_lower:
            row.append(1)
        else:
            row.append(0)
        # 25th feature, Silk
        if "silk" in str_lower:
            row.append(1)
        else:
            row.append(0)
        feature_vec.append(row)
    return feature_vec

if __name__ == '__main__':

    train_output = []
    initial_vector = []

    train_list = read_train_file(sys.argv[1], train_output)
    test_list = read_test_file(sys.argv[2], initial_vector)

    trainMatrix = build_feature_vectors(train_list)
    testMatrix = build_feature_vectors(test_list)

    clf = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
    clf = clf.fit(trainMatrix, train_output)
    predict = clf.predict(testMatrix)
    # print(predict)

    # categories of user agent family
    agent_dict = {
        "Chrome": "Chrome", "Facebook": "FBAV", "Opera": "OPR", "IE": "rv", "Safari": "Safari",
        "QQ": "QQBrowser", "Edge": "Edge", "UC": "UCBrowser", "Sogou": "MetaSr", "Maxthon": "Maxthon",
        "AOL": "AOL", "AppleMail": "AppleWebKit", "Puffin": "Puffin", "Android": "Android",
        "YandexSearch": "YandexSearch", "BlackBerry": "Version", "Amazon": "Silk"
    }
 
    # compose output data with extracting major version
    res = []
    for line, agent in zip(initial_vector, predict):
        space = agent.find(' ')
        if space == -1:
            word = agent
        else:
            word = agent_dict[agent[:space]]
        if line.startswith("Opera"):
            start = line.find("Version")+8
            end = line.find(".", start)
            num = int(line[start:end])
        elif word in line:
            start = line.find(word)+len(word)+1
            end = line.find(".", start)
            num = int(line[start:end])
        elif "FxiOS" in line:
            start = line.find("FxiOS")+6
            end = line.find(".", start)
            num = int(line[start:end])
        else:
            num = 10
        res.append(line+agent+"\t"+str(num))
        # print(res)

        ouput_file = open(sys.argv[3], 'w')
        for s in res:
            ouput_file.write(s+"\n")

        ouput_file.close
