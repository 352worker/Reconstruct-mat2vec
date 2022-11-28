import pandas as pd
from tqdm import tqdm
from nltk import word_tokenize
from mat2vec.processing import MaterialsTextProcessor
import  multiprocessing
import argparse
import csv

PRO = ['solar', 'photovoltaic', 'PV', 'photodevices', 'photoelectronics', 'optoelectronic', 'optoelectronics','nano-optoelectronics', 'nano-optoelectronic', 'opto-electronic', 'opto-electronics', 'photodiodes','photodiode', 'photodetectors', 'photodetector', 'photosensor', 'photosensors', 'photosensing','LED','LEDs']

def is_pro(tok):
    if tok in PRO:
        return True
    else:
        return False


tool = MaterialsTextProcessor()

def processing(year):
    mat=[]
    f = open("../hxs_2021.csv",'r',encoding="utf-8") 
    for line in f:
        m = line.split(',')
        mat.append(m[0].strip())
    mat = list(set(mat))
    df = pd.DataFrame(index=mat)
    #df['typ'] = 0
    df['pro'] = 0
    #df['typ_pro'] = 0
    print("processing: %d" %year)
    f = open("../../para/final/%d.txt" %year, "r", encoding="utf-8")  # open the abs_txt
    # f2 = open("./abs2/MATE%d.txt" %year, "r", encoding="utf-8")

    print("processing year is %d" %year)
    abstract = f.readlines()

    for abstract in tqdm(abstract):
        mat = []
        cnt_pro = 0

        tokens = word_tokenize(abstract)
        for i, tok in enumerate(tokens):

            try:
                if tool.is_simple_formula(tok):
                    mat.append(tok)
                if is_pro(tok):
                    cnt_pro += 1
            except:
                print(tok) 
        for m in set(mat):
            if m in df.index:

                df.loc[m, 'pro'] += cnt_pro
                
            else:
                continue
    df.to_csv("./all2/%d_occur.csv" % year)


if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument("--year", type=int)

   args = parser.parse_args()

   processing(year=args.year)