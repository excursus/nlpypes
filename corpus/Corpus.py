from pathlib import Path
from tokenizers.Tokenizer import SentenceTokenizer, WordTokenizer, Tokenizer
from tokenizers.TokenizerFactory import TokenizerFactory
from functional import seq
from functional.pipeline import Sequence
from typing import Callable, List, Any, Dict
from utils.dir import Dirtree
from ebooklib.epub import EpubBook, EpubHtml
from ebooklib import ITEM_DOCUMENT
from bs4 import BeautifulSoup
from operator import add
from .CorpusText import EpubHtmlBackedCorpusText, StringBackedCorpusText, FileBackedCorpusText, HtmlBackedCorpusText
from .epub1 import get_ebook_from
from .DiscourseUnit import DiscourseUnit

class Corpus:
    def __init__(self, texts: Sequence=seq([]), children: Sequence=seq([])):
        assert(type(texts) == Sequence, type(children) == Sequence)
        self.texts_ = texts
        self.children = children
        self.tokenizer_factory = TokenizerFactory()

    def __add__(self, other: "Corpus") -> "Corpus":
        return Corpus(texts=self.texts + other.texts,
                      children=self.children + other.children)

    # Note: This doesn't replicate the tree structure, choosing instead to flatten it to a list.
    def map(self, transform: Callable[[str], str]) -> "Corpus":
        newTexts: Sequence = self.texts.map(lambda text: text.map(transform))
        return Corpus(texts=newTexts)

    @staticmethod
    def fromFile(path: Path):
        text = FileBackedCorpusText(path)
        return Corpus(texts=seq([text]))

    @staticmethod
    def fromDirtree(dt: Dirtree) -> "Corpus":
        return Corpus(texts=dt.files.map(FileBackedCorpusText),
                   children=dt.children.map(Corpus.fromDirtree))

    @staticmethod
    def fromHtml(path: Path):
        text = HtmlBackedCorpusText(path.read_text())
        c = Corpus(texts=seq([text]))
        c.path = path
        return c

    @staticmethod
    def fromEpub(path: Path, filter: Callable[[EpubHtml], bool]=None) -> "Corpus":
        epub: EpubBook = get_ebook_from(path)
        epubhtmls = seq(epub.get_items_of_type(ITEM_DOCUMENT)) # generator of ebooklib.epub.EpubHtml
        if filter:
            epubhtmls = epubhtmls.filter(filter)
        epubhtmls = seq(sorted(epubhtmls, key=lambda x: x.file_name))
        texts = seq(epubhtmls.map(EpubHtmlBackedCorpusText))

        corpus = Corpus(texts=texts)
        corpus.path = path
        return corpus

    def tokens(self, unit: DiscourseUnit, tokenizer: Tokenizer=None) -> Sequence:
        tokenizer = tokenizer or self.tokenizer_factory.get(unit)
        return seq(self.texts.flat_map(lambda x: x.tokens(unit, tokenizer=tokenizer)))

    @property
    def texts(self) -> Sequence:
        return seq(self.children.flat_map(Corpus.texts)) + seq(self.texts_)

    @property
    def lines(self):
        return self.tokens(DiscourseUnit.line)

    @property
    def paragraphs(self):
        return self.tokens(DiscourseUnit.paragraph)

    @property
    def words(self):
        return self.tokens(DiscourseUnit.word)

    @property
    def sentences(self):
        return self.tokens(DiscourseUnit.sentence)

    def __str__(self) -> str:
        return (self.texts.map(str)).reduce(add)

    def addChild(self, child):
        self.children + [child]

    def merge_epub_corpus(self) -> BeautifulSoup:
        out = BeautifulSoup("", features="lxml")
        for html in self.texts:
            assert(isinstance(html, EpubHtmlBackedCorpusText))
            for elem in html.content.body:
                out.append(elem)
        return out
