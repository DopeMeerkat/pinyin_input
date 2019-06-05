import numpy as np
import json

class Node(object):
    def __init__(self, hz, count, express):
        self.hz = hz
        self.count = count
        self.express = express
        self.max_prob = 0.0
        self.prev_node = None

class Graph(object):
    def __init__(self, py):
        self.levels = []
        for py in py:
            level = []
            hz_list = pyDict[py]
            for hz in hz_list:
                code = index[hz]
                count = head[code]
                express = trans[code][:]
                node = Node(hz, count, express)
                level.append(node)
            self.levels.append(level)

def readData():
    global pyDict, index, trans, head, total_num
    with open('../data/pyDict.json') as pyD:
        pyDict = json.loads(pyD.read())
    with open('../data/index.json') as ind:
        index = json.loads(ind.read())
    trans = np.load('../data/trans.npy')
    head = np.load('../data/head.npy')
    total_num = sum(head)

def viterbi(graph, lamda):
    def viterbi_i(i, graph):
        if i == 0:
            for node_j in graph.levels[i]:
                code_j = index[node_j.hz]
                num_j = head[code_j]
                node_j.max_prob = num_j / total_num
            return

        for node_j in graph.levels[i]:
            probs =  []
            code_j = index[node_j.hz]
            num_j = head[code_j]

            for node_k in graph.levels[i-1]:
                code_k = index[node_k.hz]
                num_k = head[code_k]
                if num_k == 0:
                    P_emission = 0
                else:
                    P_emission = lamda * node_k.express[code_j] / num_k + (1-lamda) * num_k / total_num
                probs.append(node_k.max_prob * P_emission)
            max_k = probs.index(max(probs))
            node_j.max_prob = probs[max_k]
            node_j.prev_node = graph.levels[i-1][max_k]
        return
    level_len = len(graph.levels)
    for i in range(level_len):
        viterbi_i(i, graph)


def optimalPath(graph):
    level_len = len(graph.levels)
    max_prob = []
    for node in graph.levels[level_len-1]:
        max_prob.append(node.max_prob)
    max_index = max_prob.index(max(max_prob))
    node = graph.levels[level_len-1][max_index]
    result = []
    real_result = ''
    while True:
        result.append(node.hz)
        node = node.prev_node
        if node is None:
            break
        if node.prev_node is None:
            result.append(node.hz)
            break
    while len(result) > 0:
        hz = result.pop()
        real_result+=hz
    return real_result

def compute(lamda):
    for lamda in [lamda]:
        accuracy = []
        count_line = 0
        for line in fin:
            py = line.lower().split()
            new_pys = []
            for py in py:
                new_pys.append(py)
            mygraph = Graph(new_pys)
            viterbi(mygraph, lamda)
            result = optimalPath(mygraph)
            result.encode('gbk')
            fout.write(result + '\n')
            print(result)


if __name__ == '__main__':
    readData()
    fin = open('../data/input.txt', 'r')
    fout = open('../data/output.txt', 'w', encoding="GBK")
    compute(0.99999)
    fin.close()
    fout.close()
