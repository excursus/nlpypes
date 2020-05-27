from nltk.parse.corenlp import CoreNLPParser, CoreNLPDependencyParser
from nlp.tagging import POSTaggedList

class StanfordParser():
    def __init__(self):
        self.parser = CoreNLPParser()
        self.i = 0

    def parse2(self, lst: list):
        parse = list(self.parser.parse(lst))
        return(parse)

    def parse(self, s: POSTaggedList):
        assert(isinstance(s, POSTaggedList))
        self.i += 1
        parse = list(self.parser.parse(s.flatten()))[0]
        return(parse)

class DepParser():
    def __init__(self):
        self.parser = CoreNLPDependencyParser()
        self.i = 0
        
    def parse(self, s: str):
        return
        self.i += 1
        s = [a[0] for a in s if a[0] not in [",", '.']]
        parse = list(self.parser.parse(s))[0]
        return parse
