import numpy as np

class textRank:
    def __init__(self, txt, window_size = 2, threshold = 0.01, max_iter = 50):
        self.txt_split = txt.split()
        self.txt_list = list(set(self.txt_split))
        self.window_size = window_size
        self.threshold = threshold
        self.max_iter = max_iter
    
    def zero_array(self):
        self.arr = np.zeros([len(self.txt_list), len(self.txt_list)])

    def nodes(self):
        self.node = [1 for i in range(len(self.txt_list))]
        
    def freq(self):
        for i in range(len(self.txt_split) - self.window_size + 1):
            self.arr[self.txt_list.index(self.txt_split[i])][self.txt_list.index(self.txt_split[i+1])] += 1
            self.arr[self.txt_list.index(self.txt_split[i+1])][self.txt_list.index(self.txt_split[i])] += 1

    def graph(self):
        self.sum = []

        for i in range(len(self.arr)):
            tmp_sum = 0
            for j in range(len(self.arr)):
                tmp_sum += self.arr[j][i]
            self.sum.append(tmp_sum)

        for i in range(len(self.arr)):
            for j in range(len(self.arr)):
                if self.arr[i][j] != 0:
                    self.arr[i][j] = self.node[i] / self.sum[i]

    def score(self):
        self.sum = []
        self.new_node = []
        self.diff = []
        
        for i in range(len(self.arr)):
            tmp = 0
            for j in range(len(self.arr)):
                tmp += self.arr[j][i]
            self.sum.append(tmp)
        
        for i in range(len(self.node)):
            self.new_node.append((1 - 0.85) + 0.85 * self.sum[i])

        for i in range(len(self.node)):
            self.diff.append(abs(self.new_node[i] - self.node[i]))

        for i in range(len(self.node)):
            self.node[i] = self.new_node[i]

    def keyword(self):
        self.nodes()

        for i in range(self.max_iter):
            self.zero_array()
            self.freq()
            self.graph()
            self.score()     

            if min(self.diff) <= self.threshold:
                break

        return self.txt_list[self.diff.index(max(self.diff))]