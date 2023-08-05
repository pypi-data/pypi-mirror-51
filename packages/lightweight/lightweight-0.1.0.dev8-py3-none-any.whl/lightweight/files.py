from glob import iglob
from pathlib import Path
from typing import Iterator


def create_file(path: Path, *, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w') as f:
        f.write(content)


def paths(glob_path: str) -> Iterator[Path]:
    """An iterator of paths matching the provided `glob`_ pattern.

    _glob: https://en.wikipedia.org/wiki/Glob_(programming)"""
    return map(Path, iglob(glob_path, recursive=True))


def strip_extension(file_name: str):
    return file_name.rsplit('.', 1)[0]
