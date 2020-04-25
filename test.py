# coding=utf-8
import datasets.words_db
import utils.utils
import datasets.dataset

article_fn = './data/test.txt'
all_words = utils.utils.get_all_words_in_article(article_fn)
none_rpt_words = utils.utils.get_all_none_repeated_words(all_words)
#print("wdb:%s" % none_rpt_words)

# test_str = "自此三国归于晋帝司马炎，为一统之基矣。此所谓“天下大势，合久必分，分久必合”者也。\n后来后汉皇帝刘禅亡于晋泰始七年，魏主曹奂亡于太安元年，吴主孙皓亡于太康四年，皆善终。后人有古风一篇，以叙其事曰："
# print("\n原始文字:\n%s\n" % test_str)
wdb = datasets.words_db.WordsDb(none_rpt_words)
# vector = wdb.words2idx(test_str)
# print("编码后:\n%s\n" % vector)

# line = wdb.idx2words(vector)
# print("解码后:\n%s\n" % ("".join(line)))

dataset = datasets.dataset.TrainDataset(
    article_fn, wdb, dataset_len=10, read_step=1)

X, Y = dataset.get_data()
#print("first str:\n%s" % all_words[0:100])
#print("first str in dataset:\n%s" % dataset.words[0:100])
print("X Shape:%s" % str(X.shape))
print("Y Shape:%s" % str(Y.shape))
# for i in range(len(X)):
#    print("X%d:%s\nY:%s" % (i, X[i], Y[i]))
#    print("X decode is:%s" % "".join(wdb.idx2words(X[i])))
#    print("Y decode is:%s\n" % "".join(wdb.idx2words(Y[i])))
