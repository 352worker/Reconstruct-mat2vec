from ast import Return
from cgitb import text
from lib2to3.pygram import Symbols
from pickle import FALSE
from re import T
from string import punctuation
from turtle import Turtle
from typing import Tuple
from gensim.models.phrases import Phraser
from nltk import word_tokenize
from pymatgen.core.composition import Composition
import regex as re
from nltk.tokenize import sent_tokenize
from tqdm import tqdm
from pymatgen.core.periodic_table import Element
from nltk.corpus import stopwords
from gensim.models.phrases import Phraser

PHRASER_PATH = "./phraser.pkl"
        

class TextProcess:
    """
    Text processor.
    """
    def __init__(self) -> None:
        print("Processing is preparing!")
        self.phraser = Phraser.load(PHRASER_PATH)
        print("make phraser!")


    symbols =['+', '-', 'x', '/', '^', '.','_', ':', '>', '<' ,'=', '~']
    number_regex = re.compile(r"^[+-]?\d*\.?\d+\(?\d*\)?+$", re.DOTALL)
    punctuations = ['!', '"','#', '$', '%', '&', "'", '(', ')', '*', '+', \
    ',', '.', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '`', '{', '}', '~','"','`','``'] + ["\"", "“", "”", "≥", "≤"]
    stop_words = set(stopwords.words('english'))



    def char_process(self, text):
        """ char_preprocess.
        let MoS<inf>2</inf> ----> MoS2
        """
        char_to_del = ['<inf>','<inf>']   # MoS<inf>2</inf>
        for ch in char_to_del:
            text = text.replace(ch, " ")
        return text


    def tokenize(self, sentence):
        """ word tokenizer  
        """
        tokens = word_tokenize(sentence)
        return tokens

    def split_sentences(slef, text):
        return sent_tokenize(text)

    def is_element(self, tok):
        try:
            ele = Element(tok)
            return True 
        except:
            return False

    def is_ele_mat(self, tok):
        try:
            comp = Composition(tok).get_el_amt_dict()
            if any([not self.is_element(key) for key in comp.keys()]):
                return False
            return True
        except:
            return False

    def is_simple_formula(self,tok):
        try:
            if self.is_ele_mat(tok) and len(Composition(tok).get_el_amt_dict().keys()) >= 2:
                return True
            else:
                return False
        except:
            return False 
    
    def normalized_formula(self, tok):
        """Normalizes materials formual
        let  Cr2Ge2Te6 ----> Cr1Ge1Te3
        """
        try:
            form = Composition(Composition(tok).reduced_formula).formula
            return form.replace(" ", "")
        except:
            return tok


    def is_number(self, tok):
        
        if len(tok) > 1 and tok[0] in self.symbols and self.number_regex.match(tok[1:].replace(",", "")) is not None:
            return True
        else:
            return self.number_regex.match(tok.replace(",", "")) is not None

    def is_ele_num_next(self, tok):
        try:
            if tok in [str(i) for i in range(2, 11)]:
                return True
            if len(Composition(tok).get_el_amt_dict().keys()) == 1 and list(Composition(tok).get_el_amt_dict().values())[0] > 1:
                return True
            else:
                return False
        except:
            return False


    def material_process(self, tokens, split_mode=0):
        def split_token(token):
            split_tokens = []
            #kkk=[]
            formula = self.normalized_formula(token)
         
            return" ".join(split_tokens)
            

        mat = []
        # tokens = []
        for i, tok in enumerate(tokens):
            if self.is_ele_mat(tok):
                try:
                    if  self.is_ele_num_next(tokens[i+1]):
                        tokens[i] = str(tokens[i]+tokens[i+1])
                        tokens[i+1] = ""
                        if  self.is_ele_num_next(tokens[i+1]):
                            tokens[i] = str(tokens[i]+tokens[i+2])
                            tokens[i+2] = ""
                            if  self.is_ele_num_next(tokens[i+1]) :
                                tokens[i] = str(tokens[i]+tokens[i+3])
                                tokens[i+3] = ""
                except IndexError:
                    continue
            
        
        for j,t in enumerate(tokens): 
            if self.is_simple_formula(t):
                norm_formula = self.normalized_formula(t)
                mat.append(norm_formula)
                if split_mode == 0:
                    tokens[j] = norm_formula
                elif split_mode == 1:
                    tokens[j] = split_token(t)
                elif split_mode == 2:
                    temp = norm_formula + " " + split_token(t) + " " + norm_formula
                    tokens[j] = temp
            if self.is_number(t):
                tokens[j] = "num"
            if self.is_supper(t):
                tokens[j] = t.lower()
        return tokens, mat


    def is_punct(slef, tok):
        if tok is "":
            return True
        if tok in slef.punctuations:
            return True
        else:
            return False

    def is_stopwords(self,tok):
        if tok in self.stop_words:
            return True
        else:
            return False

    def is_copyright(self,sent):
        if '©' in sent:
            return True
        if 'copyright' in sent:
            return True

    def is_supper(self, tok):
        if self.is_element(tok):
            return False
        if self.is_simple_formula(tok):
            return False
        if len(tok) > 1 and tok[0].isupper() and tok[1:].islower():
            return True

    def make_phrases(self, sentence):
        for i in range(2):
            sentence = self.phraser[sentence]
        return sentence




    
