from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from gensim.models.phrases import Phrases, Phraser
import gensim
import logging
import os
import argparse
import regex
import pickle
from tqdm import tqdm
from utils import EpochSaver
from pymatgen.core.composition import Composition
from gensim.models.callbacks import CallbackAny2Vec
from pymatgen.core.periodic_table import Element
logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", required=True, help="The path to the corpus to train on.")
    parser.add_argument("--model_name", required=True, help="Name for saving the model (in the models folder).")
    parser.add_argument("--epochs", default=30, help="Number of epochs.")
    parser.add_argument("--size", default=200, help="Size of the embedding.")
    parser.add_argument("--window", default=8, help="Context window size.")
    parser.add_argument("--min_count", default=1, help="Minimum number of occurrences for word.")
    parser.add_argument("--workers", default=30, help="Number of workers.")
    parser.add_argument("--alpha", default=0.01, help="Learning rate.")
    parser.add_argument("--batch", default=10000, help="Minibatch size.")
    parser.add_argument("--negative", default=15, help="Number of negative samples.")
    parser.add_argument("--subsample", default=0.0001, help="Subsampling rate.")
    parser.add_argument("-sg", action="store_true", help="If set, will train a skip-gram, otherwise a CBOW.")
    args = parser.parse_args()

    sentences = LineSentence(args.corpus)


    callbacks = [EpochSaver(name=args.model_name)]

    my_model = Word2Vec(
        sentences,
        size=int(args.size),
        window=int(args.window),
        min_count=int(args.min_count),
        sg=bool(args.sg),
        workers=int(args.workers),
        alpha=float(args.alpha),
        sample=float(args.subsample),
        negative=int(args.negative),
        compute_loss=True,
        sorted_vocab=True,
        batch_words=int(args.batch),
        iter=int(args.epochs),
        callbacks= callbacks)
    my_model.save(os.path.join("models", args.model_name))
