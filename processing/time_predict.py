"""
date:2021-0301
writer:wy

"""
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.preprocessing import normalize

from gensim import utils, matutils
import numpy as np
import pandas as pd
import argparse
import logging
import random

import os

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

def predict_output_word(context_words_list1, year, data, topn=3000) -> list:
    model = KeyedVectors.load_word2vec_format("w2v_2011.txt")
    outv = KeyedVectors(200)
    outv.vocab = model.wv.vocab
    outv.index2word = model.wv.index2word
    outv.syn0 = normalize(model.syn0)
    inv = KeyedVectors(200)
    inv.vocab = model.wv.vocab
    inv.index2word = model.wv.index2word
    inv.syn0 = normalize(model.wv.vectors)
    output_vec = []
    output_mat = []

    for x in data:
        try:
            # print(x)
            output_vec.append(outv.wv[x])
            # print(1)
            output_mat.append(x)
            # print(output_mat)
        except KeyError:
            continue
    output_vec = np.array(output_vec)
    word_vocabs = [inv.wv.vocab[w] for w in context_words_list1 if w in model.wv.vocab]
    word2_indices = [word.index for word in word_vocabs]
    l1 = np.sum(inv.wv.vectors[word2_indices], axis=0)
    if word2_indices:
        l1 /= len(word2_indices)
    # propagate hidden -> output and take softmax to get probabilities
    prob_values = np.exp(np.dot(l1, output_vec.T))
    prob_values /= sum(prob_values)
    top_indices = matutils.argsort(prob_values, topn=topn, reverse=True)
    # returning the most probable output words with their probabilities
    result = [(output_mat[index1], prob_values[index1]) for index1 in top_indices]

    pred = []
    prop = []

    for i in result:
        pred.append(i[0])
        prop.append(i[1])
    #随机排序材料
    return pred
    # random.shuffle(pred) 


def write_csv(pred, year):
    pro =  []
    for i in range(year, 2022):
        df = pd.read_csv("./%d_occur.csv" %i, index_col=0)
        unit = df[df["pro"]!=0].index
        pro.append(unit)
    # print(pro)
    re = pd.DataFrame(pred,columns=["test"])
    for i in range(year,2022):
        re["%d" %year] = 0
    re = re.drop('test', axis=1)
    re.index = pred
    m = year
    for j in pro:
        for i in pred:
            if i in j:
                re.loc[i,str(m)] = int(1)
            else:
                re.loc[i, str(m)] = int(0)
        m = m + 1
    re.to_csv( "./time/%d_21.csv" % year)



if __name__ == "__main__":



    f3 = open("./word.csv")
    data = []
    for line in f3:
        data.append(line.strip())
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--year", required=True,help="start year.",type=int)
    list1 = predict_output_word(context_words_list1=['thermoelectric'],year=2011,data=data)

    write_csv(pred=list1,year=2011)    