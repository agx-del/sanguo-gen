# codeing: utf-8

from keras.models import Model
from keras.layers import Input, Dense, Embedding, LSTM, Dropout
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam, RMSprop
from keras.utils import to_categorical
import numpy as np
from collections import deque


class BaseModel():
    def __init__(self, input_shape, words_db_len):
        self.input_shape = input_shape
        self.words_db_len = words_db_len
        self.model = None
        self.create_model()

    def create_model(self):
        in_x = Input(self.input_shape)

        network = Embedding(self.words_db_len+1, 256)(in_x)
        network = LSTM(512, return_sequences=False)(network)
        #network = BatchNormalization()(network)
        network = Dropout(0.5)(network)

        network = Dense(self.words_db_len, activation='softmax')(network)

        self.model = Model(inputs=in_x, outputs=network)
        self.model.summary()

        opt = RMSprop()
        loss = 'categorical_crossentropy'
        self.model.compile(optimizer=opt, loss=loss,
                           metrics=['accuracy'])

    def loss_train(self, X, Y, batch_size, epochs=1):
        #print("X shape:%s" % str(X.shape))
        in_Y = to_categorical(Y, num_classes=self.words_db_len)
        #print("Y shape:%s" % str(in_Y.shape))
        #print("Y:%s" % in_Y)
        self.model.fit(x=X, y=in_Y, batch_size=batch_size, epochs=epochs)

    def save(self, filename):
        self.model.save(filename)


class ArticleModel(BaseModel):
    def __init__(self, wdb, input_shape, words_db_len):
        super(ArticleModel, self).__init__(input_shape, words_db_len)
        self.wdb = wdb

    def loss_train(self, X, Y, batch_size, epochs=1):
        print("X shape:%s" % str(X.shape))

        for i in range(epochs):
            print("train round %d/%d" % (i+1, epochs))
            # for i in range(10):
            # print(X[i])
            # print("round:%d\nX(raw):%s\nX:%s\nY:%s\n" %
            #      (i, X[i], self.wdb.idx2words(X[i]), self.wdb.idx2words(Y[i])))
            super(ArticleModel, self).loss_train(X, Y, batch_size, epochs=1)
            self.save("temp.h5")
            atc = self.get_article(
                "第一回 兵败落凤坡", output_len=500)
            print("%d round predict:\n%s\n" % (i+1, atc))

    def get_article(self, input_str, output_len=1000):
        words = []
        start_pos = len(input_str)
        word = ''
        words.append(input_str)
        in_str_vec = deque([0]*self.input_shape[0],
                           maxlen=self.input_shape[0])
        #print("cycle input len:%d" % self.input_shape[0])
        for i in range(len(input_str)):
            in_str_vec.append(self.wdb.word2idx(input_str[i]))
        #print("first input:%s" % in_str_vec)
        for i in range(start_pos, output_len, 1):
            # print("i:%d - X:%s" %
            #      (i, "".join(self.wdb.idx2words(list(in_str_vec)))))
            in_vec = np.array(in_str_vec)
            in_vec = np.expand_dims(in_vec, axis=0)
            #print("in_vec:%s" % in_vec)
            pred_vec = self.model.predict_on_batch(in_vec)[0]
            #print("pred_vec:%s" % pred_vec)
            word = self.wdb.idx2word(
                np.argmax(pred_vec))
            #print("Y:%s" % word)
            in_str_vec.append(self.wdb.word2idx(word))
            words.append(word)
        ret_str = "".join('%s' % word for word in words)
        return ret_str
