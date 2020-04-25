# coding=utf-8
import sys
import utils.utils
import numpy as np


class Dataset():
    def __init__(self, filename, dataset_len=100, read_step=3):
        self.fn = filename
        self.dataset_len = dataset_len
        self.read_step = read_step
        self.words = []
        self.read_words()

    def read_words(self):
        assert self.fn is not None, "[ERROR]filename is empty!"
        self.words = utils.utils.get_all_words_in_article(self.fn)

    def get_data(self, data_len=None):
        assert len(self.words) > 0, "[ERROR]input words is empty!"
        dataset_len = self.dataset_len if data_len is None else data_len
        words_len = len(self.words)
        X = []
        Y = []
        for i in range(0, words_len-1, self.read_step):
            unit_X, unit_Y = self.__get_str_unit(i, dataset_len)
            X.append(unit_X)
            Y.append(unit_Y)
        return X, Y

    def __get_str_unit(self, pos, dataset_len):
        assert pos >= 0 and pos < len(
            self.words), "[ERROR]__get_str_unit() position input error."
        # print("pos:%d,dataset_len:%d,words_len:%d" %
        #      (pos, dataset_len, len(self.words)))
        X_unit = []
        Y_unit = []
        if (pos+dataset_len) < len(self.words):
            X_unit = list(self.words[pos:pos+dataset_len])
            Y_unit = list(self.words[pos+dataset_len])
        elif pos+dataset_len >= len(self.words):
            Y_unit = [0]
            X_unit = list(self.words[pos:])+[0] * \
                (dataset_len-len(self.words[pos:]))
        #print("X_unit:%s" % X_unit)
        #print("Y_unit:%s\n" % Y_unit)
        return X_unit, Y_unit


class TrainDataset(Dataset):
    def __init__(self, filename, wdb, dataset_len=100, read_step=3):
        super(TrainDataset, self).__init__(filename, dataset_len, read_step)
        self.wdb = wdb

    def get_data(self, data_len=None):
        X, Y = super(TrainDataset, self).get_data(data_len)
        X_out = []
        Y_out = []
        data_cnt = len(X)
        out_cnt = int(data_cnt/100)
        for i in range(data_cnt):
            X_out.append(self.wdb.words2idx(X[i]))
            Y_out.append(self.wdb.words2idx(Y[i]))
            if(i % out_cnt == 0):
                print("%d%%." % (100*i/data_cnt), end="")
                sys.stdout.flush()
        return np.array(X_out), np.array(Y_out)
