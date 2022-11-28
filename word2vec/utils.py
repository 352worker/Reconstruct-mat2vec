

import gensim
from gensim.models.callbacks import CallbackAny2Vec
from gensim.models import Word2Vec

class EpochSaver(CallbackAny2Vec):
    def __init__(self,name):
        self.name=name
        self.iter = 0

    def on_epoch_end(self, model):
        iter_name = "{}epoch{}".format(self.name, self.iter)
        l = model.get_latest_training_loss()
        print("Model loss:", l)
        f = open("loss/loss%s.txt"%self.name, 'a', encoding="utf-8")
        f.write(iter_name + ","+ str(l) +'\n')
        self.iter += 1
        # LOSS_EPOCHES
