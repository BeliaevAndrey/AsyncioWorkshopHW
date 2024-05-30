import socket
from util import *


def start_listen(host_addr: str, host_port: int):

    buffer = b''

    receiver_socket = socket.socket()
    receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiver_socket.bind((host_addr, host_port))
    receiver_socket.listen()

    print(f"Listening at: {host_addr}:{host_port}")

    connection, client_address = receiver_socket.accept()

    file_size = 0
    file_name = 'tmp_buffer'

    try:
        while True:
            data = connection.recv(1024)
            if data.startswith(b'FILE:'):
                line = data.decode()
                print(f'{line=}')
                file_params = line.split(':')
                file_name = file_params[1]
                file_size = file_params[-1]

                print(f'{file_name=}\n{file_size=}\n{file_params=}')

                try:
                    file_size = int(file_size)
                    print(f'Trying to get a file of size: {file_size}')
                    connection.send(b'Ready')
                except Exception as exc:
                    print(f'\033[31m{exc.__class__.__name__}: {exc}')
                    connection.close()
                    break
                finally:
                    data = b''
            elif len(data) < 1024:
                buffer += data
                break
            else:
                buffer += data

    finally:
        print('\n\n')
        receiver_socket.close()
    print(f'{len(buffer)=} == {file_size=} -> {len(buffer)==file_size}')
    if buffer:
        print(f'{len(buffer)=}')
        try:
            write_file(buffer, file_name, file_dir='files_received')
        except NotADirectoryError as exc:
            print(f"{exc}")
        except Exception as exc:
            print(f'{exc}')


def starter():
    host_addr = '127.0.0.1'
    host_port = 8020
    start_listen(host_addr, host_port)


if __name__ == '__main__':
    starter()
