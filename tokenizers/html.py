from . import Tokenizer
from bs4 import BeautifulSoup
from functional.streams import Sequence
from functional import seq
from typing import Callable
from .Tokenizer import Tokenizer

class SoupTokenizer(Tokenizer):
    def __init__(self, func: Callable[[BeautifulSoup], BeautifulSoup]):
        self.func = func

    def tokenize(self, soup: BeautifulSoup) -> Sequence:
        return seq([soup]).flat_map(self.func)

class HtmlParagraphTokenizer(SoupTokenizer):
    def __init__(self):
        def tokenizer(soup: BeautifulSoup) -> [BeautifulSoup]:
            return soup.find_all('p')
        super().__init__(tokenizer)
