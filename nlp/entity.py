from basics import *
import en_core_web_sm
from typing import List

class NounPhraseExtractor:
    def extract(self, s: str) -> List[str]:
        return []

class EntityRecognizer:
    def __init__(self):
        self.spacy = en_core_web_sm.load()

    def recognize(self, s: str) -> List[str]:
        doc = self.spacy(s)
        results = [x.text  for x in doc.ents]
        return results
