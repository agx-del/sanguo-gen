# coding=utf-8
import datasets.words_db
import utils.utils
import datasets.dataset
import model.model
import numpy as np

article_fn = './data/sanguo.txt'
all_words = utils.utils.get_all_words_in_article(article_fn)
none_rpt_words = utils.utils.get_all_none_repeated_words(all_words)
# print(none_rpt_words)

wdb = datasets.words_db.WordsDb(none_rpt_words)
dataset = datasets.dataset.TrainDataset(
    article_fn, wdb, dataset_len=100, read_step=3)

#print(wdb.words2idx_fix_len("古今多少事，都付笑笑谈中", fix_len=10))
X, Y = dataset.get_data()

acticle_model = model.model.ArticleModel(wdb, X[0].shape, wdb.unknow_idx)
acticle_model.loss_train(X, Y, 1024, 200)
#article = acticle_model.get_article("俱往矣，数风流人", output_len=1000)
#print("output:%s" % article)
