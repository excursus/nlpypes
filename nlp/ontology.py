from basics import *
from nltk.corpus import wordnet as wn

class Ontology:
    def __init__(self):
        pass

    def synsets(self, s):
        return wn.synsets(s)