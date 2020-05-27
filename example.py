from tokenizers.TokenizerFactory import TokenizerFactory
from tokenizers.Tokenizer import Tokenizer, QuoteParser, SentenceTokenizer, WordTokenizer
from pipeline import Pipeline as P, pprint
from nlp.tagging import POSTagger
import re
from corpus.Corpus import Corpus
from pathlib import Path

# nltk.download('averaged_perceptron_tagger')

pos_pipeline = P.map(lambda t: t.text) \
    | P.map(lambda x: x.replace("’", "'").strip()) \
    | P.flat_map(QuoteParser().parse) \
    | P.flat_map(SentenceTokenizer().tokenize) \
    | P.filter(lambda x: not re.match(r'(^(\s*[a-z]|…)|(“|”))', x)) \
    | P.map(WordTokenizer().tokenize) \
    | P.map(POSTagger().tag)
#   | P.map(StanfordParser().parse)

book = Corpus.fromEpub(Path("data/Moby Dick.epub"))
pprint(book.paragraphs | pos_pipeline)
