from pathlib import Path
from functional import seq
from typing import Callable

class Dirtree:
    def __init__(self, path):
        self.path = path
        self.files = seq([])
        self.children = seq([])

    class Filter:
        doesntStartWithDot = lambda x: not x.name.startswith('.')

    @staticmethod
    def fromPath(dir: Path, filter: Callable[[Path], bool]=Filter.doesntStartWithDot):
        dt = Dirtree(dir)
        for e in dir.iterdir():
            if not filter(e): continue
            if e.is_file():
                dt.files += [e]
            elif e.is_dir():
                dt.children += [Dirtree.fromPath(e, filter=filter)]
        return dt
