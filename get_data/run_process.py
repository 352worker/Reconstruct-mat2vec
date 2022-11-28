import text_process
from tqdm import tqdm
import multiprocessing



mp = text_process.TextProcess()
def process(year):
    f1_corpus = open("./abs/abs%d.txt" %year, 'r',encoding="utf-8")  # daichuli
    f2_unsplit_sent_abs = open("../../results/text-v0/%dpara.txt" %year, 'w', encoding="utf-8") 
    f3_split_sent_abs = open("../../results/sent-v0/%sent.txt" %year, 'w', encoding="utf-8")
    f4_mat = open("../../results/mat-v0/%dmat.txt" %year, 'w', encoding="utf-8")
    # f5_error = open("./error/2d2020.txt", 'w', encoding="utf-8")
    texts = f1_corpus.readlines()

    for text in tqdm(texts):
        # try:
        text = mp.char_process(text)
        words = mp.tokenize(text)
        p_tokens, mat = mp.material_process(words,split_mode=0)
        text = " ".join(p_tokens)
        f2_unsplit_sent_abs.write(text + '\n')
        for m in mat:
            f4_mat.write(m +'\n')
        sents = mp.split_sentences(text)
        for sent in sents:
            if mp.is_copyright(sent):
                continue
            tokens =[]
            words = mp.tokenize(sent)
            for tok in words:
                if mp.is_punct(tok):
                    continue
                if mp.is_stopwords(tok):
                    continue
                tokens.append(tok)
            if len(tokens) < 5:
                continue
            f3_split_sent_abs.write(" ".join(tokens) + '\n') 


if __name__ ==  '__main__':
    pool = multiprocessing.Pool(1)
    for i in range(1921,2012):
        pool.apply_async(func=process, args=(i,))
    pool.close()
    pool.join()
    print("end!")
    # process(1928)
