# coding=utf-8
from collections import deque


class WordsDb():
    def __init__(self, words):
        self.words = words
        self.db_len = len(self.words)
        self.end_idx = self.db_len+1
        self.unknow_idx = self.db_len+2
        self.unknow_word = "E"

    def word2idx(self, word):
        if(word in self.words):
            return self.words.index(word)
        else:
            if word == 0:  # 结束标志
                return self.end_idx
            else:
                return self.unknow_idx

    def words2idx(self, words):
        idx = []
        for word in words:
            idx.append(self.word2idx(word))
        return idx

    def words2idx_fix_len(self, words, fix_len=100):
        supply_char = " "
        idx = deque([self.word2idx([supply_char])]*fix_len, maxlen=fix_len)
        in_len = len(words)
        for i in range(fix_len):
            if(i < in_len):
                idx.append(self.word2idx(words[i]))
            else:
                break
            #print("i:%d,char:%s" % (i, words[i]))
        return list(idx)

    def idx2word(self, idx):
        if(idx < self.db_len):
            return self.words[idx]
        elif idx == self.end_idx:
            return None
        else:
            return self.unknow_word

    def idx2words(self, idxs):
        words = []
        # print("word:")
        for idx in idxs:
            word = self.idx2word(idx)
            if word != None:
                #print("[%s]" % word, end="")
                words.append(word)
            else:
                break  # 有结束标志，表示结束
        # print("\n")
        return words
