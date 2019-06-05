import re
import numpy as np
import json

def readFile(filename, inputList):
    print('reading ' + filename)
    with open(filename, 'r', encoding="GBK") as f:
        for line in f:
            inputList.append(line)

def makeInd():
    pat = re.compile(r'[\u4e00-\u9fa6]')
    with open('../pinyinData/一二级汉字表.txt', 'r', encoding="GBK") as f:
        wordList = re.findall(pat, f.read())
        i = 0
        for word in wordList:
            index[word] = i
            #print(word + ' ' + str(index[word]))
            i += 1
    with open('../data/index.json', 'w') as subjs:
        json.dump(index, subjs)

def makePy():
    pat = re.compile(r'[\u4e00-\u9fa6]')
    with open('../pinyinData/拼音汉字表.txt', 'r', encoding="GBK") as f:
        for line in f:
            pyDict[line.split(' ', 1)[0]] = re.findall(pat, line)
    with open('../data/pyDict.json', 'w') as pyjs:
        json.dump(pyDict, pyjs)


def readInput():
    baseFile = '../sina_news_gbk/2016-'
    sources = ['02','04','05','06','07','08','09','10','11']
    for i in sources:
        filename = baseFile + i + '.txt'
        readFile(filename, inputList)


def transition():
    head = np.zeros(6763)
    trans = np.zeros((6763,6763))
    pat = re.compile(r'[\u4e00-\u9fa6]+')
    sentenceList = []
    #print('sentences')
    for news in inputList:
        sentenceList.append(re.findall(pat, news))
    print('head')
    for sentences in sentenceList:
        for sentence in sentences:
            if sentence[0] in index:
                head[index[sentence[0]]] += 1
    print('trans')
    for sentences in sentenceList:
        for sentence in sentences:
            for i in range(1, len(sentence)):
                if (sentence[i - 1] in index) & (sentence[i] in index):
                    trans[index[sentence[i - 1]]][index[sentence[i]]] += 1
    print('done')

    np.save('../data/head.npy', head)
    np.save('../data/trans.npy', trans)

if __name__ == '__main__':
    global index, pyDict, inputList
    index = {}
    makeInd()
    pyDict = {}
    makePy()
    inputList = []
    readInput()
    transition()
