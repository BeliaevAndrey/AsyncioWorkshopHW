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
MENU_STRING = '\n'.join([f'{n:<3} {v}' for n, v in enumerate(MENU, start=1)])


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
                        connection.send(f'MENU:{MENU_STRING}'.encode())

                    elif data.startswith(b'COMMAND:'):
                        command_num, *command_suf = data.decode('utf-8').split(':')[1:]
                        print(f'{command_num = } {command_suf = }')
                        match command_num:
                            case '1':  # file list
                                send_file_list(connection)
                            case '2':  # upload
                                data_receiver(connection)
                            case '3':  # download
                                if not command_suf:
                                    send_file_list(connection)
                                data_sender(connection, *command_suf)
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


def send_file_list(connection: socket.socket) -> list[str]:
    """ Send file list to client """
    file_list = get_file_list(FILES_PATH, False)
    files_string = '\n'.join(file_list)
    files_string = f'FILE_LIST:{files_string}'
    connection.send(files_string.encode())
    return file_list


def data_receiver(connection: socket.socket):
    """
    A function to upload a file form client.
    :param connection: -- socket of client data exchange
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


def data_sender(connection: socket.socket, file_name: str) -> int:
    """

    :param connection: socket   -- connection: socket of client data exchange
    :param file_name: str       -- name of file to send
    :return: int: bytes_sent    -- amount of bytes successfully sent
    """
    bytes_sent: int = 0

    file_path, file_size = get_file_path_size(FILES_PATH, file_name)

    file_string = f'FILE_STRING:{file_name}:{file_size}'.encode()

    connection.send(file_string)
    confirm = connection.recv(CHUNK_SIZE)
    if confirm != b'READY':
        return 0

    with open(file_path, 'rb') as f_in:
        data_to_send = f_in.read()

    for i in range(0, file_size, CHUNK_SIZE):
        portion = data_to_send[i:i + CHUNK_SIZE]
        bytes_sent += len(portion)
        connection.send(portion)

    return bytes_sent


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
