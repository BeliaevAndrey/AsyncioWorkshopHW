""" Utility operations """

import os
import re

__all__ = [
    'read_file', 'write_file', 'get_filename',
    'get_path', 'print_files', 'get_file_list',
    'get_file_path_size',
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


def write_file(data: bytes,
               file_name: str,
               file_dir: str = '.',
               append_flag: bool = False) -> None:
    """
        Write (NB!) a file to disk
        :param data:      bytes     -- a data pack to write
        :param file_name: str       -- file name
        :param file_dir:  str       -- path to file, default = '.'
        :param append_flag: bool    -- open for write of append
        :return None
        """
    # write_mode = ['wb', 'ab'][append_flag]
    fullpath = os.path.abspath(file_dir)
    if not os.path.isdir(fullpath):
        print(f"Directory not found. Creating!\n{fullpath}")
        os.makedirs(fullpath)
    fullpath = os.path.join(fullpath, file_name)

    if append_flag:
        with open(fullpath, 'ab') as file_out:
            file_out.write(data)
    else:
        with open(fullpath, 'wb') as file_out:
            file_out.write(data)

    print(f'file {file_name} is written to disk')


def get_path() -> str:
    """ Read path from keyboard """
    path = input("Input path: ") or '.'

    os.path.abspath(path)
    while not os.path.isdir(path):
        path = input("Wring input. Input path: ")
        os.path.abspath(path)

    return path


def get_filename() -> str:
    """ Read filename from keyboard """

    pattern = re.compile(r'[A-Za-z\d._\-]+')

    file_name = input("Input filename: ")
    while not pattern.fullmatch(file_name):
        file_name = input("Only letters and digits. '_' instead of space"
                          "\nInput filename: ")

    return file_name


def print_files(dir_path: str) -> None:
    """ Prints file list """

    dir_path = os.path.abspath(dir_path)

    if not os.path.isdir(dir_path):
        print(f'{dir_path} NOT FOUND.')

    for file in os.listdir(dir_path):
        print(file)


def get_file_list(path: str, absolute: bool = True) -> list[str] | None:
    """ Returns file list (absolute paths) """

    path = os.path.abspath(path)
    if not os.path.isdir(path):
        print('Not a directory!')
        return
    if absolute:
        return [*map(lambda x: os.path.join(path, x), os.listdir(path))]
    return os.listdir(path)[:]


def get_file_path_size(path, file_name: str) -> tuple[str, int] | None:
    for file in get_file_list(path, False):
        if file == file_name:
            path = os.path.join(path, file_name)
            size = os.path.getsize(path)
            return path, size
