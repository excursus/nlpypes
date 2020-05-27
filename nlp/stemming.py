from basics import *
from nltk.stem.porter import PorterStemmer

class Stemmer:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def stem(self, token: str) -> str:
        return self.stemmer.stem(token)