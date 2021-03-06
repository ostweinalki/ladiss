from PIL import Image
from toml import load
from pathlib import Path

import s3fs
import pandas as pd


def get_root() -> str:
    return str(Path(__file__).parent.parent)


def get_image(file):
    Image.open(Path(get_root()) / f'images/{file}')


def get_lager(file):
    return dict(load(Path(get_root()) / f'{file}'))


def read_file_as_df(filename):
    # get file using pandas s3 import
    df = pd.read_csv(f's3://{filename}')
    return df


def add_diss_to_s3(filename, row):
    # get file from connection object
    fs = s3fs.S3FileSystem(anon=False)
    with fs.open(filename, 'a', newline='') as f:
        row = str(row)[1:-1].replace("'", '')
        return f.writelines('\n' + row)
