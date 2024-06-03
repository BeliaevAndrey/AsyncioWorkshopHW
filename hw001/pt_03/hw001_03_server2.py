import socket
import os

from util import *

CHUNK_SIZE = 1024
FILES_PATH = os.path.abspath('server_files')

MENU = [
    'list files',
    'upload file',
    'download file',
    'leave',
]
MENU_STRING = '\n'.join([f'{n:<3} {v}' for n, v in enumerate(MENU, start=1)]).encode()


def listener(host_addr: str, host_port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host_addr, host_port))
        server_socket.listen()

        print(f'Server listens to {host_addr}:{host_port}')

        while True:
            connection, client_address = server_socket.accept()
            try:
                while True:
                    data = connection.recv(CHUNK_SIZE)
                    if not data:
                        break
                    print(f"Received: {data.decode('utf-8')}")

                    if data == b'handshake':
                        connection.send(MENU_STRING)

                    elif data.startswith(b'COMMAND:'):
                        command_num, *command_suf = data.decode('utf-8').split(':')[1:]
                        print(f'{command_num = } {command_suf = }')
                        match command_num:
                            case '1':  # file list
                                send_file_list(connection)
                            case '2':  # upload
                                data_receiver(connection)
                            case '3':  # download
                                pass
                            case '4':  # leave
                                connection.close()
                                break
                            case 'EXIT':  # leave
                                connection.close()
                                break
                    elif data.startswith(b'FILE:'):
                        pass

                    else:
                        break

            except Exception as exc:
                print(f'\033[31mERROR: {exc.__class__.__name__} {exc}\033[0m')
                raise exc
            finally:
                connection.close()


def send_file_list(connection: socket.socket) -> None:
    """ Send file list to client """
    f_list = '\n'.join(get_file_list(FILES_PATH, False))
    connection.send(f_list.encode())


def data_receiver(connection: socket.socket):
    """
    A function to upload a file form client.
    :param connection: socket of client data exchange
    :return: ...
    """
    buffer: bytes = b''
    file_size: int = 0
    file_name: str = ''
    append_flag: bool = False

    while True:
        data = connection.recv(CHUNK_SIZE)
        print(f'{len(data)}')
        if data.startswith(b'FILE:'):
            file_name, file_size = data.decode().split(':')[1:]
            file_size = int(file_size)
            print(f'{file_name=}\n{file_size=}')
            bytes_exist = check_if_present(file_name)
            if bytes_exist == file_size:
                request = (f'file exists, size: {bytes_exist}\n'
                           f'Rewrite? (y/n)').encode()
                connection.send(request)
                data = connection.recv(CHUNK_SIZE)
                if data.decode('utf-8') in 'Nn':
                    return
            elif bytes_exist and bytes_exist < file_size:
                request = (f'file exists, size: {bytes_exist}\n'
                           f'Rewrite/Append? (R/A)').encode()
                connection.send(request)
                data = connection.recv(CHUNK_SIZE)
                if data.decode('uft-8') in 'Aa':
                    append_flag = True

            connection.send(b'READY')
        else:
            if len(data) and len(data) < CHUNK_SIZE or len(buffer) == file_size:
                buffer += data
                write_file(buffer, file_name, FILES_PATH, append_flag)
                return
            else:
                buffer += data


def data_sender():
    pass


def check_if_present(file_name: str) -> int:
    """
    Not implemented yet. Must return position (size) of file if presents
    to continue uploading. A dictionary of sessions should be realized.
    """
    files = get_file_list(FILES_PATH)

    for file in enumerate(map(lambda x: x.rsplit('/', 1)[-1], files)):
        if file[1] == file_name:
            return os.path.getsize(files[file[0]])
    return 0


# =============================================================================
def starter():
    host_addr, host_port = '127.0.0.1', 8020
    listener(host_addr, host_port)


# =============================================================================
if __name__ == '__main__':
    starter()
