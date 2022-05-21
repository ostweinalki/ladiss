from PIL import Image
from toml import load
from pathlib import Path


def get_root() -> str:
    return str(Path(__file__).parent.parent)


def get_image(file):
    Image.open(Path(get_root()) / f'images/{file}')


def get_lager(file):
    return dict(load(Path(get_root()) / f'{file}'))
