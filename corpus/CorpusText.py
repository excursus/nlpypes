from tokenizers.Tokenizer import SentenceTokenizer, WordTokenizer, Tokenizer, DoubleNewlineParagraphTokenizer, LineTokenizer
from tokenizers.html import HtmlParagraphTokenizer
from tokenizers.TokenizerFactory import TokenizerFactory
from functional import seq
from functional.pipeline import Sequence
from typing import Callable, List, Any, Dict
from .epub1 import get_ebook_from
from ebooklib.epub import EpubBook, EpubHtml
from ebooklib import ITEM_DOCUMENT
from bs4 import BeautifulSoup
from operator import add
from pathlib import Path
from .DiscourseUnit import DiscourseUnit

class CorpusText:
    def __init__(self, content):
        self.content = content
        self.tokenizer_factory = TokenizerFactory()

    def __str__(self):
        raise NotImplementedError()

    def map(self, transform: Callable[[str], str]) -> 'CorpusText':
        return StringBackedCorpusText(transform(str(self)))

    def tokens(self, unit: DiscourseUnit, tokenizer: Tokenizer=None) -> Sequence:
        tokenizer = tokenizer or self.tokenizer_factory.get(unit)

        if unit == DiscourseUnit.text:
            return seq([self.content])
        else:
            depends = {DiscourseUnit.paragraph: DiscourseUnit.text,
                       DiscourseUnit.sentence: DiscourseUnit.paragraph,
                       DiscourseUnit.word: DiscourseUnit.sentence}
            dependType = depends[unit]
            dependency = self.tokens(dependType)
            return seq(dependency).flat_map(tokenizer.tokenize)

    @property
    def paragraphs(self) -> Sequence:
        return self.tokens(DiscourseUnit.paragraph)

    @property
    def sentences(self) -> Sequence:
        return self.tokens(DiscourseUnit.sentence)

    @property
    def words(self) -> Sequence:
        return self.tokens(DiscourseUnit.word)

    @property
    def lines(self) -> Sequence:
        return self.tokens(DiscourseUnit.line)


    # def paragraphs(self, tokenizer: Tokenizer=None) -> Sequence:
    #     raise NotImplementedError()

    # def sentences(self, tokenizer: Tokenizer=None) -> Sequence:
    #     raise NotImplementedError()

    # def lines(self, tokenizer: Tokenizer=None) -> Sequence:
    #     raise NotImplementedError()

    # def words(self, tokenizer: Tokenizer=None) -> Sequence:
    #     raise NotImplementedError()

    # def paragraphs(self, tokenizer: Tokenizer=None) -> Sequence:
    #     tokenizer = tokenizer or CorpusText.tokenizers[DiscourseUnit.paragraph]

    # def sentences(self, tokenizer: Tokenizer=None) -> Sequence:
    #     tokenizer = tokenizer or CorpusText.tokenizers[DiscourseUnit.sentence]

    # def lines(self, tokenizer: Tokenizer=None) -> Sequence:
    #     tokenizer = tokenizer or CorpusText.tokenizers[DiscourseUnit.line]

    # def words(self, tokenizer: Tokenizer=None) -> Sequence:
    #     tokenizer = tokenizer or CorpusText.tokenizers[DiscourseUnit.word]

class StringBackedCorpusText(CorpusText):
    def __init__(self, string: str):
        super().__init__(string)
        self.tokenizer_factory = TokenizerFactory({
            DiscourseUnit.word: WordTokenizer(),
            DiscourseUnit.sentence: SentenceTokenizer(),
            DiscourseUnit.paragraph: DoubleNewlineParagraphTokenizer(),
            DiscourseUnit.line: LineTokenizer})

    def __str__(self):
        return self.content

## A thin wrapper around a string-backed corpus text
class FileBackedCorpusText(StringBackedCorpusText):
    def __init__(self, path: Path):
        self.path = path
        super().__init__(self.path.open().read()) # should be done lazily


class HtmlBackedCorpusText(CorpusText):
    def __init__(self, string: str=None, bts: bytes=None):
        if bool(string) == bool(bts):
            raise Exception("May initialize with either string or bytes but not both.")
        content = BeautifulSoup(bts or string, features="lxml")
        super().__init__(content)
        self.tokenizer_factory = TokenizerFactory({
        DiscourseUnit.paragraph: HtmlParagraphTokenizer()})

    def bytes_to_soup(self, bts: bytes) -> BeautifulSoup:
        return BeautifulSoup(bts, features="lxml")

    def __str__(self) -> str:
        return str(self.content)

    def lines(self, tokenizer: Tokenizer=None) -> Sequence:
        # Structured documents replace the notion of lines (a holdover from unstructured documents) with that of the pargraph.
        return self.paragraphs

class EpubHtmlBackedCorpusText(HtmlBackedCorpusText):
    def __init__(self, epub: EpubHtml):
        self.epub: EpubHtml = epub
        bytes = self.epub.get_content()
        super().__init__(bts=bytes)
