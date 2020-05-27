import shutil
from pathlib import Path
import zipfile

def is_valid_zip_file(path: Path) -> bool:
    zf = zipfile.ZipFile(str(path))
    return zf.testzip() is None

# From: https://stackoverflow.com/questions/1855095/
def zipdir(inpath: Path, outpath_sans_extension: Path) -> Path:
    if not inpath.is_dir: raise Exception(f"Path {inpath} must to be a directory.")

    outpath_with_extension = shutil.make_archive(str(outpath_sans_extension), 'zip', inpath)
    return Path(outpath_with_extension)