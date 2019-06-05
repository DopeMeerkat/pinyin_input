# Pinyin Input Method
## Abstract
This algorithm implements a word-based binary model conversion from pinyin to Chinese characters.

The characters used are listed in the file ‘pinyinData/一二级汉字表.txt’, and its complimentary file ‘pinyinData/拼音汉字表.txt’ lists the pinyin for these characters.

The algorithm uses data from sina news to train, stored in ‘sina_news_gbk’.

In order to use the code, the user must first train using train.py, then use viterbi.py to use the pinyin inputs from ‘data/input.txt’ to ‘data/output.txt’.

## Implementation
In order to predict Chinese characters based on Pinyin, we will use a Hidden Markov Model (HMM). In this case, the observation objects are in the form of the user’s pinyin input, while the hidden sequence is the phrase that the user wants in Chinese. The highest continuous probability of each sequence state should yield the most desired outcome, which would be the intended sentence in Chinese.

We will use the Viterbi algorithm to find the optimal path. If we draw out every possible value of a node in the hidden sequence, we will find that this is actually a problem of finding the optimal path for a directed graph.

### Training
Since working with a large data set takes time, we will split the process up so that you won’t be required to go over the data again when working with new inputs. This part of the code aims to compile the data into data structures to make it easier for the next part to utilize. The program crawls through each file using regular expressions, so that it exclusively picks up Chinese Unicode characters. We use python’s dict for hash maps, while using numPy for arrays.

### Viterbi
This section iterates through the list of inputs and performs the Viterbi algorithm on each sentence. It also uses a smoothing algorithm to deal with the sparsity of the data. 

## Experimental Results
In addition to the standard inputs, I asked a few people to write some inputs in order to get an accurate representation of what everyday language looks like:

|      | Input | Expected Answer | Output | Accuracy |
| ---- | ----- | -------- | ------ | ------ | -------- |
| 1 | qing hua da xue ji suan ji xi | 清华大学计算机系 | 清华大学计算机系 | 8/8 |
| 3 | wo shang xue qu le | 我上学去了 | 我上学去了 | 5/5 |
| 4 | jin tian hui jia bi jiao wan | 今天回家比较晚 | 今天会价比较完 | 4/7 |
| 5 | liang hui zai bei jing zhao kai | 两会在北京召开 | 两会在北京召开 | 7/7 |
| 6 | jin tian shi si yue er shi yi ri | 今天是四月二十一日 | 今天事司约尔士一日 | 4/9 |
| 7 | xiang bi zhi xia | 相比之下 | 相比之下 | 4/4 |
| 8 | xiang xing jian chu | 相形见绌 | 项行检出 | 0/4 |
| 9 | tian qi qing lang | 天气晴朗 | 天气晴朗 | 4/4 |
| 10 | wo shi ni ba | 我是你爸 | 我是泥巴 | 2/4 |
| 11 | ji suan neng li de ti sheng dai lai suan fa de gai jin | 计算能力的提升带来算法的改进 | 计算能力的提升带来算法的改进 | 14/14 |
| 12 | zhe shi yi ge ce shi wen jian | 这是一个测试文件 | 这是一格栅式文件 | 6/8 |
| 13 | zhou liu shang wu jian | 周六上午见 | 周六上午间 | 4/5 |
| 14 | ni hao peng you | 你好朋友 | 你好朋友 | 4/4 |
| 15 | guo ji sheng lan qiu dui yu jin tian zhan bai | 国际篮球生于今天战败 | 国际生篮球队于今天战败 | 11/11 |

Overall accuracy = 79.0419%

## Conclusion
Overall, the program’s accuracy is pretty good given the data it had to work with.

One key aspect is that the corpus consists of exclusively news sources. This is good for consistency since common words will most likely be used in similar ways, leading to increased accuracy of results. However, a downside to this is that the sentences will be taken as if it were in the context of news, even when the user intended otherwise.

A simple way to improve the accuracy would be to give it more data sets to work with, so long as they’re consistent with their context.
Since the corpus is from news sources, it’s not likely that they will have phrases such as idioms (成语) or slang terms. 

Additionally, the handling of the corpus was very rough and split the sentence up whenever there wasn’t a Chinese Unicode character, including numbers. This can lead to some issues when dealing with scenarios such as dates in the form of “y年m月d日”.

This also leads to a lot of broken sentences, which could possibly give words more head cases than they should, as well as have a few missing some transition cases.

Finally, if we test the accuracy of results while adjusting the value of lambda, we can improve the accuracy even further.
