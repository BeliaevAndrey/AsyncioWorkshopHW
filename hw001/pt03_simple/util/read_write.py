import os
import re

__all__ = [
    'read_file', 'write_file', 'get_filename',
    'get_path', 'print_files'
]


def read_file(file_name: str, file_dir: str = '.') -> bytes:
    """
    Read a file from disk
    :param file_name: str   -- file name
    :param file_dir:  str   -- path to file, default = '.'
    :return data: bytes    --
    """
    fullpath = os.path.abspath(os.path.join(file_dir, file_name))
    if not os.path.exists(fullpath):
        raise FileNotFoundError

    with open(fullpath, 'rb') as file_in:
        data = file_in.read()

    return data


def write_file(data: bytes, file_name: str, file_dir: str = '.') -> None:
    """
        Write (NB!) a file to disk
        :param data:      bytes -- a data pack to write
        :param file_name: str   -- file name
        :param file_dir:  str   -- path to file, default = '.'
        :return None
        """
    fullpath = os.path.abspath(file_dir)
    if not os.path.isdir(fullpath):
        raise NotADirectoryError
    fullpath = os.path.join(fullpath, file_name)

    with open(fullpath, 'wb') as file_out:
        file_out.write(data)


def get_path() -> str:
    path = input("Input path: ") or '.'

    os.path.abspath(path)
    while not os.path.isdir(path):
        path = input("Wring input. Input path: ")
        os.path.abspath(path)

    return path


def get_filename() -> str:
    pattern = re.compile(r'[A-Za-z\d._\-]+')

    file_name = input("Input filename: ")
    while not pattern.fullmatch(file_name):
        file_name = input("Only letters and digits. '_' instead of space"
                          "\nInput filename: ")

    return file_name


def print_files(dir_path: str) -> None:
    dir_path = os.path.abspath(dir_path)

    if not os.path.isdir(dir_path):
        print(f'{dir_path} NOT FOUND.')

    for file in os.listdir(dir_path):
        print(file)
