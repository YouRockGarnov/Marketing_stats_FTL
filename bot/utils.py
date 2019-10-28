from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory


@contextmanager
def TmpDir():
    with TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)
