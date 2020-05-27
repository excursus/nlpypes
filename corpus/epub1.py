from pathlib import Path
from typing import Callable, List, Tuple, Any
from ebooklib import epub
from utils.ziputils import is_valid_zip_file, zipdir
import tempfile

# def get_epub_as_corpus_from(path: Path) -> epub.EpubBook:
#     epb = get_ebook_from(path)

def get_ebook_from(path: Path) -> epub.EpubBook:
    try:
        return epub.read_epub(str(path))
    except IsADirectoryError:
        pathhint: Path = Path(str(tempfile.mkdtemp())) / path.name
        path = zipdir(path, pathhint)
        return epub.read_epub(str(path))
    if is_valid_zip_file(path):
        return epub.read_epub(str(path))
    else:
        raise Exception(f"Not valid epub format (neither zip file nor directory) at {path}")
